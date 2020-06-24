from django.shortcuts import render
# -*- coding: utf-8 -*-
# Create your views here.
import json
from functools import wraps
from django.shortcuts import render
import sys
sys.path.append("..")
sys.path.append("..\..")
sys.path.append("..\..\..")
sys.path.append("..\..\..\..")
from django.http import FileResponse,HttpResponse
from app.controller.render import render_json
from app.service.Data_Service import *
from app.service.Detect_Service import *
from app.common.errorcode import *
from app.common.common import *
from django.template import loader
import time

def unescapeHTML(html):
    html=html.replace("&lt;","<")
    html=html.replace("&gt;",">")
    return html

def check_post(func):
    @wraps(func)
    def f(request):
        if request.method =="POST":
            return_dct=func(request)
        else:
            return_dct=build_ret_data(NOT_POST)
        return render_json(return_dct)
    return f


def index(request):

    template = loader.get_template('index.html')
    data_service = DataService()
    context = data_service.query_all_table()
    if context['code']!=0:return HttpResponse(template.render({}, request))
    df=context['data']
    #df['name'] = df['name'].apply(lambda x: "<a href=\"{% url 'search_data' %}\"><b>"+x+"</b></a>")
    df['name'] = df['name'].apply(lambda x: "<a href=\""+x+"/"+"\"><b>" + x + "</b></a>")
    df['Timepoint']=df['Timepoint'].apply(lambda x:time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(x)) )
    #df['root_cause']=df['root_cause'].apply(lambda x: '''<form action=\"\" method=\"post\">
    #                                                  <button name=\"foo\" value=\"detect\">'''+
      #                                                x+" detect</button></form> </form>")
    print(context)
    html=df.to_html()
    html=unescapeHTML(html)
    context['data']=html
    return HttpResponse(template.render(context, request))
    #return HttpResponse('hello')

#@check_post
def import_data(request):
    #file=request.FILES.get('file')
    #print("the request is:",file['data_file'],"end")

    template = loader.get_template('import_data.html')
    data_service=DataService()
    context=data_service.import_file(request.FILES)
    if context['code'] != 0: return HttpResponse(template.render({}, request))
    table_name=context['data']['tablename']
    context['data']['data'] = data_service.query_data({'name': [table_name]})
    # print(context)

    if context['data']['data']['code']==0:
        df = context['data']['data']['data']['data'][table_name]
        html = df.to_html()
        html = unescapeHTML(html)
        context['data']['data'] = html
    #return render(request, "index.html")
    return HttpResponse(template.render(context, request))

#@check_post
def delete_data(request,table_name):
    template = loader.get_template('delete.html')

    data_service=DataService()
    context=data_service.delete_data({'table_name':[table_name]})
    print(context)
    return HttpResponse(template.render(context, request))

#@check_post
def search_table(request):
    data_service=DataService()
    return data_service.query_table(request.body)


def search_data_by_name(request,table_name):
    #print("request:",request)
    #print("runing search data by name,table name:",table_name)

    data_service = DataService()
    detect_service = DetectService()
    if request.method == "POST":
        template = loader.get_template('detect.html')
        context=detect_service.Detect({'table_name':table_name})
        print("detect info:", context)
        context['ret_data']=context['data']['ret_data'][table_name]

        return HttpResponse(template.render(context, request))

    template = loader.get_template('search_data_by_name.html')
    context=data_service.query_data({'table_name':[table_name]})
    print(table_name, context)
    if context['code']!=0:return HttpResponse(template.render({}, request))
    df=context['data']['data'][table_name]
    html = df.to_html()
    html = unescapeHTML(html)
    context['data'] = html
    context['name']=table_name

    return HttpResponse(template.render(context, request))

@check_post
def search_all_table(request):
    data_service=DataService()
    return data_service.query_all_table(request.body)

def data_download(request):
    if request.method=="GET":
        try:
            data_service=DataService()
            ret_code,file_name=data_service.data_download(request.GET['id'])
            files=open(file_name,'rb')
            response=FileResponse(files)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename = "SampleExport.csv"'
            return response
        except Exception as ex:
            return_dict=build_ret_data(THROW_EXP,str(ex))
            return render_json(return_dict)
    else:
        return_dict=build_ret_data(NOT_GET)
    return render_json(return_dict)

@check_post
def detect(request):
    detect_service=DetectService()
    return detect_service.Detect(json.loads(request.body))