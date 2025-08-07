from django.shortcuts import render, redirect

# Create your views here.

def home(request):
    return redirect('home_feed')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_error(request):
    return render(request, 'error.html', status=500)
