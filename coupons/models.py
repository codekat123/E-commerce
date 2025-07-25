from django.db import models
from django.core.validators import MinValueValidator , MaxValueValidator

class Coupon(models.Model):
     code = models.CharField(max_length = 8,unique=True)
     valid_from = models.DateTimeField()
     valid_to = models.DateTimeField()
     discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)],help_text="percentage value from 0 to 100")
     active = models.BooleanField()
     

     def __str__(self):
          return self.code