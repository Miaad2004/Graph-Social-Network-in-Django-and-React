from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from .apps import ApiConfig
from .models import Connection, CustomUser
from .serializers import UserLoginSerializer, UserSerializer, ConnectionSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        try:
            user = serializer.save()
            return Response(status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_200_OK)


class UserLoginView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            auth_serializer = self.serializer_class(data=request.data,
                                                    context={'request': request})
            
            auth_serializer.is_valid(raise_exception=True)
            user = auth_serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({'token': token.key, 'error': None}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'token': None, 'error': str(e)}, status=status.HTTP_200_OK)


class GetUserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            username = request.data.get('username')
            
            if username == None:
                 return Response({'connection': None, 'error': 'Username is required.'}, status=status.HTTP_200_OK)

            try:
                user = CustomUser.objects.get(username=username)
                
            except CustomUser.DoesNotExist:
                return Response({'connection': None, 'error': 'User does not exist.'}, status=status.HTTP_200_OK)
            
            return Response({'user': user, 'error': None}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_200_OK)


class GetCurrentUserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({'user': serializer.data, 'error': None}, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'error': None}, status=status.HTTP_200_OK)


class UserDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        serializer = UserSerializer(user)
        serializer.delete(user)
        return Response({'error':None}, status=status.HTTP_200_OK)


class GetAllUsersView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny] 
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


class AddConnectionView(APIView):
    permission_classes = [permissions.IsAuthenticated] 

    def post(self, request):
        try:
            username = request.data.get('username')
            
            if username == None:
                 return Response({'connection': None, 'error': 'Username is required.'}, status=status.HTTP_200_OK)

            user1 = request.user
            try:
                user2 = CustomUser.objects.get(username=username)
                
            except CustomUser.DoesNotExist:
                return Response({'connection': None, 'error': 'User does not exist.'}, status=status.HTTP_200_OK)

            if Connection.objects.filter(user1=user1, user2=user2).exists() or \
               Connection.objects.filter(user1=user2, user2=user1).exists():
                return Response({'connection': None, 'error': 'Users are already connected.'}, status=status.HTTP_200_OK)

            connection = Connection.objects.create(user1=user1, user2=user2)
            return Response({'connection': connection.id, 'error': None}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'connection': None, 'error': str(e)}, status=status.HTTP_200_OK)


class RemoveConnectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            username = request.data.get('username')
            user2 = CustomUser.objects.get(username=username)

            connection1 = Connection.objects.filter(user1=request.user, user2=user2)
            connection2 = Connection.objects.filter(user1=user2, user2=request.user)

            if not (connection1.exists() or connection2.exists()):
                raise Exception('Connection does not exist.')

            connection1.delete()
            connection2.delete()

            return Response({'message': 'Connection removed successfully.', 'error':None}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_200_OK)


class GetAllConnectionsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConnectionSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Connection.objects.filter(user1=user) | Connection.objects.filter(user2=user)
        return queryset


class GetSuggestionsView(generics.CreateAPIView):
    pass