from django import forms
from .models import account

class RegisterForm(forms.ModelForm):
     password = forms.CharField(widget =forms.PasswordInput())
     confirm_password = forms.CharField(widget =forms.PasswordInput())

     class Meta:
          model = account
          fields = ['first_name','last_name','email','phone_number','country']
     def clean(self):
          cleaned_data = super(RegisterForm,self).clean()
          password = cleaned_data.get('password')
          confirm_password = cleaned_data.get('confirm_password')
          if password and confirm_password and password != confirm_password:
               raise forms.ValidationError('your password don\'t match ')
          return cleaned_data
     
     def __init__(self,*arg,**kwargs):
          super(RegisterForm,self).__init__(*arg,**kwargs)
          self.fields['first_name'].widget.attrs['placeholder'] = 'please enter your first name'
          self.fields['last_name'].widget.attrs['placeholder'] = 'please enter your last name'
          self.fields['email'].widget.attrs['placeholder'] = 'you can enter your email here'
          self.fields['phone_number'].widget.attrs['placeholder'] = 'enter your number here'
          self.fields['password'].widget.attrs['placeholder'] = 'you can create your password here'