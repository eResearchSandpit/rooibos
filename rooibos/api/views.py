from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.contrib import auth
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, HttpRequest, HttpResponseNotAllowed, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.cache import cache_control
from rooibos.access.functions import filter_by_access
from rooibos.data.models import Collection, CollectionItem, DisplayFieldValue, Field, FieldSet, FieldSetField, FieldValue, MetadataStandard, Record
from rooibos.presentation.models import Presentation
from rooibos.solr.views import *
from rooibos.storage import get_thumbnail_for_record
from rooibos.storage.models import Storage, Media
from rooibos.storage.views import create_proxy_url_if_needed
from rooibos.ui import update_record_selection
from rooibos.util import safe_int, json_view, must_revalidate
from rooibos.util.models import OwnedWrapper
from tagging.models import Tag
from django.views.decorators.csrf import csrf_exempt



# urls for easy reference

    # url(r'^search/$', api_search),
    # url(r'^search(/(?P<id>\d+)/(?P<name>[\w-]+))?/$', api_search),
    # url(r'^record/(?P<id>\d+)/(?P<name>[-\w]+)/$', record, name='api-record'),
    # url(r'^presentations/currentuser/$', presentations_for_current_user),
    # url(r'^presentation/(?P<id>\d+)/$', presentation_detail, name='api-presentation-detail'),
    # url(r'^keepalive/$', keep_alive, name='api-keepalive'),
    # url(r'^autocomplete/user/$', autocomplete_user, name='api-autocomplete-user'),
    # url(r'^autocomplete/group/$', autocomplete_group, name='api-autocomplete-group'),


"""
@apiDefine csrf User must be logged in
This api will only return correct results if the user has been authenticated
"""


@json_view
def collections(request, id=None):
    """
    @api {get} /collection/:id Get Collection Information
    @apiName collections
    @apiGroup collections
    @apiVersion 1.0.0

    @apiParam {Number} id Collection ID.

    @apiDescription Returns information about a Collection obtained via filter_by_access(request.user, Collection.objects.filter(id=id))

    @apiSuccessExample {json} User has access to a collection
    {"collections": [{"description": "Personal images", "title": "Personal Images", "agreement": null, "children": [], "owner": null, "hidden": false, "id": 1, "name": "personal-images"}], "result": "ok"}

    @apiSuccessExample {json} Collection does not exist
    {"collections": [], "result": "ok"}

    @apiSuccess {json} collections A list of the collections the sepecific user has access to.

    @apiUse csrf
    """



    if id:
        collections = filter_by_access(request.user, Collection.objects.filter(id=id))
    else:
        collections = filter_by_access(request.user, Collection)
    return {
        'collections': [
            dict(id=c.id,
                 name=c.name,
                 title=c.title,
                 owner=c.owner.username if c.owner else None,
                 hidden=c.hidden,
                 description=c.description,
                 agreement=c.agreement,
                 children=list(c.children.all().values_list('id', flat=True)),
                 )
            for c in collections]
    }


"""
@api {get} /collections List User's Accessible Collections
@apiName collection
@apiGroup collections
@apiVersion 1.0.0

@apiDescription Returns a list of Collections obtained via filter_by_access(request.user, Collection)

@apiSuccess {json} collections A list of the collections the current user has access to.

@apiSuccessExample {json} User has access to a collection
{"collections": [], "result": "ok"}
"""



@csrf_exempt
@json_view
def login(request):
    """
    @api {post} /login Login
    @apiName login
    @apiGroup authentication
    @apiVersion 1.0.0

    @apiParam {String} username request.POST["username"]
    @apiParam {String} password request.POST["password"]

    @apiDescription Authenticate a user

    @apiSuccess {Number} sessionid Session ID token
    @apiSuccess {Number} userid The ID (pk) of the authenticated user
    @apiSuccess {String} result Will be either 'ok', 'Login failed' or 'Invalid method. Use POST.'

    @apiSuccessExample {json} User is successfully logged in
    {"sessionid": "b87ed91f693bc51927d522c60fc22ac9", "userid": 37, "result": "ok"}

    @apiErrorExample {json} Login Failed
    {"result": "Login failed"}

    @apiErrorExample {json} Forgot to use Post
    {"result": "Invalid method. Use POST."}

    """

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if (user is not None) and user.is_active:
            auth.login(request, user)
            return dict(result='ok',
                        sessionid=request.session.session_key,
                        userid=user.id)
        else:
            return dict(result='Login failed')
    else:
        return dict(result='Invalid method. Use POST.')


