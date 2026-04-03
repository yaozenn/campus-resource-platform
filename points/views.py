from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import PointRecord, Prize, PrizeExchange
from .serializers import PointRecordSerializer, PrizeSerializer, PrizeExchangeSerializer

# 1. 积分流水列表
class PointRecordListView(generics.ListAPIView):
    serializer_class = PointRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PointRecord.objects.filter(user=self.request.user)

# 2. 用户当前积分概览
class UserPointsView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            'username': request.user.username,
            'points': request.user.points or 0
        })

# 3. 奖品列表（公开）
class PrizeListView(generics.ListAPIView):
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer
    permission_classes = [permissions.AllowAny]

# 4. 提交兑换申请
class PrizeExchangeView(generics.CreateAPIView):
    serializer_class = PrizeExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        prize_id = request.data.get('prize')
        try:
            prize = Prize.objects.get(id=prize_id)
        except Prize.DoesNotExist:
            return Response({'error': '奖品不存在'}, status=404)

        user = request.user
        if user.points < prize.points_required:
            return Response({'error': '积分不足'}, status=400)
        
        if prize.stock <= 0:
            return Response({'error': '库存不足'}, status=400)

        # 扣分并记流水
        user.add_points(-prize.points_required, 'exchange', f"兑换奖品：{prize.name}")
        
        prize.stock -= 1
        prize.save()

        exchange = PrizeExchange.objects.create(user=user, prize=prize)
        return Response(PrizeExchangeSerializer(exchange).data, status=201)

# 5. 我的兑换记录
class MyExchangesView(generics.ListAPIView):
    serializer_class = PrizeExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PrizeExchange.objects.filter(user=self.request.user)

# 6. 管理员：所有兑换记录
class AllExchangesView(generics.ListAPIView):
    queryset = PrizeExchange.objects.all()
    serializer_class = PrizeExchangeSerializer
    permission_classes = [permissions.IsAuthenticated] # 实际应配合IsAdminUser

# 7. 管理员：审批兑换
class ExchangeApproveView(generics.UpdateAPIView):
    queryset = PrizeExchange.objects.all()
    serializer_class = PrizeExchangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        exchange = self.get_object()
        exchange.status = request.data.get('status', 'completed')
        exchange.save()
        return Response(PrizeExchangeSerializer(exchange).data)

# 8. 管理员：奖品管理（增删改）
class PrizeManageView(generics.ListCreateAPIView):
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PrizeUpdateView(generics.UpdateAPIView):
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PrizeDeleteView(generics.DestroyAPIView):
    queryset = Prize.objects.all()
    serializer_class = PrizeSerializer
    permission_classes = [permissions.IsAuthenticated]