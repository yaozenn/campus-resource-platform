# 覆盖 courses/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('types/', views.ResourceTypeListView.as_view(), name='resource_type_list'),
    path('types/manage/', views.ResourceTypeManageView.as_view(), name='resource_type_manage'),
    path('types/<int:pk>/delete/', views.ResourceTypeDeleteView.as_view(), name='resource_type_delete'),
    
    path('', views.ResourceListView.as_view(), name='resource_list'),
    path('create/', views.ResourceCreateView.as_view(), name='resource_create'),
    path('pending/', views.PendingResourceListView.as_view(), name='pending_resources'),
    path('teacher/', views.TeacherResourceListView.as_view(), name='teacher_resources'),
    
    path('<int:pk>/', views.ResourceDetailView.as_view(), name='resource_detail'),
    path('<int:pk>/update/', views.ResourceUpdateView.as_view(), name='resource_update'),
    path('<int:pk>/delete/', views.ResourceDeleteView.as_view(), name='resource_delete'),
    path('<int:pk>/approve/', views.ResourceApproveView.as_view(), name='resource_approve'),
    path('<int:pk>/status/', views.ResourceStatusUpdateView.as_view(), name='resource_status_update'),
    path('<int:pk>/download/', views.ResourceDownloadView.as_view(), name='resource_download'),
    path('<int:pk>/comments/', views.ResourceCommentView.as_view(), name='resource_comments'),
    path('<int:pk>/reply/', views.comment_reply, name='comment_reply'),
    path('<int:pk>/report/', views.ResourceReportView.as_view(), name='resource_report'),
    path('<int:pk>/rate/', views.resource_rate, name='resource_rate'),
    
    path('collections/', views.CollectionListView.as_view(), name='collection_list'),
    path('collect/', views.CollectionCreateView.as_view(), name='collection_create'), # 新增
    path('uncollect/<int:pk>/', views.CollectionDeleteView.as_view(), name='collection_delete'), # 新增
]