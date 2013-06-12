from app.openpgp_auth.models import PGPUser

class PGPAuthBackend(object):
	def get_user(user_id):
		try:
			return PGPUser.objects.get(pk=user_id)
		except PGPUser.DoesNotExist:
			return None

	def authenticate(self, user, challenge, response):
		if challenge == response:
			return user
		return None


