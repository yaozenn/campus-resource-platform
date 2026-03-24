from rest_framework import serializers
from .models import PointsRecord, Prize, PrizeExchange
from users.users_serializers import UserSerializer

class PointsRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointsRecord
        fields = '__all__'

class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = '__all__'

class PrizeExchangeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    prize = PrizeSerializer(read_only=True)
    
    class Meta:
        model = PrizeExchange
        fields = '__all__'

class PrizeExchangeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrizeExchange
        fields = ['prize']
