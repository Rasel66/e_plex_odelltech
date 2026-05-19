from .models import dashboard_models

def support_notification(request):
    pending_support_count = dashboard_models.Support.objects.filter(status='pending').count()

    return {
        'pending_support_count': pending_support_count
    }