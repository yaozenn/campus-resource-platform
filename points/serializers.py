from rest_framework import serializers
from .models import PointRecord, Prize, PrizeExchange

class PointRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointRecord
        fields = '__all__'

class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = '__all__'

class PrizeExchangeSerializer(serializers.ModelSerializer):
    prize_name = serializers.CharField(source='prize.name', read_only=True)
    class Meta:
        model = PrizeExchange
        fields = '__all__'