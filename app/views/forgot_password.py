from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.models import User
from app.serializers.forgot_password import ForgotPasswordSerializer, ConfirmPasswordSerializer, ResetPasswordSerializer
from app.services import send_verification_code, confirm_code, finish_code
from app.services.pre_token import make_pre_token, get_user


class ForgotPasswordView(generics.GenericAPIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        user = User.objects.filter(email=email, is_active=True).first()
        if user:
            send_verification_code(user)   # register'dagi funksiya

        # email yo'q bo'lsa ham javob bir xil (user_id=0)
        user_id = user.id if user else 0
        return Response({"pre_token": make_pre_token(user_id)})


class ConfirmPasswordView(generics.GenericAPIView):
    serializer_class = ConfirmPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = get_user(data["pre_token"])
        confirm_code(user, data["code"])
        return Response({"detail": "Kod to'g'ri. Yangi parol kiriting."})

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = get_user(data["pre_token"])
        finish_code(user)
        user.set_password(data["new_password"])
        user.save()
        return Response({"detail": "Parol yangilandi."})
