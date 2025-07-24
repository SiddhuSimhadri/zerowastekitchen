from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect, render

def custom_logout_view(request):
    logout(request)
    return render(request, 'core/landing.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Will be pantry dashboard
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})
