from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', 'bio.views.sequence_redirect', name='bio_sequence_redirect'),

    url(r'^(?P<sequence>[\w-]+)/$', 'bio.views.bio', name='bio_bio'),

    url(
        r'^(?P<sequence>[\w-]+)/save_bio/$',
        'bio.views.save_bio',
        name='bio_save_bio'
    ),

    url(
        r'^(?P<sequence>[\w-]+)/request_link/$',
        'bio.views.request_link',
        name='bio_request_link'
    ),

    url(r'^clear_session/$', 'bio.views.clear_session'),
)
