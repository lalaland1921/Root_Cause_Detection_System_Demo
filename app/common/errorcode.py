# -*- ecoding: utf-8 -*-
# @ModuleName: errorcode
# @Function: 
# @Author: Yuxuan Xi
# @Time: 2020/4/9 12:27

OP_SUCCESS = 0
THROW_EXP = 1000
OP_DB_FAILED = 1001
CHECK_PARAM_FAILED = 1002
FILE_FORMAT_ERR = 1003
NOT_POST = 1004
NOT_GET = 1005
CAL_FEATURE_ERR = 2001
READ_FEATURE_FAILED = 2002
TRAIN_ERR = 2003
WRITE_FAILED = 2004

ERR_CODE = {
    OP_SUCCESS: "操作成功",
    THROW_EXP: "抛出异常",
    OP_DB_FAILED: "数据库操作失败",
    CHECK_PARAM_FAILED: "参数检查失败",
    FILE_FORMAT_ERR: "文件格式有误",
    NOT_POST: "非post请求",
    NOT_GET: "非get请求",
    CAL_FEATURE_ERR: "特征计算出错",
    READ_FEATURE_FAILED: "读取特征数据失败",
    TRAIN_ERR: "训练出错",
    WRITE_FAILED: "写入失败"
}