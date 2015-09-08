# from django.conf.urls import *
from django.conf.urls import patterns, url, include, handler404
from django.contrib import admin
from django.conf import settings
#from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView
from django.views.static import serve
from django.views.decorators.cache import cache_control
from django.http import HttpResponseServerError
from django.template import loader, RequestContext
from rooibos.ui.views import main
from rooibos.access.views import login, logout
from rooibos.legacy.views import legacy_viewer

import logging

log = logging.getLogger('rooibos')

admin.autodiscover()

# Cache static files
serve = cache_control(max_age=365 * 24 * 3600)(serve)


def handler500_with_context(request):
    template = loader.get_template('500.html')
    return HttpResponseServerError(template.render(RequestContext(request)))


handler404 = getattr(settings, 'HANDLER404', handler404)
handler500 = getattr(settings, 'HANDLER500', handler500_with_context)


def raise_exception():
    raise Exception()


urls = [
    # main page needs SSL because of embedded login form, otherwise CSRF fails
    url(r'^$', main, {'HELP': 'frontpage', 'SSL': True}, name='main'),
    url(r'^about/', TemplateView.as_view(template_name='about.html'), name='about'),
    #url(r'^showcases/', TemplateView.as_view(HELP='showcases', template='showcases.html', extra_context={'applications': apps_showcases}), name='showcases'))
    url(r'^login/$', login, {'HELP': 'logging-in', 'SSL': True}, name='login'),
    url(r'^logout/$', logout, {'HELP': 'logging-out', 'next_page': settings.LOGOUT_URL}, name='logout'),
    #    url(r'^admin/(.*)', admin.site.root, {'SSL': True}, name='admin'),
    (r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    (r'^admin/', include(admin.site.urls)),

    # Legacy URL for presentation viewer in earlier version
    url(r'^viewers/view/(?P<record>\d+)/.+/$', legacy_viewer),

    (r'^ui/', include('rooibos.ui.urls')),
    (r'^acl/', include('rooibos.access.urls')),
    (r'^explore/', include('rooibos.solr.urls')),
    (r'^media/', include('rooibos.storage.urls')),
    (r'^data/', include('rooibos.data.urls')),
    (r'^legacy/', include('rooibos.legacy.urls')),
    (r'^presentation/', include('rooibos.presentation.urls')),
    (r'^viewers/', include('rooibos.viewers.urls')),
    (r'^workers/', include('rooibos.workers.urls')),
    (r'^convert/', include('rooibos.converters.urls')),
    (r'^api/', include('rooibos.api.urls')),
    (r'^profile/', include('rooibos.userprofile.urls')),
    (r'^federated/', include('rooibos.federatedsearch.urls')),
    #    (r'^nasa/', include('rooibos.federatedsearch.nasa.urls')),
    (r'^flickr/', include('rooibos.federatedsearch.flickr.urls')),
    (r'^artstor/', include('rooibos.federatedsearch.artstor.urls')),
    (r'^shared/', include('rooibos.federatedsearch.shared.urls')),
    (r'^impersonate/', include('rooibos.contrib.impersonate.urls')),
    (r'^mediaviewer/', include('rooibos.mediaviewer.urls')),
    (r'^megazine/', include('rooibos.megazine.urls')),
    (r'^pdfviewer/', include('rooibos.pdfviewer.urls')),
    (r'^pptexport/', include('rooibos.pptexport.urls')),
    (r'^audiotextsync/', include('rooibos.audiotextsync.urls')),

    url(r'^favicon.ico$', serve, {'document_root': settings.STATIC_DIR, 'path': 'images/favicon.ico'}),
    url(r'^robots.txt$', serve, {'document_root': settings.STATIC_DIR, 'path': 'robots.txt'}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_DIR}, name='static'),

    url(r'^exception/$', raise_exception),
]

"""
    MDID plugin apps (i.e. apps in the rooibos/apps dir)
    added to settings.INSTALLED_APPS as 'rooibos.apps.{appname} will have their urls
    automatically added to MDID



"""
# TODO: should apps_prefix be set in settings_local?
# urls were not loading for apps
apps_prefix = 'rooibos.apps.'
apps_pre_slice = apps_prefix.__len__()

apps = filter(lambda a: a.startswith(apps_prefix), settings.INSTALLED_APPS)

#if settings.CLIP_APP_NAMES:
#    # TODO update for a tuple rather than a string - currently only the first will be processed
#    clip = settings.CLIP_APP_STRINGS[0]
#else:
#    clip = ''

app_list = [app[len(clip):] if app[:len(clip)] == clip else app for app in [app[apps_pre_slice:] for app in apps]]
# TODO: is it a correct assumpion that showcases would want to clip names as well?
apps_showcases = list(s[apps_pre_slice:].replace('.', '-') + '-showcase.html' for s in app_list)

log.debug('processing rooibos.apps: %s ' % app_list)

for app in apps:
    #if not '.' in app[5:]:
    if not '.' in app[apps_pre_slice:]:
        # list dynamically appended app urls in  log
        sliced_app = app[apps_pre_slice:]
        app_name = sliced_app[len(clip):] if sliced_app[:len(clip)] == clip else sliced_app
        log.debug('rooibos.urls - appending urls for %s as ^/%s'
                  ' (app added via config.settings_local.INSTALLED_APPS)' % (app, app_name))
        try:
            urls.append(url(r'^%s/' % app_name, include('%s.urls' % app)))
        except Exception as e:
            log.debug('rooibos.urls Error loading  %s.urls -not loaded' % app)
            log.debug(e)
            continue

urlpatterns = patterns('', *urls)


# # CLIP_APP_STRINGS = ('mdid-', )
# clip = 'mdid-'
#
# if settings.CLIP_APP_NAMES:
#     app_url_list = [app[len(clip):]
#                     if app[:len(clip)] == clip else app
#                     for app in [app[apps_pre_slice:] for app in apps]]
#
#     log.debug('app_name_list: %s ' % app_url_list)
# else:
#     app_url_list = [app for app in apps]
#
# for app in apps:
#     #log.debug('app = %s; clip: %s,  app[:len(clip)]: %s, app: %s' % (app, clip, app[:len(clip)], app[len(clip):]))
#
#     #if not '.' in app[5:]:
#     if not '.' in app[apps_pre_slice:]:
#         sliced_app = app[apps_pre_slice:]
#         # list dynamically appended app urls in  log
#         log.debug('rooibos.urls - attempting to append urls for %s as ^/%s'
#                   ' (app added via config.settings_local.INSTALLED_APPS)' % (app, sliced_app))
#         try:
#             if settings.CLIP_APP_NAMES and sliced_app[:len(clip)] == clip:
#                 clipped_name = sliced_app[len(clip):]
#                 log.debug('app %s, app name: %s, clipped name: %s' % (app, sliced_app, clipped_name))
#                 urls.append(url(r'^%s/' % clipped_name, include('%s.urls' % sliced_app)))
#             else:
#                 urls.append(url(r'^%s/' % app[apps_pre_slice:], include('%s.urls' % app)))
#         except Exception as e:
#             log.debug('rooibos.urls Error loading  %s.urls -not loaded' % app)
#             continue
