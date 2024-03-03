from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created! You are now able to log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request,"You have been logged out.")
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'p_form': p_form,
        'breadcrumbs': [{'title': f"{request.user.username}'s Profile"}],
        'title': f'{request.user.username}'
    }
    return render(request, 'users/profile.html', context)

@login_required
def account_settings(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('account-settings')
    else:
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'u_form': u_form,
        'breadcrumbs': [{'title': 'Account Settings'}],
        'title': 'Account Settings'
    }
    return render(request, 'users/account_settings.html', context)