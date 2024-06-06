from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView

from wordgame.models import Game

from .forms import CustomerUserCreationForm, CustomerAuthenticationForm, ProfileForm, CustomerUserForm
from .models import Country, CustomerUser
from .utils import send_code_email



def home(request):
    return render(request, 'home.html')

def verify_email(request, id):
    user = CustomerUser.objects.get(id=id)
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == user.auth_code:
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'verify_email.html', {'error': 'Неверный код!'})
    return render(request, 'verify_email.html')

def register(request):
    if request.method == 'POST':
        form = CustomerUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_code_email(user)
            return redirect('verify_email', user.id)
    else:
        form = CustomerUserCreationForm()
    return render(request, 'register.html', {'form': form})

class CustomerLoginView(LoginView):
    authentication_form = CustomerAuthenticationForm
    template_name = 'login.html'
    redirect_field_name = 'home'

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    games = Game.objects.filter(user=request.user, completed_at__isnull=False).order_by('-created_at')
    return render(request, 'profile.html', {'games': games})

@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        user_form = CustomerUserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = CustomerUserForm(instance=user)
        profile_form = ProfileForm(instance=profile)
    
    countries = Country.objects.all()
    return render(request, 'authorization/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'countries': countries,
    })





"""
GET  - Получение 
POST - Отправка
PATCH - Изменения одного из полей или более
PUT - Изменения всех полей
DELETE - Удаление
"""
