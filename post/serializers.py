from rest_framework import serializers
from .models import Polya


class PolyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polya
        fields = ('address', 'locations')

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        return Polya.objects.create(creator=user, **validated_data)


class PolyaUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polya
        fields = ('address', 'locations')

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.locations = validated_data.get('locations', instance.locations)
        instance.save()
        return instance


class PolyaGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polya
        fields = ['address', 'locations', 'owner']


class GetAllPolyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polya
        fields = ['address', 'locations', 'owner']


class GetPolyaByIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polya
        fields = ['address', 'locations', 'owner']


class GetMyLastReversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Polya
        fields = '__all__'

