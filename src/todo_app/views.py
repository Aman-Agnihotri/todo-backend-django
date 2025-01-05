from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from django.db.models import Q
from .models import Todo
from .serializers import TodoSerializer, UserSerializer

class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'due_date', 'priority']

    def get_queryset(self):
        queryset = Todo.objects.filter(user=self.request.user)
        status = self.request.query_params.get('status', None)
        
        if status:
            if status == 'completed':
                queryset = queryset.filter(completed=True)
            elif status == 'pending':
                queryset = queryset.filter(completed=False)
            elif status == 'overdue':
                queryset = queryset.filter(
                    completed=False,
                    due_date__lt=timezone.now()
                )

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        todos = self.get_queryset()
        return Response({
            'total': todos.count(),
            'completed': todos.filter(completed=True).count(),
            'pending': todos.filter(completed=False).count(),
            'overdue': todos.filter(
                completed=False,
                due_date__lt=timezone.now()
            ).count()
        })

    @action(detail=False, methods=['delete'])
    def clear_completed(self, request):
        todos = self.get_queryset().filter(completed=True)
        count = todos.count()
        todos.delete()
        return Response({
            'message': f'Deleted {count} completed todos'
        })

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Add password explicitly
        user_model = get_user_model()
        user = user_model.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data.get('email', ''),
            password=request.data['password']
        )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
