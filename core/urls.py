from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import re_path,path,include
from .import views


app_name = 'core'
urlpatterns = [
    re_path(r'^signup/$', views.Signup.as_view(), name='core-signup'),
    re_path(r'^signup/verify/$', views.SignupVerify.as_view(),
         name='core-signup-verify'),
    re_path(r'signup/resend/verification/link/$',views.ResendVerificationLink.as_view(),
        name="core-signup-resend-verification-link"
        ),

    re_path(r'^login/$', views.Login.as_view(), name='core-login'),
    re_path(r'^refresh/$',TokenRefreshView.as_view(), name='core-refresh'),
    re_path(r'^logout/$', views.Logout.as_view(), name='core-logout'),

    re_path(r'^password/reset/$', views.PasswordReset.as_view(),
         name='core-password-reset'),
    re_path(r'^password/reset/verify/$', views.PasswordResetVerify.as_view(),
         name='core-password-reset-verify'),
    re_path(r'^password/reset/verified/', views.PasswordResetVerified.as_view(),
         name='core-password-reset-verified'),

    re_path(r'^email/change/$', views.EmailChange.as_view(),
         name='core-email-change'),
    re_path(r'^email/change/verify/$', views.EmailChangeVerify.as_view(),
         name='core-email-change-verify'),

    re_path(r'^password/change/$', views.PasswordChange.as_view(),
         name='core-password-change'),

    re_path(r'^users/me/$', views.UserMe.as_view(), name='core-me'),
]