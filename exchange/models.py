from django.db import models


# Create your models here.
class RegisterLike(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    access_token = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=False, blank=False, default='')
