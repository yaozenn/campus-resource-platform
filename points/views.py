from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import PointsRecord, Prize, PrizeExchange
from .serializers import PointsRecordSerializer, PrizeSerializer, PrizeExchangeSerializer, PrizeExchangeCreateSerializer
from users.models import User

class PointsRecordListView(generics.ListAPIView):
    queryset = PointsRecord.objects.all()
    serializer_class = PointsRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserPointsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        records = PointsRecord.objects.filter(user=user)
        serializer = PointsRecordSerializer(records, many=True)
        return Response({
            'total_points': user.points,
            'records': serializer.data
        })

class PrizeListView(generics.ListAPIView):
    queryset = Prize.objects.filter(is_active=True)
    serializer_class = PrizeSerializer
    permission_classes = [permissions.AllowAny]

class PrizeExchangeView(generics.CreateAPIView):
    serializer_class = PrizeExchangeCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        prize_id = request.data.get('prize')
        
        try:
            prize = Prize.objects.get(id=prize_id, is_active=True)
        except Prize.DoesNotExist:
            return Response({'error': '奖品不存在'}, status=400)
        
        if prize.stock <= 0:
            return Response({'error': '奖品库存不足'}, status=400)
        
        if user.points < prize.points_required:
            return Response({'error': '积分不足'}, status=400)
        
        user.points -= prize.points_required
        user.save()
        
        prize.stock -= 1
        prize.save()
        
        exchange = PrizeExchange.objects.create(
            user=user,
            prize=prize,
            points_spent=prize.points_required,
            status='pending'
        )
        
        PointsRecord.objects.create(
            user=user,
            type='deduct',
            points=prize.points_required,
            reason=f'兑换奖品: {prize.name}'
        )
        
        return Response(PrizeExchangeSerializer(exchange).data)

class MyExchangesView(generics.ListAPIView):
    serializer_class = PrizeExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PrizeExchange.objects.filter(user=self.request.user)

class AllExchangesView(generics.ListAPIView):
    queryset = PrizeExchange.objects.all()
    serializer_class = PrizeExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExchangeApproveView(generics.UpdateAPIView):
    queryset = PrizeExchange.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        exchange = self.get_object()
        action = request.data.get('action')
        
        if action == 'approve':
            exchange.status = 'approved'
        elif action == 'reject':
            exchange.status = 'rejected'
            exchange.user.points += exchange.points_spent
            exchange.user.save()
            exchange.prize.stock += 1
            exchange.prize.save()
        
        exchange.save()
        return Response(PrizeExchangeSerializer(exchange).data)

class PrizeManageView(generics.ListCreateAPIView):
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PrizeDeleteView(generics.DestroyAPIView):
    queryset = Prize.objects.all()
    permission_classes = [permissions.IsAuthenticated]
