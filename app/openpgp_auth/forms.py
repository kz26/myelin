from django import forms

class RegisterForm(forms.Form):
	error_css_class = "text-error"
	required_css_class = error_css_class

	username = forms.RegexField(regex='^[A-Za-z0-9_\-]+$', max_length=30)
	pubkey_file = forms.FileField(required=False)
	pubkey_string = forms.CharField(required=False, widget=forms.Textarea())

	def clean(self):
		cleaned_data = super(RegisterForm, self).clean()
		pubkey_string = cleaned_data.get('pubkey_string')
		pubkey_file = cleaned_data.get('pubkey_file')	
		if not (pubkey_string or pubkey_file):
			raise forms.ValidationError("The OpenPGP public key must be uploaded as a file or entered as ASCII-armored plain text.")
		pubkey = self.get_pubkey()
		if not (pubkey.find("-----BEGIN PGP PUBLIC KEY BLOCK-----") == 0 and pubkey.endswith("-----END PGP PUBLIC KEY BLOCK-----")):
			raise forms.ValidationError("Invalid OpenPGP public key.")
		self.pubkey = pubkey
		return cleaned_data

	def get_pubkey(self):
		if getattr(self, 'cleaned_data', None):
			if self.cleaned_data.get('pubkey_file'):
				return self.cleaned_data['pubkey_file'].read().strip()
			elif self.cleaned_data.get('pubkey_string'):
				return self.cleaned_data['pubkey_string'].strip()
		return None
