from app.users.models import User

class PGPAuthBackend(object):
	def get_user(user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None

	def authenticate(self, pubkey, challenge, response):
		try:
			user = User.objects.get(pubkey=pubkey)
		except:
			return None
		if challenge == response:
			return user
		return None


