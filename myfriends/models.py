from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from icecreamshop import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

# Create your models here.

class User(AbstractUser):
	photo = models.ImageField(upload_to="user_images", default='default_user.jpeg')
	DOB = models.DateField(default = datetime.date.today)
	friends = models.ManyToManyField('self', blank = True)
	token_user_auth = models.CharField(max_length=100, blank=True, null =True)

	def __str__(self):
		return "{} ({})".format(self.username, self.id)

