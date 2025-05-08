from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username already exist!")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password','image')

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['id'] = user.phone_number
        token['role'] = user.role
        return token


class ModeraterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password')


    def create(self, validated_data):
        created_by_id = self.context['request'].user.id
        user = User.objects.create_user(
        phone_number=validated_data['phone_number'],
        created_by_id = created_by_id,
        password= '55555',
        role= 'moderator')
        return user



class ModeratorUpdateSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone_number','created_by_id')

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user:
            instance.created_by = request.user
        return super().update(instance, validated_data)



