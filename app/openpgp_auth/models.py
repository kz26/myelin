from django.db import models
from django.contrib.auth.models import BaseUserManager

from picklefield.fields import PickledObjectField

from string_utils import *

# Create your models here.

class UserManager(BaseUserManager):
	def create_user(self, username, pubkey, pubkey_info, **kwargs):
		return User.objects.create(username=username, pubkey=pubkey, pubkey_info=pubkey_info)
	def create_superuser(self, username, pubkey, pubkey_info, **kwargs):
		pass

class User(object):
	username = models.CharField(max_length=30, unique=True, db_index=True)
	pubkey = models.TextField(unique=True, db_index=False)
	pubkey_fingerprint = models.CharField(max_length=40, unique=True, db_index=True)
	pubkey_info = PickledObjectField()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []

	objects = UserManager()

	def save(self, *args, **kwargs):
		if not self.id:
			self.pubkey_fingerprint = self.pubkey_info.fingerprint
		super(User, self).save(*args, **kwargs)
