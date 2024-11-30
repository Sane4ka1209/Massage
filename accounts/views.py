from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import CreateView, TemplateView, FormView, UpdateView
from .models import custom_user_model
from django.contrib.auth import login, authenticate
from . import forms
# Create your views here.

User = custom_user_model()

class RegistrationView(CreateView):
    model = User
    fields = ['email', 'password']
    template_name = 'registration/registration.html'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object = None
        form = self.get_form()
        if form.is_valid():
            new_user = form.save(commit = False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('mainpage:main')
        return super().post(request, *args, **kwargs)

class ProfileView(TemplateView):
    template_name = 'registration/profile.html'

class LoginView(FormView):
    form_class = forms.LoginForm
    template_name = 'registration/login.html'

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('mainpage:main')
        return render(request, self.template_name, {'error': True, 'form': form})

class ProfileSettingsView(UpdateView):
    fields = ['first_name', 'last_name']
    model = User
    template_name = 'registration/profile_settings.html'

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> Model:
        return self.request.user
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()
        if form.is_valid():
            cd = form.cleaned_data
            user = self.request.user
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()
            return redirect('accounts:profile')
        return super().post(request, *args, **kwargs)