import logging

from django.contrib.auth import logout
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import ChangePasswordSerializer, RegisterSerializer

logger = logging.getLogger('user_app')


class RegisterView(generics.CreateAPIView):
    """
    An API endpoint for user registration.
    """
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class ChangePasswordView(generics.UpdateAPIView):
    """
    An API endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def update(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        data = serializer.data
        # Check old password
        if not instance.check_password(data["old_password"]):
            return Response({"message": "Wrong password."}, status=status.HTTP_400_BAD_REQUEST)
        elif data['password'] != data['password2']:
            return Response({"message": "Password fields didn't match."}, status=status.HTTP_400_BAD_REQUEST)
        elif data['old_password'] == data['password']:
            return Response({"message": "Old Password and new password should not be same."},
                            status=status.HTTP_400_BAD_REQUEST)
        # set_password also hashes the password that the user will get
        instance.set_password(data["password"])
        instance.save()
        return Response({'message': "Password updated successfully."}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    An API endpoint for logout
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        logout(request)
        refresh_token = request.data.get("refresh_token", None)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': "Logout successfully."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f"Error in {request.resolver_match.view_name}, error: {e}")
            if "Token is blacklisted" in str(e):
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
