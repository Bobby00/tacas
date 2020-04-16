from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	avatar = models.ImageField(blank=True, upload_to='avatars')
	location = CountryField()
	phonenumber = models.CharField(max_length=20)

	def __str__(self):
		return self.user.username