from rest_framework import serializers
from .models import Reservation


class CreateReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['start_time', 'end_time']

    def create(self, validated_data):
        request = self.context.get('request')
        return Reservation.objects.create(**validated_data)


class UpdateReservationSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['start_time', 'end_time']

    def update(self, instance, validated_data):
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.save()
        return instance


class GetMyReservationsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

