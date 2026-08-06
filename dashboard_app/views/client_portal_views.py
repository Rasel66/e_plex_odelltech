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

from dashboard_app.helper import get_support_details

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
        qs = dashboard_models.Support.objects.all().order_by('-id')
 
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
 
    support_obj = get_object_or_404(dashboard_models.Support, id=pk)
 
    if request.method == 'POST':
        remarks = request.POST.get('remarks', '').strip()
        status  = request.POST.get('status', support_obj.status).strip()
        active_filter = request.POST.get('active_filter', 'all')
 
        support_obj.remarks = remarks
        support_obj.status  = status
        support_obj.support_by = request.user
        support_obj.save()
 
        messages.success(request, f"Ticket #{support_obj.support_id} updated to '{support_obj.get_status_display()}'.")
 
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


from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..serializers import SupportCreateSerializer


class SupportCreateAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        api_key = request.headers.get("X-API-KEY")

        if api_key != settings.SUPPORT_API_KEY:
            return Response(
                {
                    "status": False,
                    "message": "Invalid API Key"
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = SupportCreateSerializer(data=request.data)

        if serializer.is_valid():

            support = serializer.save()

            return Response(
                {
                    "status": True,
                    "message": "Support Created Successfully",
                    "support_id": support.support_id
                },
                status=status.HTTP_201_CREATED
            )
        print(serializer.errors) 
        return Response(
            {
                "status": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )




from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from dashboard_app.models import dashboard_models
from ..serializers import SupportListSerializer


class MySupportListAPIView(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):

        api_key = request.headers.get("X-API-KEY")

        if api_key != settings.SUPPORT_API_KEY:
            return Response(
                {"status": False, "message": "Invalid API Key"},
                status=401
            )

        email = request.GET.get("email")

        queryset = dashboard_models.Support.objects.all()

        if email:
            queryset = queryset.filter(enlisted_email=email)

        serializer = SupportListSerializer(queryset.order_by("-id"), many=True)

        return Response({
            "status": True,
            "data": serializer.data
        })

from rest_framework import generics
from ..serializers import SupportDetailSerializer,SupportReplySerializer,AdminSupportReplySerializer
class SupportDetailAPIView(generics.RetrieveAPIView):

    serializer_class = SupportDetailSerializer

    lookup_field = "support_id"

    queryset = dashboard_models.Support.objects.all()


class SupportReplyCreateAPIView(APIView):

    def post(self, request, support_id):

        support = dashboard_models.Support.objects.get(
            support_id=support_id
        )

        serializer = SupportReplySerializer(
            data=request.data
        )

        serializer.is_valid(raise_exception=True)

        serializer.save(

            support=support,

            user=request.user,

            is_central_reply=False

        )

        return Response(

            serializer.data,

            status=status.HTTP_201_CREATED

        )


def support_details(request, support_id):

    response = get_support_details(support_id)

    if response.status_code != 200:
        return redirect("support_list")

    ticket = response.json()

    return render(
        request,
        "dashboard/new_support_detail.html",
        {
            "ticket": ticket
        }
    )


class SupportReplyAPIView(APIView):

    def post(self, request, support_id):

        ticket = dashboard_models.Support.objects.filter(support_id=support_id).first()

        if not ticket:
            return Response(
                {
                    "status": False,
                    "message": "Support ticket not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AdminSupportReplySerializer(
            data=request.data
        )

        if serializer.is_valid():

            dashboard_models.SupportReply.objects.create(
                support=ticket,
                user=request.data.get("user"),
                message=serializer.validated_data["message"],
                attachment=serializer.validated_data.get("attachment"),
                is_central_reply=True
            )

            ticket.status = serializer.validated_data["status"]
            ticket.save(update_fields=["status"])

            return Response(
                {
                    "status": True,
                    "message": "Reply submitted successfully."
                }
            )

        return Response(serializer.errors, status=400)

from dashboard_app.helper import reply_support_ticket

def admin_support_reply_view(request, support_id):

    if request.method == "POST":
        ticket_id=support_id
        data = {
            "user": getattr(request.user, "name", None) or "Support User",
            "message": request.POST.get("message"),
            "status": request.POST.get("status"),
        }

        files = {}

        if request.FILES.get("attachment"):
            files["attachment"] = request.FILES["attachment"]

        response = reply_support_ticket(
            ticket_id,
            data,
            files
        )

        if response.ok:
            messages.success(request, "Reply sent successfully.")
        else:
            messages.error(request, f"Failed to send reply. {response.text}")

        return redirect("support_details", support_id=support_id)