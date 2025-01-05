from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'completed', 'priority', 'due_date', 'created_at')
    list_filter = ('completed', 'priority', 'created_at', 'due_date')
    search_fields = ('title', 'description', 'user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
        ('Status', {
            'fields': ('completed', 'priority', 'due_date')
        }),
        ('User Info', {
            'fields': ('user',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)