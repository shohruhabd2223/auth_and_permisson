from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app.views.product import (ProductListCreateAPIView, ProductDestroyAPIView,
                               ProductUpdateAPIView)
from app.views.auth import RegisterView, ResendCodeView, VerifyEmailView
from app.views.forgot_password import ForgotPasswordView, ConfirmPasswordView, ResetPasswordView

schema_view = get_schema_view(
    openapi.Info(
        title="Student API",
        default_version='v1',
        description="Student CRUD API hujjati",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('products/', ProductListCreateAPIView.as_view(), name='list-and-create'),
    # path('create/', ProductCreateAPIView.as_view(), name="create"),
    path('delete/<int:pk>/', ProductDestroyAPIView.as_view(), name="delete"),
    path('update/<int:pk>/', ProductUpdateAPIView.as_view(), name="update"),

    path("user/register/", RegisterView.as_view()),
    path("user/verify-email/", VerifyEmailView.as_view()),
    path("user/resend-code/", ResendCodeView.as_view()),
    path("user/login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("forgot/forgot-password/", ForgotPasswordView.as_view()),
    path("forgot/confirm-password/", ConfirmPasswordView.as_view()),
    path("forgot/reset-password/", ResetPasswordView.as_view()),
    # path("me/", MeView.as_view()),

]