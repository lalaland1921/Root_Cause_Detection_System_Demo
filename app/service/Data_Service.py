# -*- ecoding: utf-8 -*-
# @ModuleName: Sample_Service
# @Function: 
# @Author: Yuxuan Xi
# @Time: 2020/4/23 15:12

import json
#import traceback
#import csv
from app.db_operation.datatable_op import *
from app.common.errorcode import *
from app.common.common import *
import uuid
import pandas as pd

class DataService(object):

    def __init__(self):
        self.__data_op=DatatableOperation()
        uuid_str=uuid.uuid4().hex[:8]
        self.__upload_file_path=UPLOAD_FILE_PATH%uuid_str

    @exce_service
    def import_data(self,data):#:list of list
        return self.__data_op.add_data(data)

    def import_file(self,file_data):
        try:
            pfile=file_data.get('file')
            with open(self.__upload_file_path,'wb+') as destination:
                for chunk in pfile.chunks():
                    destination.write(chunk)

            df=pd.read_csv(self.__upload_file_path)#假设文件形式为样本中的那样
            #print("dataframe",df.head(5))
            data=df.values

        except Exception as ex:
            traceback.print_exc()
            return_dict=build_ret_data(FILE_FORMAT_ERR,str(ex))
            return return_dict
        import_ret=self.import_data(data)
        return import_ret

    @exce_service
    def delete_data(self,body):
        return self.__data_op.delete_data(body)

    @exce_service
    def query_table(self,body):
        return self.__data_op.query_table(json.loads(body))

    @exce_service
    def query_data(self,body):
        return self.__data_op.query_data(body)

    @exce_service
    def query_all_table(self):
        return self.__data_op.query_all_table()

    def data_download(self,body):
        ret_code=THROW_EXP
        try:
            if len(body)>VALUE_LEN_MAX:
                return ""
            ret_code,ret_data=self.__data_op.download_data(body)
        except Exception as ex:
            traceback.print_exc()
            ret_data=build_ret_data(THROW_EXP,str(ex))
        return ret_code,ret_data




