from django.db import models
from django.contrib.auth.models import BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
	def create_user(self, username, pubkey, **kwargs):
		return User.objects.create(username=username, pubkey=pubkey)
	def create_superuser(self, username, pubkey, **kwargs):
		pass

class User(object):
	username = models.CharField(max_length=30, unique=True, db_index=True)
	pubkey = models.TextField(unique=True, db_index=True)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	objects = UserManager()
