from django.http.response import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import redirect, render

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from .tasks import send_email_on_registration
from .utils import activation_token_generator
from .forms import RegistrationForm


def log_user_in(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next') or '/poems/'
        return redirect(next_url)
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', context={'form': form, 'next': request.GET.get('next') or '/poems/'})


def log_user_out(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')


def register(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next') or '/poems/'
        return redirect(next_url)
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            next_url = request.POST.get('next')
            current_site = get_current_site(request)
            send_email_on_registration(current_site.domain, user.id)
            return redirect(next_url)
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', context={'form': form, 'next': request.GET.get('next') or '/poems/'})


def activate(request, uid, token):
    user = User.objects.filter(id=uid).first()
    if user:
        if activation_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect(reverse('poems'))
    return HttpResponse(content='Invalid activation link', status=401)
