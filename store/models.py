from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class category(models.Model):
     name = models.CharField(max_length = 50)
     slug = models.SlugField()
     created_at = models.DateTimeField(auto_now_add=True)
     def save(self,*arg,**knargs):
          if not self.slug:
               self.slug = slugify(self.name)
               super().save(*arg,**knargs)
     
     def get_category_url(self):
          return  reverse('store:category',args=[self.slug])
     def __str__(self):
          return self.name




class product(models.Model):
     class Status(models.TextChoices):
          available = 'AV','available'
          dreft = 'DF','dreft'

     name = models.CharField(max_length=50)
     slug = models.SlugField()
     image = models.ImageField('product/images')
     description = models.TextField(max_length=1000)
     price = models.DecimalField(max_digits=6,decimal_places=2)
     category = models.ForeignKey(category,on_delete=models.CASCADE,null=True,blank=True)
     status = models.CharField(max_length=2,choices=Status.choices,default=Status.available)
     status = models.CharField(max_length=2,choices=Status.choices,default=Status.available)
     created_at = models.DateTimeField(auto_now_add=True)
     update = models.DateTimeField(auto_now_add=True)
     feature = models.CharField(max_length = 250)
     def save(self,*arg,**knargs):
          if not self.slug:
               self.slug = slugify(self.name)
               super().save(*arg,**knargs)
     class Meta:
          ordering = ['name']
          indexes = [
               models.Index(fields=['id','slug']),
               models.Index(fields=['name']),
               models.Index(fields=['-created_at']),
          ]
     def __str__(self):
          return self.name
     def get_url(self):
          return reverse('store:home')