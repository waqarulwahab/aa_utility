from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTP, PasswordResetToken

# Register your models here.

class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the CustomUser model.
    """
    list_display = ('email', 'username', 'is_email_verified', 'date_joined', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined',)
    ordering = ('-date_joined',)
    list_filter = ('is_staff', 'is_superuser', 'is_email_verified')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Status', {'fields': ('is_email_verified',)}),
        ('Personal', {'fields': ('profile_picture',)}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active', 'is_email_verified')}
        ),
    )


class OTPAdmin(admin.ModelAdmin):
    """
    Admin configuration for the OTP model.
    """
    list_display = ('user', 'otp_code', 'created_at', 'expires_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


class PasswordResetTokenAdmin(admin.ModelAdmin):
    """
    Admin configuration for the PasswordResetToken model.
    """
    list_display = ('user', 'created_at', 'expires_at')
    search_fields = ('user__email', 'user__username')
    readonly_fields = ('created_at', 'token')
    ordering = ('-created_at',)


# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP, OTPAdmin)
admin.site.register(PasswordResetToken, PasswordResetTokenAdmin)
