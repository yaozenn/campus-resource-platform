from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import PointRecord, Prize, PrizeExchange, CheckInRecord
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

# 签到相关视图
class CheckInStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        has_signed = CheckInRecord.objects.filter(user=request.user, checkin_date=today).exists()
        return Response({'has_signed': has_signed})

class CheckInView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        today = timezone.now().date()
        
        # 检查今天是否已经签到过
        if CheckInRecord.objects.filter(user=request.user, checkin_date=today).exists():
            return Response({'error': '今日已签到'}, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建签到记录
        CheckInRecord.objects.create(user=request.user, checkin_date=today)
        
        # 增加积分
        user = request.user
        if user.role == 'student':
            user.add_points(5, 'checkin', '每日签到奖励')
        
        return Response({
            'success': True,
            'points': user.points,
            'points_added': 5,
            'message': '签到成功！积分 +5'
        })