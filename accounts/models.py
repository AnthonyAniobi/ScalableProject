from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta
import random
import string

from util.models import ImageModel


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True, default="")
    profile_photo = models.ForeignKey(
        ImageModel, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='profile_user'
    )
    website = models.URLField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username
    
    @property
    def get_profile_photo_url(self):
        """Get profile photo URL or return default"""
        if self.profile_photo and self.profile_photo.file:
            return self.profile_photo.file.url
        return '/static/images/default-avatar.png'  # We'll create this default image


class PasswordResetOTP(models.Model):
    """Model to store OTP codes for password reset"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reset_otps')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"OTP for {self.user.username} - {self.otp_code}"
    
    @classmethod
    def generate_otp(cls, user):
        """Generate a new 6-digit OTP for user"""
        # Delete old unused OTPs for this user
        cls.objects.filter(user=user, is_used=False).delete()
        
        # Generate random 6-digit code
        otp_code = ''.join(random.choices(string.digits, k=6))
        
        # Create new OTP with 15 minute expiration
        otp = cls.objects.create(
            user=user,
            otp_code=otp_code,
            expires_at=timezone.now() + timedelta(minutes=15)
        )
        return otp
    
    def is_valid(self):
        """Check if OTP is still valid"""
        return not self.is_used and timezone.now() < self.expires_at
    
    def mark_used(self):
        """Mark OTP as used"""
        self.is_used = True
        self.save()
    