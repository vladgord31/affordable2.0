from django.urls import path
from users import views as user_views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

app_name = "users"

urlpatterns = [
    path("signin/", user_views.UserSigninView.as_view(), name="signin"),
    path("signup/", user_views.UserSignupView.as_view(), name="signup"),
    path("forgot/", user_views.UserForgotView.as_view(), name="forgot"),
    path("profile/", user_views.UserProfileView.as_view(), name="profile"),
    path("password-reset/", PasswordResetView.as_view(template_name='users/password_reset_form.html'), name="password_reset"),
    path("password-reset/done/", PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name="password_reset_done"),
    path('password-reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("reset/done/", PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name="password_reset_complete"),
    path("logout/", user_views.UserSignoutView.as_view(), name="logout"),
]
