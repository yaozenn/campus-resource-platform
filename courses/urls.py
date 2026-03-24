from django.urls import path
from . import views

urlpatterns = [
    path('types/', views.ResourceTypeListView.as_view(), name='resource_type_list'),
    path('types/manage/', views.ResourceTypeManageView.as_view(), name='resource_type_manage'),
    path('types/delete/<int:pk>/', views.ResourceTypeDeleteView.as_view(), name='resource_type_delete'),
    path('', views.ResourceListView.as_view(), name='resource_list'),
    path('create/', views.ResourceCreateView.as_view(), name='resource_create'),
    path('teacher/', views.TeacherResourceListView.as_view(), name='teacher_resource_list'),
    path('pending/', views.PendingResourceListView.as_view(), name='pending_resource_list'),
    path('<int:pk>/', views.ResourceDetailView.as_view(), name='resource_detail'),
    path('<int:pk>/update/', views.ResourceUpdateView.as_view(), name='resource_update'),
    path('<int:pk>/delete/', views.ResourceDeleteView.as_view(), name='resource_delete'),
    path('<int:pk>/approve/', views.ResourceApproveView.as_view(), name='resource_approve'),
    path('<int:pk>/comments/', views.ResourceCommentView.as_view(), name='resource_comments'),
    path('<int:pk>/comment-reply/', views.comment_reply, name='comment_reply'),
    path('collect/', views.ResourceCollectView.as_view(), name='resource_collect'),
    path('uncollect/<int:pk>/', views.ResourceUncollectView.as_view(), name='resource_uncollect'),
    path('collections/', views.CollectionListView.as_view(), name='collection_list'),
    path('<int:pk>/download/', views.ResourceDownloadView.as_view(), name='resource_download'),
    path('comments/', views.CommentListView.as_view(), name='comment_list'),
]