from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'classphoto.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^bio/', include('bio.urls')),
    url(r'^twitter/', include('twitter.urls')),
    url(r'^gplus/', include('gplus.urls')),
    url(r'^/$', TemplateView.as_view(template_name="home.html"), name='home'),
)
