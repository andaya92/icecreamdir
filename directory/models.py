from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from myfriends.models import User


# Create your models here.

class Parlor(models.Model):
	name = models.CharField(max_length=25)
	phone = models.CharField(max_length=15)

	def __str__(self):
		return "{} {}".format(self.name, self.phone)

class HOOperation(models.Model):
	day = models.IntegerField(default=0)
	opentime = models.TimeField(null=True, blank= True)
	closetime = models.TimeField(null=True, blank= True)
	business = models.ForeignKey(Parlor, on_delete = models.CASCADE)

	def __str__(self):
		return "{}| {} {} to {}".format(self.business.name, self.day, str(self.opentime), str(self.closetime))

## Holds all icecream entries
class Icecreams(models.Model):
	name = models.CharField(max_length = 50, default="White Swirly", db_index=True)
	image = models.CharField(max_length= 100, default="/static/images/default.png")
	flavor = models.CharField(max_length = 50, default="Vanilla")
	kin = models.CharField(max_length = 15, default="HardIce", db_index=True)
	style = models.CharField(max_length = 15, default="No-Churn")
	price = models.DecimalField(max_digits=4, decimal_places=2)
	favors = models.ManyToManyField(User, related_name="favors", blank = True)
	haters = models.ManyToManyField(User, related_name="haters", blank = True)
	parlors = models.ManyToManyField(Parlor, related_name="parlors", blank= True)

	class Meta:
		unique_together = (('name', 'kin'),)

	def __str__(self):
		return "{} | {} | ${} ({})".format(self.name, self.kin, str(self.price), self.id)  

class Comments(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, db_index=True)
	icecream = models.ForeignKey(Icecreams, on_delete = models.CASCADE, db_index=True)
	comment = models.CharField(max_length = 280, default = "So Gud!")

	def __str__(self):
		return self.icecream.name + " | " + str(self.user) + ": " + self.comment[:10]

