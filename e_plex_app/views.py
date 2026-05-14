from django.shortcuts import render, redirect

# Create your views here.

def home_page_view(request):
    return render(request, 'home.html')

def get_started_view(request):
    return render(request, 'get_started_form.html')