from django.urls import path
from dashboard_app.views import client_portal_views, account_views
urlpatterns = [
    path('', client_portal_views.dashboard_view, name='dashboard_url'),
    path('account-details/', account_views.accounts_details_view, name='account_details_url'),
    path('support-create/', client_portal_views.support_create_view, name='support_create_url'),
    path('support-list/', client_portal_views.SupportListView.as_view(), name='support_list_url'),
    path('support-delete/<int:pk>/', client_portal_views.support_ticket_delete_view, name='support_delete_url'),
    path('support-reply/<int:pk>/', client_portal_views.support_reply_view, name='support_reply_url'),
    path('get-it-now/', client_portal_views.customer_get_it_now_view, name='get_it_now_submit_url'),
    path('leads/', client_portal_views.leads_view, name="leads_url"),
    path('leads-delete/<int:pk>/', client_portal_views.leads_delete_view, name="leads_delete_url"),
    path('change-contact-status/<int:pk>/', client_portal_views.toggle_contact_status, name='toggle_contact_status_url'),
    path("api/support/create/",client_portal_views.SupportCreateAPIView.as_view(),name="support_create_api"),
    path("api/support/my-list/",client_portal_views.MySupportListAPIView.as_view(),name="my_support_list_api",),
    path("api/support/<str:support_id>/",client_portal_views.SupportDetailAPIView.as_view(),name="support_detail_api",),
    path("api/support/reply/<str:support_id>/",client_portal_views.SupportReplyCreateAPIView.as_view(),name="support_reply_api"),
    path("support/details/<str:support_id>/",client_portal_views.support_details, name="support_details"),
    path("support/admin/reply/<str:support_id>/",client_portal_views.admin_support_reply_view, name="support_reply_admin_create"),
    path("api/support/<str:support_id>/reply/",client_portal_views.SupportReplyAPIView.as_view(),name="support_reply_api_admin")

]
