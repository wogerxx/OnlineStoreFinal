from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("signin/", LoginView.as_view(template_name="app_users/login.html", next_page='products'), name="login"),
    path("logout/", views.logout_view, name="logout"),

    path('account/<int:user_id>/', views.UpdateAccount.as_view(), name='account'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='app_users/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='app_users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app_users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='app_users/password_reset_complete.html'), name='password_reset_complete'),
]
