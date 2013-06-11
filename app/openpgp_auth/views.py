from django.core.cache import cache
from django.views.generic.base import View
from django.contrib import auth
from django.shortcuts import *

from rest_framework.views import *
from rest_framework.response import Response

from app.openpgp_auth.gpg import GPG
from app.openpgp_auth.models import PGPUser
from app.openpgp_auth.string_utils import *
from app.openpgp_auth.forms import *

class RegisterView(View):
	template_name = 'openpgp_auth/register.html'

	def get(self, request, *args, **kwargs):
		form = RegisterForm()
		return render(request, self.template_name, {'form': form})	
	def post(self, request, *args, **kwargs):
		form = RegisterForm(request.POST, request.FILES)
		if form.is_valid():
			pubkey = form.pubkey
			result = GPG.import_keys(pubkey)
			if result.imported == 1:
				return redirect('home')
			else:
				return render(request, self.template_name, {'form': form, 'import_error': True})
		return render(request, self.template_name, {'form': form})

class LoginChallengeView(APIView):
	def post(self, request, *args, **kwargs):
		if 'pubkey_fingerprint' in request.DATA:
			try:
				user = PGPUser.objects.get(pubkey_fingerprint=request.DATA['pubkey_fingerprint'])	
			except PGPUser.DoesNotExist:
				return Response({'error': 'Unregistered public key'}, status=403)
			challengeStr = randomString()
			cache.set(user.pubkey.pubkey_fingerprint, challengeStr, 60)
			challenge = GPG.encrypt(challengeStr, user.pubkey.pubkey_fingerprint)
			return Response({'challenge': challenge}, status=200) 
		return Response({'error': 'pubkey_fingerprint must be provided'}, status=400)

class LoginResponseView(APIView):
	def post(self, request, *args, **kwargs):
		if all([x in request.DATA for x in ('pubkey_fingerprint', 'response')]):
			try:
				user = PGPUser.objects.get(pubkey_fingerprint=request.DATA['pubkey_fingerprint'])
			except PGPUser.DoesNotExist:
				return Response({'error': 'Invalid pubkey'}, status=403)
			challengeStr = cache.get(user.pubkey_fingerprint, '') 
			cache.delete(user.pubkey_fingerprint)
			user = auth.authenticate(user, challengeStr, request.DATA['response'])
			if user is not None:
				auth.login(request, user)
				return Response(None, status=204)
			return Response({'error': 'Incorrect response. Login failed.'}, status=403)
		return Response({'error': 'pubkey_fingerprint and response must be provided.'}, status=400)
