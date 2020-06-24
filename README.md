# Root_Cause_Detection_System_Demo
一个部署在windows本地主机上的根因分析系统，作为数据库，网页开发练手的小demo，细节待完善
算法部分基于[squeeze](https://github.com/lalaland1921/Squeeze),数据库操作接口在app中，基于MySQLdb，前端基于Django，网页部分写的很粗糙，为经过渲染，可以实现简单的文件上传（本地），数据可视化，根因检测，文件删除功能
## get started
新建数据库，并根据数据库名称修改db_operation/database中的参数，在该数据库中运行sql文件夹中的三个sql文件，对数据库进行初始化，会生成一个数据样表，和管理数据表的table of data
数据可从[Tsinghua Cloud](https://cloud.tsinghua.edu.cn/d/0bc5a68ce2764a0d8215/)下载
## 打开网页
cd到controller目录下
执行py manage.py runserver
