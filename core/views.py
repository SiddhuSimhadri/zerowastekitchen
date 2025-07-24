from django.shortcuts import render, redirect

def landing_page(request):
    # If user is already logged in, redirect to dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/landing.html')
