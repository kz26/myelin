from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from app.openpgp_auth.views import *

urlpatterns = patterns('',
	url(r'^register/$', RegisterView.as_view(), name="register"),
	url(r'^login/$', TemplateView.as_view(template_name="openpgp_auth/login.html"), name="login"),
	url(r'^login/challenge/$', LoginChallengeView.as_view(), name="login_challenge"),
	url(r'^login/response/$', LoginResponseView.as_view(), name="login_response"),
	url(r'^keygen/$', TemplateView.as_view(template_name="openpgp_auth/keygen.html"), name="keygen"),
)
