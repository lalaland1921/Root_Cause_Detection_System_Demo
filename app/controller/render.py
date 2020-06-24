# -*- ecoding: utf-8 -*-
# @ModuleName: render
# @Function: 
# @Author: Yuxuan Xi
# @Time: 2020/4/28 21:38

import json
from django.http import HttpResponse


def render_json(dictionary=None):
    dictionary = {} if dictionary is None else dictionary
    response = HttpResponse(json.dumps(dictionary), content_type="application/json")
    response['Access-Control-Allow-Origin'] = '*'
    response["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type"
    response["Access-Control-Allow-Methods"] = "GET, POST, PUT, OPTIONS"
    return response