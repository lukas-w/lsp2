from django.conf.urls import patterns, url
from django.views.generic import TemplateView, RedirectView

from lsp2.backend.views import *

urlpatterns = patterns('',
	url(r'^$', WelcomeView.as_view(), name='welcome'),

	url(r'^files/$', SubmissionList.as_view(), name='submission-list'),
	url(r'^files/(?P<pk>\d+)/$', SubmissionDetail.as_view(), name='submission-detail'),
	url(r'^users/(?P<pk>\d+)/$', UserDetail.as_view(), name='user-detail'),
)
