from django.conf import settings

import gnupg

GPG = gnupg.GPG(gnupghome=settings.GPG_HOME)
