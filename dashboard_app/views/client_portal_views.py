import json
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from accounts.models import User
from django.urls import reverse
from dashboard_app.models import choices
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from dashboard_app.models import dashboard_models
from dashboard_app.forms import dashboard_forms


def is_support_user(user):
    return user.is_authenticated and user.user_type == 'support'


@login_required
def dashboard_view(request):
    profile = User.objects.get(pk=request.user.pk)
    base_qs = dashboard_models.Support.objects.all()
    
    if not is_support_user(request.user):
        base_qs = base_qs.filter(Q(enlisted_email=request.user.email))
    else:
        base_qs=base_qs
    
    tickets = base_qs.count()
    pending = base_qs.filter(status='pending').count()
    in_progress = base_qs.filter(status='on_progress').count()
    solved = base_qs.filter(status='solved').count()

    context = {
        'profile': profile,
        'ticket': tickets,
        'pending': pending,
        'in_progress': in_progress,
        'solved': solved,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def support_create_view(request):
    if request.method == "POST":
        form = dashboard_forms.SupportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Support request submitted successfully!')
            return redirect('home_page_url')
        else:
            messages.error(request, "Invalid form")
    else:
        form = dashboard_forms.SupportForm()

    context = {
        'form': form
    }
    return render(request, 'dashboard/support.html', context)

@method_decorator(login_required, name='dispatch')
class SupportListView(ListView):
    model = dashboard_models.Support
    template_name = 'dashboard/support_list.html'
    context_object_name = 'obj_list'
    paginate_by = 30
 
    def get_queryset(self):
        status_filter = self.request.GET.get('status', 'all')
        qs = dashboard_models.Support.objects.select_related('user').all().order_by('-id')
 
        if not is_support_user(self.request.user):
            qs = qs.filter(Q(enlisted_email=self.request.user.email))
 
        if status_filter and status_filter not in ('', 'all'):
            qs = qs.filter(status=status_filter)
 
        return qs
 
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = choices.SUPPORT_STATUS_CHOICE
        ctx['active_filter']  = self.request.GET.get('status', 'all')
 
        base_qs = dashboard_models.Support.objects.all().order_by('-id')
        if not is_support_user(self.request.user):
            base_qs = base_qs.filter(Q(enlisted_email=self.request.user.email)).order_by('-id')

 
        ctx['count_all']        = base_qs.count()
        ctx['count_pending']    = base_qs.filter(status='pending').count()
        ctx['count_on_progress'] = base_qs.filter(status='on_progress').count()
        ctx['count_solved']      = base_qs.filter(status='solved').count()
        return ctx

@login_required
def support_reply_view(request, pk):
    if not is_support_user(request.user):
        messages.error(request, "You are not authorised to reply to support tickets.")
        return redirect('support_list_url')
 
    support_obj = get_object_or_404(dashboard_models.Support, pk=pk)
 
    if request.method == 'POST':
        remarks       = request.POST.get('remarks', '').strip()
        status        = request.POST.get('status', support_obj.status).strip()
        active_filter = request.POST.get('active_filter', 'all')
 
        support_obj.remarks = remarks
        support_obj.status  = status
        support_obj.user = request.user
        support_obj.save()
 
        messages.success(
            request,
            f"Ticket #{pk} updated to '{support_obj.get_status_display()}'."
        )
 
        return redirect(f"{reverse('support_list_url')}?status={active_filter}")
 
    messages.error(request, "Invalid request.")
    return redirect('support_list_url')

@login_required
def support_ticket_delete_view(request, pk):
    obj = get_object_or_404(dashboard_models.Support, id=pk)
    obj.delete()
    messages.success(request, "Suppport ticket deleted successfully.")
    return redirect('support_list_url')

@require_POST
def customer_get_it_now_view(request):
    full_name = request.POST.get('full_name', '').strip()
    contact_no = request.POST.get('contact_number', '').strip()
    email = request.POST.get('email', '').strip()
    message = request.POST.get('message', '').strip()

    if not full_name:
        return JsonResponse({'success': False, 'message': 'Full name is required.'}, staus=400)
    if not contact_no:
        return JsonResponse({'success': False, 'message': 'Contact number is required.'}, status=400)
    
    dashboard_models.GetItNow.objects.create(
        full_name = full_name, contact_no = contact_no, email = email, message = message
    )

    return JsonResponse({'success': True, 'message': 'Thank you! We will get back to you soon.'})


@login_required
def leads_view(request):
    obj_list = dashboard_models.GetItNow.objects.all()
    return render(request, 'dashboard/leads.html', {'obj_list': obj_list})

@login_required
def leads_delete_view(request, pk):
    obj = get_object_or_404(dashboard_models.GetItNow, id=pk)
    obj.delete()
    messages.success(request, "Leads deleted successfully!!")
    return redirect('leads_url')

@login_required
def toggle_contact_status(request, pk):
    obj = get_object_or_404(dashboard_models.GetItNow, id=pk)

    obj.is_contacted = not obj.is_contacted
    if obj.is_contacted:
        obj.contacted_by = request.user
        obj.updated_at = timezone.now()
    else:
        obj.contacted_by = None
    
    obj.save()

    messages.success(request, "Contact status updated successfully.")
    return redirect("leads_url")
