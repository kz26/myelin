from django.core.cache import cache
from django.views.base import View
from django.contrib import auth
from django.shortcuts import *

from rest_framework.views import *
from rest_framework.response import Response

from openpgp_auth.gpg import GPG
from openpgp_auth.models import User
from openpgp_auth.string_utils import *

class RegisterView(View):
	template_name = 'openpgp_auth/register.html'
	def get(self, request, *args, **kwargs):
		form = RegisterForm()
		return render(request, template_name, {'form': form})	
	def post(self, request, *args, **kwargs):
		form = RegisterForm(request.POST, request.FILES)
		if form.is_valid():
			pubkey = form.get_pubkey()
			result = gpg.import_keys(pubkey)
			if result.imported == 1:
				return redirect('home')
			else:
				return render(request, template_name, {'form': form, 'import_error': True})
		return render(request, template_name, {'form': form})

class LoginChallengeView(APIView):
	def post(self, request, *args, **kwargs):
		if 'pubkey_fingerprint' in request.DATA:
			try:
				user = User.objects.get(pubkey_fingerprint=request.DATA['pubkey_fingerprint'])	
			except User.DoesNotExist:
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
				user = User.objects.get(pubkey_fingerprint=request.DATA['pubkey_fingerprint'])
			except User.DoesNotExist:
				return Response({'error': 'Invalid pubkey'}, status=403)
			challengeStr = cache.get(user.pubkey_fingerprint, '') 
			cache.delete(user.pubkey_fingerprint)
			if request.DATA['response'] == challengeStr:
				auth.login(request, user)
				return Response(None, status=204)
			return Response({'error': 'Incorrect response. Login failed.'}, status=403)
		return Response({'error': 'pubkey_fingerprint and response must be provided.'}, status=400)
