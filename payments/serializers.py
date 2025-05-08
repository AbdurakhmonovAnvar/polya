from rest_framework import serializers
from .models import Payment


class CreatePaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        return Payment.objects.create(**validated_data)


class GetMyPaymentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'



class GetMyLastPaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'