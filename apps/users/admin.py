from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAccountAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('id', 'username', 'email', 'password')}),
        ('Personal info', {
         'fields': ('first_name', 'last_name', 'avatar', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('username', 'email',)
    ordering = ('username',)
    readonly_fields = ('id',)


admin.site.register(User, UserAccountAdmin)
