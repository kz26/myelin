from django.conf import settings

import gnupg

GPG = gnupg.GPG(gnupghome=settings.GPG_HOME)

def get_key_info(fingerprint, private=False):
	for key in GPG.list_keys(private):
		if key['fingerprint'] == fingerprint:
			return key
	return None
