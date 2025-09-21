from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail,BadHeaderError
from django.conf import settings
from .forms import SignUpForm, LoginForm
import requests

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Password hashed automatically
            # Try sending welcome email
            if user.email:
                try:
                    send_mail(
                        subject="Welcome to Holidays!",
                        message=(
                            f"Hi {user.username},\n\n"
                            f"Thank you for registering with Holidays.\n\n"
                            f"Regards,\nHolidays Team"
                        ),
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False,
                    )
                except BadHeaderError:
                    messages.warning(request,
                        "Registered, but welcome email could not be sent (bad header).")
                except Exception:
                    messages.warning(request,
                        "Registered, but we couldn't send the welcome email right now.")
            messages.success(request, "Registration successful. Please log in.")
            return redirect('Userid:login')  # adjust namespace if different
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('Userid:home')
    return render(request, 'login.html', {'form': form})

@login_required
def home_view(request):
    url = "https://date.nager.at/api/v3/publicholidays/2025/AT"
    holidays = []
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        holidays = r.json()
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Could not fetch holidays: {e}")
    return render(request, 'home.html', {
        'username': request.user.username,
        'holidays': holidays
    })
    
def logout_view(request):
    logout(request)
    return redirect('Userid:login')


# Create your views here.
