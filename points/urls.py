from django.urls import path
from . import views

urlpatterns = [
    path('', views.PointRecordListView.as_view(), name='points_record_list'),
    path('user/', views.UserPointsView.as_view(), name='user_points'),
    path('prizes/', views.PrizeListView.as_view(), name='prize_list'),
    path('exchange/', views.PrizeExchangeView.as_view(), name='prize_exchange'),
    path('my-exchanges/', views.MyExchangesView.as_view(), name='my_exchanges'),
    path('all-exchanges/', views.AllExchangesView.as_view(), name='all_exchanges'),
    path('approve/<int:pk>/', views.ExchangeApproveView.as_view(), name='exchange_approve'),
    path('manage/', views.PrizeManageView.as_view(), name='prize_manage'),
    path('manage/<int:pk>/', views.PrizeUpdateView.as_view(), name='prize_update'),
    path('delete/<int:pk>/', views.PrizeDeleteView.as_view(), name='prize_delete'),
    # 签到相关
    path('checkin/status/', views.CheckInStatusView.as_view(), name='checkin_status'),
    path('checkin/', views.CheckInView.as_view(), name='checkin'),
]