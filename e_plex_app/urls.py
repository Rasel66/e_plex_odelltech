from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page_view, name='home_page_url'),
    path('get-started/', views.get_started_view, name='get_started_url')
]