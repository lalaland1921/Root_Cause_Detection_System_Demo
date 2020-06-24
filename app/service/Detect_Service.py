# -*- ecoding: utf-8 -*-
# @ModuleName: Detect_Service
# @Function: 
# @Author: Yuxuan Xi
# @Time: 2020/4/23 9:36

from app.db_operation.datatable_op import DatatableOperation
from algorithm.Squeeze import Squeeze
from app.service.arguments import args
from app.common.errorcode import*
from app.common.common import *
import pandas as pd
from functools import reduce

class DetectService(object):

    def __init__(self):
        self.data_op_obj =DatatableOperation()

    def Detect(self,param):  #对所有的数据进行检测
        op,data=self.data_op_obj.query_table(param)
        if op!=OP_SUCCESS:
            return build_ret_data(op,{})
        total_num,datas=data['num'],data['data']
        ret_data={}
        for data in datas:
            name=data['name']
            rt_cause=data['root_cause']
            time_point=data['Timepoint']
            if rt_cause!=None:
                ret_data[name]=rt_cause
                continue
            op,data=self.data_op_obj.query_data({"name":[name]})
            if op!=OP_SUCCESS:return op
            full=data['data'][name]

            data={}
            dct={}
            for i in range(len(full)):#对数据进行预处理，将dataframe转化为字典，attr:(real,pre)形式,空间复杂度有点高，更好的办法是把dataframe直接送进去
                attrs = tuple([int(full.iloc[i][attr][1:]) for attr in attributes])
                data[attrs] = tuple([full.iloc[i]['reals'],full.iloc[i]['predict']])
                dct[attrs]=full.iloc[i]['id']
            self.detect=Squeeze(data=data,thre=args['thre'],theta=args['theta'])
            anomaly_attrs=reduce(lambda x,y:x+y,self.detect.idata.values())#记录异常的数据attr
            anomaly_ids=[dct[attr] for attr in anomaly_attrs]#记录异常数据的id
            self.data_op_obj.add_anomaly({'name':name,'id':anomaly_ids})
            root_causes = list(set(self.detect.root_causes))
            root_causes_str = ';'.join(root_causes)
            ret_data[name]=root_causes_str
        op,num_changed=self.data_op_obj.add_root_causes(ret_data)
        if op!=OP_SUCCESS:
            return build_ret_data(op,{})
        return build_ret_data(OP_SUCCESS,{"total_num":total_num,"num_changed":num_changed,'ret_data':ret_data})

if __name__ == '__main__':
    detect_service=DetectService()
    ret_data=detect_service.Detect({'table_name':'table74'})
    print(ret_data)



