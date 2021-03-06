from config.settings_local import DEBUG
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from rooibos.workers.models import JobInfo
from django.template import RequestContext
from rooibos.ui.views import select_record
import json
from rooibos.access.models import AccessControl, ExtendedGroup, AUTHENTICATED_GROUP
from rooibos.data.models import Collection, Record, standardfield, CollectionItem, Field, FieldValue
from django.conf.urls import *
from urllib import urlencode
from rooibos.unitedsearch import query_parser, common, aggregate, searchers, ResultRecord, ResultImage, RecordImage  
from rooibos.unitedsearch import (ScalarParameter, OptionalParameter, DefinedListParameter, UserDefinedTypeParameter,
MapParameter, ListParameter, OptionalDoubleParameter, OptionalTripleParameter, DoubleParameter)
from rooibos.unitedsearch.external.gallica_parser import *
from common import *
from query_parser import parse
import common
import searchers
import sys
import traceback

class usViewer():

    def __init__(self, searcher, mynamespace):
        self.urlpatterns = patterns('',
            url(r'^search/', self.search, name='search'),
            url(r'^select/', self.select, name='select'))
        self.searcher = searcher
        self.namespace = mynamespace
    
    def url_select(self):
        return reverse(self.namespace + ':select')
    
    def url_search(self):
        return reverse(self.namespace + ':search')
    
    def __url_search_(self, params={}):
        u = self.url_search()
        return u + (("&" if "?" in u else "?") + urlencode(params) if params else "")
    
    def sort_keys(self,reversed_keys):
                if "field" in reversed_keys:
                    reversed_keys.remove("field")
                    reversed_keys.insert(0,"field")
                if "keywords" in reversed_keys:
                    reversed_keys.remove("keywords")
                    reversed_keys.insert(0,"keywords")
                if "all words" in reversed_keys:
                    reversed_keys.remove("all words")
                    reversed_keys.insert(0,"all words")
                if "start year" in reversed_keys:
                    reversed_keys.remove("start year")
                    reversed_keys.append("start year")
                if "end year" in reversed_keys:
                    reversed_keys.remove("end year")
                    reversed_keys.append("end year")
                if "start date" in reversed_keys:
                    reversed_keys.remove("start date")
                    reversed_keys.append("start date")
                if "end date" in reversed_keys:
                    reversed_keys.remove("end date")
                    reversed_keys.append("end date")
                return reversed_keys
    
    def htmlparams(self, defaults):    
        def out(params, indent, prefix, default):
            if DEBUG:
                print "reached 'out' method"
                print "params = " + str(params)
            label = params.label if params.label else " ".join(prefix)
            if isinstance(params, DefinedListParameter):
                options = params.options or []
                r_content = "  "*indent + (label + ": " if params.label else "") 
                r_content += "<select name=\"i_" + "_".join(prefix) + "\""
                if params.multipleAllowed :
                    r_content += " multiple = \"multiple\""
                r_content += ">"
                selected = options[0]
                if default:
                    selected = default
                  
                for option in options :
                    if option == selected:
                        r_content += "<option selected=\"selected\" value=" + '\"'+option+'\"'
                    else: 
                        r_content += "<option value=" + '\"'+option+'\"'
                    r_content += ">" + option + "</option>"
                r_content += "</select><br>"
                return [r_content]
            
            elif isinstance(params, MapParameter):
                if DEBUG: 
                    print "reached instance of MapParameter)"
                r = ["  "*indent + "<div>"]
                reversed_keys = params.parammap.keys()
                reversed_keys = self.sort_keys(reversed_keys)
                keys=[]
                while len(reversed_keys)>0:
                    keys.append(reversed_keys.pop())
                
                for index in range(len(params.parammap)-1, -1, -1) :
                #for k in params.parammap:
                    k = keys[index]
                    r += out(params.parammap[k], indent + 1, prefix + [k],
			default != None and default[k] != None and default[k])
                r += ["  "*indent + "</div>"]
                return r
            elif isinstance(params, ListParameter):
                r = ["  "*indent + (label + ": " if params.label else "")+"<div>"]
                index =0
                i = 0
                for v in params.paramlist :
                    r += out(v, indent+1, [str(prefix[0])+str(index)], default and default[i] or None)
                    index = index+1
                    i = i+1
                r += ["  "*indent + "</div>"]
                return r
            elif isinstance(params, DoubleParameter):
                r = ["  "*indent + "<div>"]                
                r += out(params.subparam1, indent + 1, prefix , default and default[0] or None)
                r += out(params.subparam2, indent + 1, prefix , default and default[1] or None)

                r += ["  "*indent + "</div>"]
                return r
            elif isinstance(params, ScalarParameter):
                if DEBUG:
                    print "reached instance of ScalarParameter"
                return ["  "*indent + (label + ": " if params.label else "") + "<input type=\"text\" name=\"i_" + "_".join(prefix) + "\" value=\"" + (default or "") + "\" />"]
         
            elif isinstance(params, OptionalParameter):
                r = ["  "*indent + "<div>"]
                indent += 1
                r += ["  "*indent + "<input name=\"i_" + "_".join(prefix+ ["opt"]) + "\" type=\"checkbox\" class=\"param-opt-a\"" + (" checked=\"true\"" if default else "") + "> " + label]
                r += ["  "*indent + "<div class=\"param-opt\">"]
                r += out(params.subparam, indent + 1, prefix , default and default[0] if isinstance(default, list) else default or None)
                r += ["  "*indent + "</div>"]
                indent -= 1
                r += ["  "*indent + "</div>"]
                return r
            elif isinstance(params, OptionalDoubleParameter):
                r = ["  "*indent + "<div>"]
                indent += 2
                r += ["  "*indent + "<input name=\"i_" + "_".join(prefix+ ["opt"]) + "\" type=\"checkbox\" class=\"param-opt-a\"" + (" checked=\"true\"" if default else "") + "> " + "Add Field"]
                r += ["  "*indent + "<div class=\"param-opt\">"]
                r += out(params.subparam1, indent + 1, prefix , default and default[0] or None)
                r += out(params.subparam2, indent + 1, prefix , default and default[1] or None)
                r += ["  "*indent + "</div>"]
                indent -= 2
                r += ["  "*indent + "</div>"]
                return r
            elif isinstance(params, UserDefinedTypeParameter) :
                options = params.type_options or []
                r_content = "  "*indent + (label + ": " if params.label else "")
                r_content += "<div>"
                # select box for the type options
                r_content += "<select name=\"i_" + "_".join(prefix) +"_type"+ "\">"
                selected = options[0]
                if default:
                    selected = default[0]
                for option in options :
                  if option == selected:
                      r_content += "<option selected=\"selected\" value=" + option
                  else: 
                      r_content += "<option value=" + option
                  r_content += ">" + option + "</option>"
                r_content += "</select><br>"
                # textbox for value
                if default and len(default) >0:
                  value = default[1]
                else:
                  value = ""
                r_content += "<input name=\"i_" + "_".join(prefix)+"_value" + "\" type=\"text\" value=\"" + value + "\" />"
                r_content += "</div>"
                return [r_content]        
        if DEBUG:
            print "SEARCHER PARAMETERS: " + str(self.searcher.parameters)
        return "\n".join(out(self.searcher.parameters, 0, [], defaults))

    """
    def readargs(self, getdata):
        inputs = dict([(n[2:], getdata[n]) for n in getdata if n[:2] == "i_"])
        def read(params, prefix):
            if isinstance(params, MapParameter):
                r = {}
                for k in params.parammap:
                    if k in r :
                      r[k].append(read(params.parammap[k], prefix + [k]))
                    else :
                      r[k] = read(params.parammap[k], prefix + [k])
                return r
            if isdigitalnzinstance(params, ListParameter):

                r = []
                index = 0
                for v in params.paramlist:
                      r.append(read(v, prefix+[str(index)]))
                      index = index+1
                return r
            if isinstance(params, ScalarParameter):
                if "_".join(prefix) in inputs:
                    return inputs["_".join(prefix)]
            if isinstance(params, OptionalParameter):
                return [read(params.subparam, prefix + ["opt"])] if inputs.get("_".join(prefix), "off") == "on" else []
            if isinstance(params, DefinedListParameter):
                if "_".join(prefix) in inputs:
                    return inputs["_".join(prefix)]

            if isinstance(params, UserDefinedTypeParameter) :
                field_type = ""
                field_value = ""
                if "_".join(prefix)+"_type" in inputs:
                    field_type = inputs["_".join(prefix)+"_type"]
                if "_".join(prefix)+"_value" in inputs:
                    field_value = inputs["_".join(prefix)+"_value"]
                return field_type, field_value
                #if "_".join(prefix) in inputs:
                #   return inputs["_".join(prefix)]
        return read(self.searcher.parameters, [])
    """
    def perform_search(self, request, resultcount):
        searcher_identifier = self.searcher.identifier
        all_query = request.GET.copy()

        offset = request.GET.get('from', '') or request.POST.get('from', '') or "0"
        query, params = parse(request,searcher_identifier)
        
        result,args = self.searcher.search(query, params, offset, resultcount)
        results = result.images
        def resultpart(image):
            if isinstance(image, ResultRecord):
                return {
                    "is_record": True,
                    "thumb_url": image.record.get_thumbnail_url(),
                    "title": image.record.title,
                    "record_url": image.record.get_absolute_url(),
                    "identifier": image.record.id
                }
            else:
                return {
                    "thumb_url": image.thumb,
                    "title": image.name,
                    "record_url": image.infourl,
                    "identifier": image.identifier,
                    "content_provider" : image.content_provider
                }

        prev_off = hasattr(self.searcher, "previousOffset") and self.searcher.previousOffset(offset, resultcount)
        prev = None
        if int(offset)>0 :
          prev_off =int(offset)-resultcount
          if prev_off > int(result.total):
            prev_off = result.total-len(result.images)-resultcount
          if prev_off <0:
            prev_off=0
          all_query.update({'from':prev_off})
          prev = self.__url_search_(all_query)
        nextPage = None
        firstPage = None
        lastPage = None
        if int(offset)>0:
          all_query.update({'from':0})
          firstPage = self.__url_search_(all_query)
        if (int(result.nextoffset)<int(result.total)):
          all_query.update({'from':result.nextoffset})
          nextPage = self.__url_search_(all_query)
        if (nextPage):
          num_lastPageResult = result.total%resultcount
          if num_lastPageResult==0:
            num_lastPageResult=resultcount
          lastOffset = result.total-num_lastPageResult
          all_query.update({'from':lastOffset})
          lastPage = self.__url_search_(all_query)
        query_language = ""
        if "simple_keywords" in args:
            query_language = args["simple_keywords"]
        if "query_string" in args:
            query_language = args["query_string"]
        return {
                'results': map(resultpart, results),
                'select_url': self.url_select(),
                'next_page': nextPage,
                'previous_page': prev, 
                'first_page': firstPage,
                'last_page' :lastPage,
                'hits': result.total,
                'searcher_name': self.searcher.name,
                'searcher_logo': self.searcher.get_logo(),
                'searcher_url': self.searcher.get_searcher_page(),
                'html_parameters': self.htmlparams(args),
                'query': query_language
            }
        
    def search(self, request):
        a = self.perform_search(request,50)
        return render_to_response('searcher-results.html', a, context_instance=RequestContext(request))

    def record(self, identifier):
        image = self.searcher.getImage(identifier)
        print(image.thumb)
        if isinstance(image, ResultRecord):
            return image.record
        #checking if image is accessible -- if not, then replace
        # thumbnail with 'thumb. unav.'
        try:
            request = urllib2.Request(image.url)
            request.get_method = lambda : 'HEAD'
            #proxy_opener = common.proxy_opener()
            #response = proxy_opener.open(request)
        except urllib2.URLError, ex:
            print(ex)
            image.thumb = "/static/images/thumbnail_unavailable.png"
            # need to change the image thumbnail url to 'thumbnail unav.' here
			
        print("About to build Record")
        print(image.thumb)
        record = Record.objects.create(
						name=image.name,
                        source=image.url,
                        tmp_extthumb=image.thumb,
                        manager='unitedsearch')
        def add_field(f, v, o):
            if type(v) == list:
                for w in v:
                    add_field(f, w, o)
            elif v:
                # TODO: neaten?
                try:
                    FieldValue.objects.create(
                        record=record,
                        field=standardfield(f),
                        order=o,
                        value=v)
                except:
                    pass
        n = 0
        # go through the metadata given by the searcher; just add whatever can be added---what are not standard fields are simply skipped.
        for field, value in dict(image.meta, title=image.name).iteritems():
            add_field(field, value, n)
            n += 1
        collection = get_collection()
        CollectionItem.objects.create(collection=collection, record=record)
        """
        This is where we should add the full image to the database and download it 
        """
		
        job = JobInfo.objects.create(func='unitedsearch_download_media', arg=json.dumps({
            'record': record.id,
            'url': image.url
        }))
        job.run()
        
        
        
        
        return record

    def select(self, request):
        if not request.user.is_authenticated():
            raise Http404()

        if request.method in "POST":
            # TODO: maybe drop the unused given-records portion of this
            postid = request.POST.get('id', '[]')
            imagesjs = json.loads(postid.strip("[]"))
            images = [self.searcher.getImage(imagesjs)]
            urlmap = {}
            for i in images:
                urlmap[i.record.get_absolute_url() if isinstance(i, ResultRecord) else i.url]=i
            urls = urlmap.keys()
            ids = dict(Record.objects.filter(source__in=urls, manager='unitedsearch').values_list('source', 'id'))
            result = []
            for url in urls:
                id = ids.get(url)
                if id:
                    result.append(id)
                else:
                    i = urlmap[url].identifier
                    record = self.record(i)
                    result.append(record.id)
            r = request.POST.copy()
            r['id'] = json.dumps(result)
            request.POST = r
        ans = select_record(request)
        return ans

class usUnionViewer(usViewer):
    def __init__(self, searcher):
        usViewer.__init__(self, searcher, None)
    
    def url_select(self):
        return reverse("united:union-select", kwargs={"sid": self.searcher.identifier})

    def url_search(self):
        return reverse("united:union-search", kwargs={"sid": self.searcher.identifier})

searchersmap = dict([(s.identifier, s) for s in searchers.all])

def union(request, sid):
    from union import searcherUnion
    slist = map(searchersmap.get, sid.split(","))
    searcher = slist[0] if len(slist) == 1 else searcherUnion(slist)
    return usUnionViewer(searcher)

def union_select(request, sid="local"):
    return union(request, sid).select(request)

def union_search(request, sid="local"):
    return union(request, sid).search(request)

    
def get_params(request):
        params = {}
        for key in request.GET:
            if key.startswith('i_'):
                params.update({key[2:]:request.GET[key]})
        keys = params.keys()
        for key in keys:
            key2 = key+"_opt"
            if key in params and key2 in params:
                params.update({key:params[key2]})
                del params[key2]
        return params    
# Todo: remove this into translator?
all_words_map = {
    'gallica' : 'all',
    'nga' : 'all words'
}
