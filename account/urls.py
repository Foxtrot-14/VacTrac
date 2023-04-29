from django.urls import path
from account.views import *
urlpatterns = [
    path('register/', RegistrationView.as_view(),name='register'),
    path('login/', LoginView.as_view(),name='login'),
    path('profile/', ProfileView.as_view(),name='profile'),
    path('change-password/', ChangePasswordView.as_view(),name='passwordchange'),
    path('forgot-password/', PasswordResetPhoneView.as_view(),name='passwordresetemail'),
    path('otp-verification/', OtpVerificationView.as_view(),name='otpverify'),
    path('reset-password/<uid>/<token>/',UserPasswordResetView.as_view(),name='resetpassword'),
]