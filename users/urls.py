from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('teachers/', views.TeacherListView.as_view(), name='teacher_list'),
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
]