@json_view
def logout(request):
    """
    @api {get} /logout Logout
    @apiName logout
    @apiGroup authentication
    @apiVersion 1.0.0

    @apiDescription Log a user out. Does not require POST.

    @apiSuccess {String} result Will be always be 'ok'

    @apiSuccessExample {json} User is successfully logged out
    {"result": "ok"}
    """
    auth.logout(request)
    return dict(result='ok')


def _record_as_json(record, owner=None, context=None, process_url=lambda url: url,
                    dc_mapping_cache=None):
    if dc_mapping_cache is None:
        dc_mapping_cache = dict()

    def get_dc_field(field):
        if not field.id in dc_mapping_cache:
            if field.standard and field.standard.prefix == 'dc':
                dc_mapping_cache[field.id] = field.name
            else:
                equivalents = (field for field in field.get_equivalent_fields()
                              if field.standard and field.standard.prefix == 'dc')
                try:
                    dc_mapping_cache[field.id] = equivalents.next().name
                except StopIteration:
                    pass
        return dc_mapping_cache.get(field.id)

    return dict(
                id=record.id,
                name=record.name,
                title=record.title,
                thumbnail=process_url(record.get_thumbnail_url()),
                image=process_url(record.get_image_url()),
                metadata=[
                    dict(
                        label=value.resolved_label,
                        value=value.value,
                        order=value.order,
                        dc=get_dc_field(value.field),
                        )
                    for value in record.get_fieldvalues(owner=owner, context=context)
                ]
            )

def _records_as_json(records, owner=None, context=None, process_url=lambda url: url):
    dc_mapping_cache = dict()
    return [_record_as_json(record, owner, context, process_url, dc_mapping_cache)
            for record in records] if records else []


def _presentation_item_as_json(item, owner=None, process_url=lambda url: url):

    fieldvalues = item.get_fieldvalues(owner=owner)

    data = dict(
                id=item.record.id,
                name=item.record.name,
                title=item.title_from_fieldvalues(fieldvalues) or 'Untitled',
                thumbnail=process_url(item.record.get_thumbnail_url()),
                image=process_url(item.record.get_image_url()),
                metadata=[
                    dict(
                        label=value.resolved_label,
                        value=value.value
                        )
                    for value in fieldvalues
                ]
            )
    annotation = item.annotation
    if annotation:
        data['metadata'].append(dict(label='Annotation', value=annotation))
    return data

def _presentation_items_as_json(items, owner=None, process_url=lambda url: url):
    return [_presentation_item_as_json(item, owner, process_url) for item in items]


@json_view
def api_search(request, id=None, name=None):
    hits, records, viewmode = search(request, id, name, json=True)
    return dict(hits=hits,
                records=_records_as_json(records, owner=request.user))


@json_view
def record(request, id, name):
    """
    @api {get} /record/:id/:name Record
    @apiName record
    @apiGroup Data
    @apiVersion 1.0.0
    @apiParam {Number} id  The ID (PK) of the specified record
    @apiParam {String} name  The name  of the record (default names will be like 'r-123456789')
    @apiParamExample {curl} Example usage:
        curl -i https://mdid.domain.edu/api/record/2991/r-7388605
    @apiSuccessExample {json} Result of request ~/record/2991/r-7388605
    {"record":
        {
            "name": "r-7388605", "title": "2", "image": "/media/get/2991/r-7388605/",
                "metadata": [
                    {"value": "AH-CD0000201-890", "label": "ID"}, {"value": "2", "label": "Title"},
                    {"value": "Indiana, Robert", "label": "Creator"},
                    {"value": "1966-93", "label": "Creation Year"},
                    {"value": "Paint on aluminum.", "label": "Medium"},
                    {"value": "American", "label": "Culture"},
                    {"value": "Modern: 19th c. to present.", "label": "Period"},
                    {"value": "n/a", "label": "Style"}, {"value": "n/a", "label": "Country"},
                    {"value": "NO", "label": "Copyright Permission"}
                ],
            "thumbnail": "/media/thumb/2991/r-7388605/",
            "id": 2991
        },
        "result": "ok"
    }
    """
    # @apiSampleRequest https://mdid.domain.edu/api/record/2991/r-7388605
    record = Record.get_or_404(id, request.user)
    return dict(record=_record_as_json(record, owner=request.user))


