from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password

from photos.models import ImageModel
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .models import PasswordResetOTP

User = get_user_model()


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('photos:home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    photos = user.photos.all()
    # print(f'photos count: {photos.count()}')
    context = {
        'profile_user': user,
        'photos': photos,
        'photo_count': photos.count(),
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Handle profile photo upload
            profile_photo = request.FILES.get('profile_photo')
            if profile_photo:
                # Delete old profile photo if it exists
                if user.profile_photo:
                    user.profile_photo.delete()
                
                # Create new ImageModel for profile photo
                profile_image = ImageModel.objects.create(
                    title=f"Profile photo for {user.username}",
                    path='profile_photos',
                    file=profile_photo
                )
                user.profile_photo = profile_image
            
            user.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile', username=request.user.username)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})


def password_reset_request(request):
    """Step 1: Request OTP by entering email"""
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate OTP
            otp = PasswordResetOTP.generate_otp(user)
            
            # Send email with OTP
            subject = 'PhotoShare - Password Reset OTP'
            message = f"""Hi {user.username},

You requested to reset your password for your PhotoShare account.

Your OTP code is: {otp.otp_code}

This code will expire in 15 minutes.

If you didn't request this, please ignore this email.

Thanks,
The PhotoShare Team"""
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            # Store email in session for next step
            request.session['reset_email'] = email
            messages.success(request, f'OTP code has been sent to {email}')
            return redirect('accounts:password_reset_verify')
            
        except User.DoesNotExist:
            # Don't reveal that the email doesn't exist (security)
            messages.success(request, 'If an account exists with that email, an OTP has been sent.')
            return redirect('accounts:password_reset_verify')
    
    return render(request, 'registration/password_reset_request.html')


def password_reset_verify(request):
    """Step 2: Verify OTP and set new password"""
    email = request.session.get('reset_email')
    if not email:
        messages.error(request, 'Please request a password reset first.')
        return redirect('accounts:password_reset_request')
    
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate passwords match
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'registration/password_reset_verify.html', {'email': email})
        
        # Validate password length
        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'registration/password_reset_verify.html', {'email': email})
        
        try:
            user = User.objects.get(email=email)
            # Find valid OTP
            otp = PasswordResetOTP.objects.filter(
                user=user,
                otp_code=otp_code,
                is_used=False
            ).first()
            
            if otp and otp.is_valid():
                # Update password
                user.password = make_password(new_password)
                user.save()
                
                # Mark OTP as used
                otp.mark_used()
                
                # Clear session
                if 'reset_email' in request.session:
                    del request.session['reset_email']
                
                messages.success(request, 'Password reset successful! You can now login with your new password.')
                return redirect('accounts:login')
            else:
                messages.error(request, 'Invalid or expired OTP code. Please try again.')
                
        except User.DoesNotExist:
            messages.error(request, 'An error occurred. Please try again.')
    
    return render(request, 'registration/password_reset_verify.html', {'email': email})
