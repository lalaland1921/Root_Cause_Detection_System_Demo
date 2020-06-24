# -*- ecoding: utf-8 -*-
# @ModuleName: sample_op
# @Function: 
# @Author: Yuxuan Xi
# @Time: 2020/4/9 11:51

import MySQLdb
import MySQLdb.cursors
from app.db_operation.database import DB,USER,PASSWD,HOST,PORT
from app.common.errorcode import *
import time
from app.common.common import*
import csv
import pandas as pd
import os

class DatatableOperation(object):
    def __init__(self):
        self.__conn=MySQLdb.connect(host=HOST,port=PORT,user=USER,passwd=PASSWD,db=DB,charset='utf8',cursorclass = MySQLdb.cursors.DictCursor)
        self.__cur = self.__conn.cursor()
        #self.__cur.execute("SET NAMES UTF8")

    def __del__(self):
        self.__conn.close()

    def add_data(self,data):#格式为list of list
        timestamp=time.time()
        insert_str="INSERT INTO table_of_data(name,Timepoint,root_cause) values(NULL,%s,NULL)"
        self.__cur.execute(insert_str,(timestamp,))#注意加逗号变为tuple
        lastid=self.__cur.lastrowid
        name='table'+str(lastid)
        update_str="UPDATE table_of_data SET name=%s WHERE id=%s"
        self.__cur.execute(update_str,(name,lastid))
        create_str='''DROP TABLE IF EXISTS %s;
        CREATE TABLE %s (
        id int(10) NOT NULL AUTO_INCREMENT,
        reals float NOT NULL comment '真实值',
        predict float NOT NULL comment '预测值',
        a varchar(10) NOT NULL comment 'a特征',
        b varchar(10) NOT NULL comment 'b特征',
        c varchar(10) NOT NULL comment 'c特征',
        d varchar(10) NOT NULL comment 'd特征',
        anomaly smallint(2) NULL comment '是否异常',
        PRIMARY KEY (id)
        );''' %(name,name)

    #ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;'''

        self.__cur.execute(create_str)
        format_str="(%s,%s,%s,%s,%s,%s) "
        insert_str = "INSERT INTO %s (reals,predict,a,b,c,d) values "%(name) + format_str
        '''param=[]
        for row in data:
            param.append(tuple(row))'''
        param=map(tuple,data)

        self.__cur.executemany(insert_str,param)
        self.__conn.commit()
        return OP_SUCCESS ,\
               {"tablename":name,"id":lastid,"timestamp":timestamp}  #返回操作成功以及数据数量

    '''def delete_data_by_id(self,data):#没有删除记录表中的条目
        id_num=data['id']
        select_str="SELECT name FROM table_of_data WHERE id=%s "
        self.__cur.execute(select_str,(id_num,))
        name=self.__cur.fetchone()
        if name==None:
            return CHECK_PARAM_FAILED
        delete_str="DROP TABLE %s "%(name)
        self.__cur.execute(delete_str)
        self.__conn.commit()
        return OP_SUCCESS,1'''

    '''def delete_data_by_timestamp(self,data):#删除时间小于某个节点的数据，fetchall()返回字典，这里有错误
        timestamp=data["timestamp"]
        select_str="SELECT name FROM table_of_data WHERE Timepoint < %s "
        num=self.__cur.execute(select_str,(timestamp,))
        names =self.__cur.fetchall()
        delete_str="DELETE FROM table_of_data WHERE Timepoint < %s "
        self.__cur.execute(select_str, (timestamp,))
        if names==None:
            return CHECK_PARAM_FAILED,None
        delete_str="DROP TABLE %s "
        num=0
        for name in names:
            command=delete_str%name[0]
            try:
                self.__cur.execute(command)
            except:
                continue
            num+=1
        self.__conn.commit()
        return OP_SUCCESS,num'''

    def delete_data(self,data):
        op,data=self.query_table(data)
        if OP_SUCCESS!=op:
            return op,None
        num,data=data['num'],data['data']
        names=[dct['name'] for dct in data]
        #names+=data['name']
        if names==None:
            return CHECK_PARAM_FAILED,None
        delete_str1 = "DROP TABLE %s "
        delete_str2 = "DELETE FROM table_of_data WHERE name = %s "
        for name in names:
            command=delete_str1%name
            self.__cur.execute(command)
            command=delete_str2 % name
            self.__cur.execute(command)
        self.__conn.commit()
        return OP_SUCCESS, num

    def query_table(self,data):
        params = []
        query_str = ""
        if 'beginTime' in data and 'endTime' in data:
            params.append(data['beginTime'])
            params.append(data['endTime'])
            query_str += "and Timepoint > %s and Timpepoint < %s "
        if 'root_cause' in data:
            params.append(data['root_cause'])
            query_str += "and root_cause=%s "
        if 'table_name' in data:
            params.append(data['table_name'])
            query_str += "and name=%s "
        if 'id' in data:
            params.append(data['id'])
            query_str += "and id=%s "
        if query_str == "":
            return CHECK_PARAM_FAILED, None
        # query_str="SELECT name FROM table_of_data WHERE "+query_str+' LIMIT %s, %s;'
        query_str = "SELECT name,root_cause,Timepoint FROM table_of_data WHERE " + query_str[4:]
        '''params.append(beg_limit)
        params.append(limit)'''
        num = self.__cur.execute(query_str, params)
        data = self.__cur.fetchall()
        print('query data:',data)
        if data == None:
            return CHECK_PARAM_FAILED,None
        return OP_SUCCESS,{"num":num,"data":data}

    def query_data(self,data):
        #print("name ", data["table_name"])
        '''item_per_page = data['itemPerPage']
        request_page = data['requestPage']
        beg_limit = (item_per_page * (request_page - 1))
        limit = item_per_page'''
        params = []
        name_list = []
        query_str = ""
        num=0
        if 'beginTime' in data and 'endTime' in data:
            params.append(data['beginTime'])
            params.append(data['endTime'])
            query_str += "and Timepoint > %s and Timpepoint < %s "
        if 'root_cause' in data:
            params.append(data['root_cause'])
            query_str += "and root_cause=%s "
        '''if 'table_name' in data:
            params.append(data['table_name'])
            query_str += "and name=%s "'''
        if 'id' in data:
            params.append(data['id'])
            query_str += "and id=%s "
        print("query str",query_str)
        if query_str != "":
            #return CHECK_PARAM_FAILED, None
        # query_str="SELECT name FROM table_of_data WHERE "+query_str+' LIMIT %s, %s;'
            query_str = "SELECT name FROM table_of_data WHERE " + query_str[4:]

            num = self.__cur.execute(query_str, params)
            names = self.__cur.fetchall()#这里返回的是字典
            if names:
                for name in names:
                    name_list.append(name[0])

        name_list+=data["table_name"]
        print("name list",name_list)
        if name_list == None:
            return CHECK_PARAM_FAILED, None

        query_str="SELECT * FROM %s"
        ret_data={}
        for name in name_list:
            command=query_str%name
            self.__cur.execute(command)
            table=self.__cur.fetchall()
            table=pd.DataFrame(table)
            ret_data[name]=table
        '''total_page = total_count / item_per_page
        current_page = min(request_page, total_page)'''
        return OP_SUCCESS,{"num":num,"data":ret_data}

    def query_all_table(self):
        select_str="SELECT * FROM table_of_data"
        num=self.__cur.execute(select_str)
        table_info=self.__cur.fetchall()
        table_info=pd.DataFrame(table_info)
        return OP_SUCCESS,table_info

    def download_data(self,data):
        #data_list=[]
        id_list = data.split(',')
        format_strings = ','.join(['%s'] * len(id_list))
        command="SELECT name FROM table_of_data WHERE id in (%s)"% format_strings
        self.__cur.execute(command, id_list)
        name_list=self.__cur.fetchall()
        select_str="SELECT * FROM %s"
        head=["id","真实值",'预测值',"a特征","b特征","c特征","d特征","是否异常"]
        #os.chdir('tmp')
        for name in name_list:
            select_command=select_str%(name[0])
            self.__cur.execute(select_command)
            table=self.__cur.fetchall()
            down_load_file_path=DOWNLOAD_FILE_PATH%name[0]
            #try:
            #os.mknod(down_load_file_path)
            with open(down_load_file_path, 'w',encoding='utf-8-sig') as pfile:
                writer = csv.writer(pfile)
                writer.writerow(head)
                writer.writerows(table)
            #except:
                #return WRITE_FAILED,{"failed_file_name":name[0]}
        return OP_SUCCESS,name_list



    '''def download_data(self,data):#还有问题！
        pardir=os.path.pardir
        os.chdir(pardir)
        print(os.getcwd())
        id_num=data["id"]
        command="SELECT name FROM table_of_data WHERE id =%s"
        self.__cur.execute(command, (id_num,))
        name=self.__cur.fetchone()
        select_str="SELECT * FROM %s INTO OUTFILE "%name[0] +"%s "
        down_load_file_path = DOWNLOAD_FILE_PATH % name[0]
        select_str=select_str%down_load_file_path
        self.__cur.execute(select_str)
        return OP_SUCCESS,down_load_file_path
        '''

    def add_root_causes(self,data:{}):#{table_name:root_cause}
        params=[]
        table_names=data.keys()
        command="UPDATE table_of_data set root_cause=%s WHERE name=%s"
        for table_name in table_names:
            params.append(tuple([data[table_name],table_name]))
        num=self.__cur.executemany(command,params)
        self.__conn.commit()
        return OP_SUCCESS,num

    def add_anomaly(self,data):
        table_name=data["name"]
        id_list=data['id']
        format_strings = ','.join(['%s'] * len(id_list))
        command = "UPDATE %s SET anomaly=0"%table_name
        self.__cur.execute(command)
        command="UPDATE %s SET anomaly=1 WHERE id in (%s)"%(table_name,format_strings)
        num=self.__cur.execute(command,id_list)
        self.__conn.commit()
        return OP_SUCCESS,num




if __name__ == '__main__':
    op=DatatableOperation()
    #data=[['1.0','2.0','a1','b2','c3','d4']]
    #print(op.add_data(data))

    '''data={"id":22}
    print(op.delete_data_by_id(data))'''
    #print(op.delete_data_by_timestamp({"timestamp":1587048395.1941006}))

    #print(op.query_data({'table_name':["table73"]}))
    #print(op.download_data("38"))
    #print(op.add_root_causes({52:"a3b3c3d3"}))
    #print(op.add_anomaly({"name":"table52","id":[0,1]}))
    #print(op.download_data({"id":52}))
    #print(op.query_all_table())
    print(op.delete_data({'table_name':["table73"]}))