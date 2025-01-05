from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo_app import views

router = DefaultRouter()
router.register(r'todos', views.TodoViewSet, basename='todo')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
]