from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomTokenObtainPairSerializer, RegisterSerializer, UserUpdateSerializer, \
    ModeraterCreateSerializer, ModeratorUpdateSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .models import User
from .permissions import IsAdminRole, IsModeratorRole
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
import os
from django.conf import settings
from django.core.files.storage import default_storage
from uuid import uuid4


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'phone_number': user.phone_number,
                    'username': user.username
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def put(self, request, username):
        user = self.get_object(username)
        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        if User.objects.filter(username=request.data.get('username', '')).exists():
            return Response({'message': "bunday user bor"})
        # Ma'lumotlarni yangilash
        user.username = request.data.get('username', user.username)
        user.phone_number = request.data.get('phone_number', user.phone_number)

        # Agar parol yuborilgan bo‘lsa
        password = request.data.get('password')
        if password:
            user.set_password(password)

        images = request.FILES.getlist('images')
        image_urls = []

        if images:
            user_folder = f'user_images/user_{user.pk}'
            os.makedirs(os.path.join(settings.MEDIA_ROOT, user_folder), exist_ok=True)

            for img in images:
                filename = f"{uuid4().hex}_{img.name}"
                path = os.path.join(user_folder, filename)
                full_path = os.path.join(settings.MEDIA_ROOT, path)

                with default_storage.open(path, 'wb+') as destination:
                    for chunk in img.chunks():
                        destination.write(chunk)

                image_urls.append(f"{settings.MEDIA_URL}{path}")

            # Rasm yo‘lini saqlash (birinchi rasm yoki hammasi vergul bilan)
            user.image_path = ','.join(image_urls)

        user.save()

        return Response({
            "message": "User updated successfully",
            "username": user.username,
            "phone_number": user.phone_number,
            "image_paths": image_urls
        }, status=status.HTTP_200_OK)


class CustomTokenObtainView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': "Protected API!", "user": request.user.username})


class GatUserDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_id = user.id
        user_role = user.role
        username = user.username
        image = user.image if user.image and hasattr(user.image, 'url') else None
        return Response({
            "user_id": user_id,
            "role": user_role,
            "username": username,
            "image_path": image
        })


class CreateModeratorUser(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request):
        user = request.user.id
        print(user)
        serializer = ModeraterCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            data = serializer.validated_data
            data['created_by_id'] = user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateModeratorUser(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def put(self, request):
        try:
            user = User.objects.get(phone_number=request.data['phone_number'])
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ModeratorUpdateSerializers(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save(role='moderator')
            return Response({'message': 'User change to moderator!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
