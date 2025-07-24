from django import forms
from .models import Order,OrderPay
from django.core.exceptions import ValidationError

class OrderCreateForm(forms.ModelForm):
     class Meta:
          model = Order
          fields = ['first_name','last_name','email','address','postal_code','city']


class OrderPayForm(forms.ModelForm):
     class Meta:
          model = OrderPay
          fields = ['pay_phone_number','pay_image']
     def clean_pay_phone(self):
          pay_phone = self.cleaned_data.get('pay_phone_number')
          initial_number = ['011','012','010','015']
          if not pay_phone.isdigit():
               raise ValidationError("the phone number must contian only digits.")
          if len(pay_phone) != 11:
               raise ValidationError("the phone must be exactly 11 digits long ")
          if not pay_phone[:3] in initial_number:
               raise ValidationError("Unknown phone number")
          return pay_phone

