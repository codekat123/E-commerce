from django.shortcuts import render , redirect
from .forms import RegisterForm
from .models import account
from django.contrib.auth import authenticate , login as auth_login



# activatetoin account 
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages


def register(request):
     if request.method == 'POST':
          form = RegisterForm(request.POST)
          if form.is_valid():
               first_name = form.cleaned_data['first_name']
               last_name = form.cleaned_data['last_name']
               email = form.cleaned_data['email']
               country = form.cleaned_data['country']
               password = form.cleaned_data['password']
               username = email.split('@')[0]
               phone_number = form.cleaned_data['phone_number']
               user = account.objects.create_user(first_name = first_name,last_name = last_name , email = email , country = country , username = username, password = password)
               user.phone_number = phone_number
               user.save()

               # User active
               domain_name = get_current_site(request)
               mail_subject ="please activate your email"
               message = render_to_string('accounts/account_verification_email.html',{
                    'user':user,
                    'domain':domain_name,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':default_token_generator.make_token(user),
               })
               send_to = EmailMessage(mail_subject,message,to = [email])
               send_to.send()

               return redirect('login' + f'?command=verification&mail={email}')

     else:
          form = RegisterForm()
     context = {
          'form':form,
          
     }
     return render(request,'accounts/register.html',context)


def login(request):
     if request.method == 'POST':
          email= request.POST['email']
          password= request.POST['password']
          user = authenticate(email = email, password = password)
          if user is not None :
               auth_login(request,user)
               messages.success(request,'login is successfully')
               return redirect('store:home')
          else:
               messages.error(request,'invalid password')
               return redirect('accounts:login')
     return render(request,'accounts/login.html')


def activate(request,uid64,token):
     try:
          uid = urlsafe_base64_decode(uid64).decode()
          user = account._default_manager.get(pk=uid)
     except(TypeError,ValueError,OverflowError,account.DoesNotExist):
          user = None     
     if user is not None and default_token_generator.check_token(user,token):
          user.is_active = True
          user.save()
          messages.success(request,'your account has been activated')
          return redirect('accounts:login')
     else:
          user = None
          messages.error(request,'something went wrong')
          return redirect('accounts:register')
     

