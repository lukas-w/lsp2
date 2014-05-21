from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.views.generic import TemplateView

import lsp2.submissions.urls

urlpatterns = patterns(
	'',
	# Examples:
	# url(r'^$', 'lsp2.views.home', name='home'),
	# url(r'^lsp2/', include('lsp2.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
	(r'^accounts/', include('allauth.urls')),
	(r'^accounts/profile/$', TemplateView.as_view(template_name='account/profile.html')),

	(r'^', include(lsp2.submissions.urls))
)
