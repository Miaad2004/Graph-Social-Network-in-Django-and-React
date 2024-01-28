from django.apps import AppConfig
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .apps import ApiConfig
from .models import Connection

from .models import CustomUser
from .serializers import UserSerializer, ConnectionSerializer
from rest_framework import status

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        print("Request Data:", request.data) 
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError as e:
            return Response({'error': f'Missing key: {e}'}, status=400)

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            return Response({'token': token.key, 'user': serializer.data}, status=200)
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        token_key = request.auth.key
        token = Token.objects.get(key=token_key)
        token.delete()

        return Response({'detail': 'Successfully logged out.'})

class UserDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=status.HTTP_200_OK)

class GetAllUsersView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

class AddConnectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConnectionSerializer  

    def post(self, request):
        try:
            username = request.data['username']

        except KeyError as e:
            return Response({'error': f'Missing key: {e}'}, status=400)
        
        user_name = request.data['username']

        try:
            user2 = CustomUser.objects.get(username=user_name)
        except ObjectDoesNotExist:
            return Response({'message': f'username does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if Connection.objects.filter(user1=request.user, user2=user2).exists() or \
                Connection.objects.filter(user1=user2, user2=request.user).exists():
            return Response({'message': 'Users are already connected.'}, status=status.HTTP_400_BAD_REQUEST)

        connection = Connection.objects.create(user1=request.user, user2=user2)

        serializer = self.serializer_class(connection)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RemoveConnectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            username = request.data['username']

        except KeyError as e:
            return Response({'error': f'Missing key: {e}'}, status=400)
        
        user_name = request.data['username']

        try:
            user2 = CustomUser.objects.get(username=user_name)
            
        except ObjectDoesNotExist:
            return Response({'message': f'username does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        connection1 = Connection.objects.filter(user1=request.user, user2=user2)
        connection2 = Connection.objects.filter(user1=user2, user2=request.user)

        if not (connection1.exists() or connection2.exists()):
            return Response({'message': 'Connection does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        connection1.delete()
        connection2.delete()

        return Response({'message': 'Connection removed successfully.'}, status=status.HTTP_200_OK)

class GetAllConnectionsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConnectionSerializer

    def get_queryset(self):
        global_graph = ApiConfig.global_graph
        print(global_graph)
        user = self.request.user
        queryset = Connection.objects.filter(user1=user) | Connection.objects.filter(user2=user)
        return queryset

class GetSuggestionsView(generics.CreateAPIView):
    pass