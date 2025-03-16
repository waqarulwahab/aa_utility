from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, OTPVerificationForm,
    CustomPasswordResetForm, CustomSetPasswordForm, ProfileUpdateForm
)
from .models import CustomUser, OTP, PasswordResetToken

# Create your views here.

def home_view(request):
    """
    Home page view.
    """
    return render(request, 'user_auth/home.html')


@login_required
def dashboard_view(request):
    """
    Dashboard view for authenticated users.
    """
    return render(request, 'user_auth/dashboard.html')


class SignupView(View):
    """
    View for user registration process.
    """
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'user_auth/signup.html', {'form': form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Create user but don't save yet
            user = form.save(commit=False)
            user.is_active = True  # User is active but email not verified
            user.save()
            
            # Generate OTP
            otp_code = OTP.generate_otp(user)
            
            # Print OTP clearly in terminal for development
            print("\n\n==================================")
            print(f"OTP CODE FOR {user.email}: {otp_code}")
            print("==================================\n\n")
            
            # Send OTP Email
            subject = 'Verify Your Email'
            html_message = render_to_string('user_auth/email/verify_email.html', {
                'user': user,
                'otp_code': otp_code,
            })
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to_email = [user.email]
            
            send_mail(
                subject,
                plain_message,
                from_email,
                to_email,
                html_message=html_message,
                fail_silently=False,
            )
            
            # Redirect to OTP verification page
            request.session['user_email'] = user.email
            messages.success(request, 'Account created! Please verify your email with the OTP sent to your inbox.')
            return redirect('verify_otp')
        
        return render(request, 'user_auth/signup.html', {'form': form})


class OTPVerificationView(View):
    """
    View for OTP verification process.
    """
    def get(self, request):
        # Check if email is in session
        if 'user_email' not in request.session:
            messages.error(request, 'Session expired. Please sign up again.')
            return redirect('signup')
        
        form = OTPVerificationForm()
        return render(request, 'user_auth/verify_otp.html', {'form': form})
    
    def post(self, request):
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp_code']
            user_email = request.session.get('user_email')
            
            try:
                user = CustomUser.objects.get(email=user_email)
                
                # Verify OTP
                if OTP.verify_otp(user, otp_code):
                    # Mark email as verified
                    user.is_email_verified = True
                    user.save()
                    
                    # Delete the OTP
                    OTP.objects.filter(user=user).delete()
                    
                    # Log the user in
                    login(request, user)
                    
                    # Clear session
                    if 'user_email' in request.session:
                        del request.session['user_email']
                    
                    messages.success(request, 'Email verified successfully! Welcome aboard!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid or expired OTP. Please try again.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'User not found. Please sign up again.')
                return redirect('signup')
        
        return render(request, 'user_auth/verify_otp.html', {'form': form})


class ResendOTPView(View):
    """
    View for resending OTP.
    """
    def get(self, request):
        if 'user_email' not in request.session:
            messages.error(request, 'Session expired. Please sign up again.')
            return redirect('signup')
        
        user_email = request.session.get('user_email')
        
        try:
            user = CustomUser.objects.get(email=user_email)
            
            # Generate new OTP
            otp_code = OTP.generate_otp(user)
            
            # Print OTP clearly in terminal for development
            print("\n\n==================================")
            print(f"OTP CODE FOR {user.email}: {otp_code}")
            print("==================================\n\n")
            
            # Send OTP Email
            subject = 'Verify Your Email'
            html_message = render_to_string('user_auth/email/verify_email.html', {
                'user': user,
                'otp_code': otp_code,
            })
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to_email = [user.email]
            
            send_mail(
                subject,
                plain_message,
                from_email,
                to_email,
                html_message=html_message,
                fail_silently=False,
            )
            
            messages.success(request, 'A new OTP has been sent to your email.')
        except CustomUser.DoesNotExist:
            messages.error(request, 'User not found. Please sign up again.')
            return redirect('signup')
        
        return redirect('verify_otp')


class LoginView(View):
    """
    View for user login.
    """
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        
        form = CustomAuthenticationForm()
        return render(request, 'user_auth/login.html', {'form': form})
    
    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                if user.is_email_verified:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.username}!')
                    
                    # Redirect to next parameter if it exists
                    next_page = request.GET.get('next')
                    if next_page:
                        return redirect(next_page)
                    return redirect('dashboard')
                else:
                    # User exists but email not verified
                    request.session['user_email'] = user.email
                    messages.warning(request, 'Please verify your email to login.')
                    return redirect('verify_otp')
            else:
                messages.error(request, 'Invalid email or password.')
        
        return render(request, 'user_auth/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    View for user logout.
    """
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


class PasswordResetRequestView(View):
    """
    View for initiating password reset process.
    """
    def get(self, request):
        form = CustomPasswordResetForm()
        return render(request, 'user_auth/password_reset_request.html', {'form': form})
    
    def post(self, request):
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            try:
                user = CustomUser.objects.get(email=email)
                
                # Generate token
                token = PasswordResetToken.generate_token(user)
                
                # Build reset URL
                reset_url = request.build_absolute_uri(
                    reverse('password_reset_confirm', kwargs={'token': token})
                )
                
                # Send password reset email
                subject = 'Password Reset Request'
                html_message = render_to_string('user_auth/email/password_reset.html', {
                    'user': user,
                    'reset_url': reset_url,
                })
                plain_message = strip_tags(html_message)
                from_email = settings.EMAIL_HOST_USER
                to_email = [user.email]
                
                send_mail(
                    subject,
                    plain_message,
                    from_email,
                    to_email,
                    html_message=html_message,
                    fail_silently=False,
                )
                
                messages.success(request, 'Password reset link has been sent to your email.')
                return redirect('login')
            except CustomUser.DoesNotExist:
                # We don't want to reveal which emails are registered
                messages.success(request, 'Password reset link has been sent to your email (if it exists).')
                return redirect('login')
        
        return render(request, 'user_auth/password_reset_request.html', {'form': form})


class PasswordResetConfirmView(View):
    """
    View for confirming password reset with token and setting new password.
    """
    def get(self, request, token):
        # Validate token
        user = PasswordResetToken.validate_token(token)
        
        if user is None:
            messages.error(request, 'Invalid or expired password reset link.')
            return redirect('password_reset_request')
        
        form = CustomSetPasswordForm(user)
        return render(request, 'user_auth/password_reset_confirm.html', {
            'form': form,
            'token': token
        })
    
    def post(self, request, token):
        # Validate token
        user = PasswordResetToken.validate_token(token)
        
        if user is None:
            messages.error(request, 'Invalid or expired password reset link.')
            return redirect('password_reset_request')
        
        form = CustomSetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            
            # Delete the token
            PasswordResetToken.objects.filter(user=user).delete()
            
            messages.success(request, 'Your password has been reset. You can now login with your new password.')
            return redirect('login')
        
        return render(request, 'user_auth/password_reset_confirm.html', {
            'form': form,
            'token': token
        })


@login_required
def profile_view(request):
    """
    View for user profile.
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'user_auth/profile.html', {'form': form})
