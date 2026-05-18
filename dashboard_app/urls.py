from django.urls import path
from dashboard_app.views import client_portal_views, account_views
urlpatterns = [
    path('', client_portal_views.dashboard_view, name='dashboard_url'),
    path('account-details/', account_views.accounts_details_view, name='account_details_url'),
    path('support-create/', client_portal_views.support_create_view, name='support_create_url'),
    path('support-list/', client_portal_views.SupportListView.as_view(), name='support_list_url'),
    path('support-reply/<int:pk>/', client_portal_views.support_reply_view, name='support_reply_url'),
]
