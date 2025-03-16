from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import random
import string
import datetime

# Create your models here.

class CustomUser(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    
    Adds email verification functionality and other custom fields.
    """
    email = models.EmailField(_('email address'), unique=True)
    is_email_verified = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics', null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.email


class OTP(models.Model):
    """
    Model to store OTP (One-Time Password) for email verification.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"OTP for {self.user.email}"
    
    def save(self, *args, **kwargs):
        # Set expiration time to 10 minutes from creation
        if not self.pk:  # Only on creation
            self.expires_at = timezone.now() + datetime.timedelta(minutes=10)
        super().save(*args, **kwargs)
    
    @classmethod
    def generate_otp(cls, user):
        """Generate a new OTP for the user."""
        # Delete any existing OTP
        cls.objects.filter(user=user).delete()
        
        # Generate a 6-digit OTP
        otp_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Print the OTP clearly for development purposes
        print("\n\n========== OTP INFORMATION ==========")
        print(f"USER: {user.email}")
        print(f"OTP CODE: {otp_code}")
        print("======================================\n\n")
        
        # Create a new OTP object
        otp = cls.objects.create(
            user=user,
            otp_code=otp_code,
        )
        
        return otp_code
    
    @classmethod
    def verify_otp(cls, user, otp_code):
        """
        Verify if OTP is valid for the given user.
        
        Args:
            user: CustomUser instance
            otp_code: String containing the OTP to verify
            
        Returns:
            Boolean: True if valid, False otherwise
        """
        try:
            otp = cls.objects.get(
                user=user,
                otp_code=otp_code,
                expires_at__gt=timezone.now()
            )
            # OTP is valid
            return True
        except cls.DoesNotExist:
            # OTP is invalid or expired
            return False


class PasswordResetToken(models.Model):
    """
    Model to store password reset tokens.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f"Password reset token for {self.user.email}"
    
    def save(self, *args, **kwargs):
        # Set expiration time to 24 hours from creation
        if not self.pk:  # Only on creation
            self.expires_at = timezone.now() + datetime.timedelta(hours=24)
        super().save(*args, **kwargs)
    
    @classmethod
    def generate_token(cls, user):
        """
        Generate a new password reset token for the given user.
        
        Args:
            user: CustomUser instance
            
        Returns:
            Token string
        """
        # Delete any existing tokens for this user
        cls.objects.filter(user=user).delete()
        
        # Generate a random token
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=64))
        
        # Create new token object
        token_obj = cls.objects.create(
            user=user,
            token=token,
        )
        
        return token
    
    @classmethod
    def validate_token(cls, token):
        """
        Validate a password reset token.
        
        Args:
            token: String containing the token to validate
            
        Returns:
            User instance if valid, None otherwise
        """
        try:
            token_obj = cls.objects.get(
                token=token,
                expires_at__gt=timezone.now()
            )
            return token_obj.user
        except cls.DoesNotExist:
            return None
