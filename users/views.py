from django.shortcuts import render, redirect
from .forms import RegisterForm, ProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from .models import Profile


def register(request):
    """ User registration function """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Check if the user already has a profile
            profile, created = Profile.objects.get_or_create(user=user)
            if not created:
                # If the profile already exists, update the gender
                profile.gender = form.cleaned_data.get('gender')
                profile.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            messages.success(request, 'Bienvenue! Votre compte a été créé avec succès. Vous êtes maintenant connecté.')
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('users:profile')
    else:
        p_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'p_form': p_form})

class LoginFormView(SuccessMessageMixin, LoginView):
    """ Add a welcome message when user logs in """
    success_message = "Bienvenu! Vous êtes maintenant connecté"

@login_required
def logout_view(request):
    """ User logout function """
    logout(request)
    messages.success(request, 'Au revoir! Vous êtes maintenant déconnecté')
    return redirect('index')

@login_required
def delete_account(request):
    profile = Profile.objects.get(user=request.user)
    profile.delete()
    request.user.delete()
    messages.success(request, 'Votre compte a été supprimé avec succès.')
    return redirect('index')