@json_view
def presentations_for_current_user(request):

    """
    @api {get} /presentations/currentuser/ Presentations For Current User
    @apiName presentations_currentuser
    @apiGroup Presentations
    @apiVersion 1.0.0
    @apiSuccess {String} result
    @apiSuccess {Object} presentations List of Presentations owned by Request.User
    @apiSuccessExample {json}  User has presentations
    {
    "result": "ok",
    "presentations": [
        {
            "description": null, "name": "arch-search", "title": "arch search",
            "created": "2005-05-12T13:42:48", "modified": "2005-05-12T13:42:48", "hidden": false,
            "id": 338,
            "tags": [
                "MDID1 Slideshows"
            ]
        },
        {
            "description": null, "name": "catalonian-madness", "title": "Catalonian Madness!!!",
            "created": "2006-10-13T15:58:02", "modified": "2009-09-11T11:43:25",
            "hidden": false, "id": 1464,
            "tags": []
        },
      ]
    }
    @apiErrorExample {json} User has no presentations
        {"result": "ok", "presentations": []}
    @apiErrorExample {json} User is not Logged In
        {"result": "ok", "presentations": []}
        """

    def tags_for_presentation(presentation):
        ownedwrapper = OwnedWrapper.objects.get_for_object(request.user, presentation)
        return [tag.name for tag in Tag.objects.get_for_object(ownedwrapper)]

    if request.user.is_anonymous():
        return dict(presentations=[])
    presentations = Presentation.objects.filter(owner=request.user).order_by('title')
    return {
        'presentations': [
            dict(id=p.id,
                 name=p.name,
                 title=p.title,
                 hidden=p.hidden,
                 description=p.description,
                 created=p.created.isoformat(),
                 modified=p.modified.isoformat(),
                 tags=tags_for_presentation(p))
            for p in presentations
        ]
    }


@must_revalidate
@json_view
def presentation_detail(request, id):
    p = Presentation.get_by_id_for_request(id, request)
    if not p:
        return dict(result='error')

    flash = request.GET.get('flash') == '1'

    # Propagate the flash URL paramater into all image URLs to control the "Vary: cookie" header
    # that breaks caching in Flash/Firefox.  Also add the username from the request to make sure
    # different users don't use each other's cached images.
    def add_flash_parameter(url, request):
        u = create_proxy_url_if_needed(url, request)
        if flash:
            u = u + ('&' if u.find('?') > -1 else '?') \
                  + ('flash=1&user=%s' % (request.user.id if request.user.is_authenticated() else -1))
        return u

    return dict(id=p.id,
                name=p.name,
                title=p.title,
                hidden=p.hidden,
                description=p.description,
                created=p.created.isoformat(),
                modified=p.modified.isoformat(),
                content=_presentation_items_as_json(p.items.select_related('record').filter(hidden=False),
                                         owner=request.user if request.user.is_authenticated() else None,
                                         process_url=lambda url:add_flash_parameter(url, request))
            )


@must_revalidate
@json_view
def keep_alive(request):
    return dict(user=request.user.username if request.user else '')


@cache_control(no_cache=True)
def autocomplete_user(request):
    query = request.GET.get('q', '').lower()
    try:
        limit = max(10, min(25, int(request.GET.get('limit', '10'))))
    except ValueError:
        limit = 10
    if not query or not request.user.is_authenticated():
        return HttpResponse(content='')
    users = list(User.objects.filter(username__istartswith=query).order_by('username').values_list('username', flat=True)[:limit])
    if len(users) < limit:
        users.extend(User.objects.filter(~Q(username__istartswith=query), username__icontains=query)
                     .order_by('username').values_list('username', flat=True)[:limit - len(users)])
    return HttpResponse(content='\n'.join(users))


@cache_control(no_cache=True)
def autocomplete_group(request):
    query = request.GET.get('q', '').lower()
    try:
        limit = max(10, min(25, int(request.GET.get('limit', '10'))))
    except ValueError:
        limit = 10
    if not query or not request.user.is_authenticated():
        return HttpResponse(content='')
    groups = list(Group.objects.filter(name__istartswith=query).order_by('name').values_list('name', flat=True)[:limit])
    if len(groups) < limit:
        groups.extend(Group.objects.filter(~Q(name__istartswith=query), name__icontains=query)
                     .order_by('name').values_list('name', flat=True)[:limit - len(groups)])
    return HttpResponse(content='\n'.join(groups))


# commented out this file rest_framework lines are for future development of the MDID3 api


# from rooibos.api.serializers import RecordSerializer
# from rest_framework import viewsets
# from rest_framework import permissions
#
#
# class IsOwnerOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         else:
#             return obj.owner == request.user
#
#
# class RecordViewSet(viewsets.ModelViewSet):
#     queryset = Record.objects.all()
#     serializer_class = RecordSerializer
#     # probably delete this next part
#     permission_classes = (IsOwnerOrReadOnly,)
#
#     def pre_save(self, obj):
#         obj.owner = self.request.user
