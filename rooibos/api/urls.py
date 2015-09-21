# commented out this file rest_framework lines are for future development of the MDID3 api


from __future__ import absolute_import
from django.conf.urls import patterns, url, include, handler404

# from rest_framework import routers

from .views import *

# router = routers.DefaultRouter()
# router.register(r'record', RecordViewSet)

urlpatterns = patterns('',

    url(r'^collection/(?P<id>\d+)/$', collections),
    url(r'^collections/$', collections),
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^search/$', api_search),
    url(r'^search(/(?P<id>\d+)/(?P<name>[\w-]+))?/$', api_search),
    url(r'^record/(?P<id>\d+)/(?P<name>[-\w]+)/$', record, name='api-record'),
    url(r'^presentations/currentuser/$', presentations_for_current_user),
    url(r'^presentation/(?P<id>\d+)/$', presentation_detail, name='api-presentation-detail'),
    url(r'^keepalive/$', keep_alive, name='api-keepalive'),
    url(r'^autocomplete/user/$', autocomplete_user, name='api-autocomplete-user'),
    url(r'^autocomplete/group/$', autocomplete_group, name='api-autocomplete-group'),
    # for now separate out django-rest api
    # url(r'^v2/', include(router.urls)),
)
