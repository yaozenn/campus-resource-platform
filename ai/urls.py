from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat, name='ai_chat'),
    path('teacher-insight/', views.teacher_insight, name='teacher_insight'),
]