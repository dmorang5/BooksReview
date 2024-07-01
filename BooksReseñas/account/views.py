import requests
import json

from django.http import HttpResponse, HttpResponseNotAllowed, BadHeaderError
from django.contrib.auth import authenticate, login, logout
from django.views import View

from BooksReseñas import settings
from books.models import Review
from .forms import LoginForm,  \
 UserEditForm, ProfileEditForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib import messages
from datetime import date

from django.contrib.auth import authenticate, login

from django.shortcuts import render, redirect

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            recaptcha_response = request.POST.get('g-recaptcha-response')
            if not recaptcha_response:
                messages.error(request, 'Debes completar el reCAPTCHA.')
                return redirect('login')

            data = {
                'secret': settings.RECAPTCHA_PRIVATE_KEY,
                'response': recaptcha_response
            }
            response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = response.json()
            if result['success']:
                cd = form.cleaned_data
                user = authenticate(request, username=cd['username'], password=cd['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, 'Autenticado exitosamente.')
                        return redirect('home')
                    else:
                        messages.error(request, 'Cuenta deshabilitada.')
                else:
                    messages.error(request, 'Credenciales inválidas.')
            else:
                messages.error(request, 'Falló la verificación de reCAPTCHA.')
        else:
            messages.error(request, 'Formulario no válido.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

@login_required
def dashboard(request):
     return render(request,
     'account/dashboard.html',
     {'section': 'dashboard'})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileEditForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            profile = profile_form.save(commit=False)
            profile.user = new_user
            profile.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileEditForm()
    return render(request, 'account/register.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil actualizado ' \
                                      'exitosamente')
        else:
            messages.error(request, 'Error al actualizar tu perfil')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(
            instance=request.user.profile)
    return render(request,
                  'account/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    age = calculate_age(profile.date_of_birth)
    return render(request, 'account/profile.html', {'profile': profile, 'reviews': reviews, 'age': age})

class CustomLogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(['POST'])

