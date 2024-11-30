from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('registration/', views.RegistrationView.as_view(), name = 'registration'),
    path('profile/', views.ProfileView.as_view(), name = 'profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/settings/', views.ProfileSettingsView.as_view(), name='settings'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name = 'password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name = 'password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(success_url = reverse_lazy('accounts:password_reset_done')), name = 'password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    path('password-reset/<uid64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name = 'password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name = 'password_reset_complete')
]