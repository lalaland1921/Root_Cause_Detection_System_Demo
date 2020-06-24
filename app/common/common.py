# -*- ecoding: utf-8 -*-
# @ModuleName: common
# @Function: 
# @Author: Yuxuan Xi
# @Time: 2020/4/16 14:01

import traceback
from functools import wraps
from app.common.errorcode import *

DOWNLOAD_FILE_PATH='tmp/tmpfile_%s.csv' #初始化的时候要用命令新建
UPLOAD_FILE_PATH='tmp/uploadfile_%s.csv'
VALUE_LEN_MAX = 50000
attributes=['a','b','c','d']


def build_ret_data(ret_code, data=""):
    return {"code": ret_code, "msg": ERR_CODE[ret_code], "data": data}


def exce_service(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            ret_code, ret_data = func(*args, **kwargs)
            return_dict = build_ret_data(ret_code, ret_data)
        except Exception as ex:
            traceback.print_exc()
            return_dict = build_ret_data(THROW_EXP, str(ex))
        return return_dict
    return wrapper