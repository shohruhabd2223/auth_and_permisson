from tokenize import TokenError

from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView, GenericAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from app.models import User, EmailCode
from app.serializers import RegisterModelSerializer, LogoutModelSerializer, VerifyEmailSerializer
from app.services import send_verification_code


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterModelSerializer
    permission_classes = [AllowAny]


    def perform_create(self, serializer):
        user = serializer.save()
        send_verification_code(user)




class VerifyEmailView(GenericAPIView):
    serializer_class = VerifyEmailSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(
            email=serializer.validated_data["email"], is_active=False
        ).first()
        record = EmailCode.objects.filter(user=user).first()

        if record is None or record.is_expired():
            return Response({"detail": "Kod topilmadi yoki muddati tugagan"}, status=400)

        if record.attempts >= EmailCode.MAX_ATTEMPTS:
            return Response({"detail": "Urinishlar tugadi, yangi kod so'rang"}, status=400)

        if record.code != serializer.validated_data["code"]:
            record.attempts += 1
            record.save()
            return Response({"detail": "Kod noto'g'ri"}, status=400)

        user.is_active = True
        user.save()
        record.delete()
        return Response({"detail": "Email tasdiqlandi. Endi login qiling."})


class LogoutGenericAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutModelSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            RefreshToken(serializer.validated_data["refresh"]).blacklist()
        except TokenError:
            return Response({"detail": "Token yaroqsiz"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_205_RESET_CONTENT)



