from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.views.generic import View

# activate account
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import NoReverseMatch, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError, force_str

# emails
from django.core.mail import send_mail, EmailMultiAlternatives, BadHeaderError, EmailMessage
from django.core import mail
from django.conf import settings

# threading
import threading

# reset password generators
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Getting tokens from utils.py
from .utils import TokenGenerator, generate_token


class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        return self.email_message.send()

def signUp(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # passwords must match
        if password == confirm_password:
            # check if username exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
                return redirect('login')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "Email already exists!")
                    return redirect('login')
                else:
                    # no error so far, store the data
                    user = User.objects.create_user(
                        username=username, email=email, password=password)
                    user.is_active = False
                    user.save()
                    #send activation link
                    current_site = get_current_site(request)
                    email_subject = 'Activate your Account'
                    message = render_to_string('smarketauth/activate.html', {
                        'user': user,
                        'domain': '127.0.0.1:8000',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': generate_token.make_token(user)
                    })
                    email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email],)
                    EmailThread(email_message).start()

                    # auto-login the user
                    auth.login(request, user)
                    messages.success(request, "We've sent activation link to your email. Please click the link to activate.")
                    return redirect('login')
                    # OR redirect the user to login
                    # messages.success(request, 'registered successfully!')
                    # return redirect('login')

        else:
            messages.error(request, 'passwords do not match')
            return redirect('register')

    return render(request, 'smarketauth/signup.html')

def login(request):
    # if trying to login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # the user
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # login user
            auth.login(request, user)
            messages.success(request, "Successfully logged in!")
            return redirect('/')
        else:
            messages.error(request, 'Wrong username or password')
            return redirect('login')
    return render(request, 'smarketauth/login.html')

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as indentifier:
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfuly!')
            return redirect('login')
        return render(request, 'smarketauth/activate.html')

class RequestResetEmailView(View):
    def get(self, request):
        return render(request, 'smarketauth/request-reset-email.html')

    def post(self, request):
        email = request.POST['email']
        user = User.objects.filter(email=email)
        if user.exists():
            current_site = get_current_site(request)
            email_subject = '[Reset your Password]'
            message = render_to_string('smarketauth/reset-user-password.html',
                                       {

                                           'domain': '127.0.0.1:8000',
                                           'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                                           'token': PasswordResetTokenGenerator().make_token(user[0]),
                                       })
            email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
            EmailThread(email_message).start()
            messages.success(request, "We have sent you an email with instructions on how to reset password")
            return render(request, 'smarketauth/request-reset-email.html')

class SetNewPasswordView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.error(request, 'Password reset link is Invalid! Request a new one')
                return render(request, 'smarketauth/request-reset-email.html')
        except DjangoUnicodeDecodeError as identifier:
            pass
        return render(request, 'smarketauth/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Password is not matching')
            return render(request, 'smarketauth/set-new-password.html', context)

        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Reset Success! Please login with new password')
            return redirect('login')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, 'Something went wrong')

        return render(request, 'smarketauth/set-new-password.html', context)


