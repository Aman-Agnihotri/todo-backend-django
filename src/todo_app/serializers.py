from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Todo
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class TodoSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    title = serializers.CharField(max_length=100, required=False)
    
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'completed', 
                 'created_at', 'updated_at', 'due_date', 
                 'priority', 'status')
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'title': {'required': False}
        }

    def get_status(self, obj):
        if (obj.completed):
            return "completed"
        if (obj.due_date and obj.due_date < timezone.now()):
            return "overdue"
        return "pending"
    
    def validate(self, data):
        if self.instance is None and 'title' not in data:
            raise serializers.ValidationError({'title': 'Title is required.'})
        return data