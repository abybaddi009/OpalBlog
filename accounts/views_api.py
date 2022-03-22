from django.contrib.auth import get_user_model, login


from rest_framework import generics, permissions
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import UserSerializer, UserRegisterSerializer


User = get_user_model()


class UserRegisterApi(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny,]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "User Created Successfully. Now perform Login to get your token",
            }
        )


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()