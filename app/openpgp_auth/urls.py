from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from app.openpgp_auth.views import *

urlpatterns = patterns('',
	url(r'^register/$', RegisterView.as_view(), name="register"),
)
