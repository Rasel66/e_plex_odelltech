from django.urls import path
from dashboard_app.views import client_portal_views, account_views
urlpatterns = [
    path('', client_portal_views.dashboard_view, name='dashboard_url'),
    path('account-details/', account_views.accounts_details_view, name='account_details_url'),
]
