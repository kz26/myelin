import hashlib
import random
import string

from django.conf import settings

def randomString(size=64, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def hashWithSecretKey(s):
	return hashlib.sha256(settings.SECRET_KEY + s).hexdigest() 
