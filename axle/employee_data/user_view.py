from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics
from rest_framework import status


# Class based view to Get User Details using Token Authentication
class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        username = request.data['username']
        user = User.objects.filter(username=username).first()
        if not user:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user = serializer.instance
            resp_data = {'data': serializer.data, 'code': '100', 'msg': 'New User created.'}
        else:
            user_data = {"username": user.username, "email": user.email, "first_name": user.first_name,
                         "last_name": user.last_name}
            resp_data = {'data': user_data, 'code': '100', 'msg': 'User already present.'}
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            pass
        else:
            token.delete()
        finally:
            token = Token.objects.create(user=user)

        resp_data['data']['token'] = str(token)
        return Response(data=resp_data, status=status.HTTP_201_CREATED)
