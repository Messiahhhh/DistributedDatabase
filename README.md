# DistributedDatabase
## 目录：
	1). 数据库搭建
	2). 项目开发

## 1.数据库搭建
### 教程地址
https://blog.csdn.net/kevinmcy/article/details/82712074/
### 注意事项
1、进行操作之前先使用su -进入root账户下  

2、教程中创建路由、配置、分片等的相关目录与文件这一步在执行6-10步时需要先创建/home/mongodb/log文件夹，然后用将mkdir改为touch即可  

3、所有的ip都改成自己虚拟机机器的ip，vmware虚拟机网络改成桥接模式  

4、数据库搭建好之后执行`use E_MARKET`创建项目需要的数据库  

5、搭好之后关闭mongo服务的方法  

`
ps -ef|grep mongo|grep -v grep | awk '{print $2}'|xargs kill -2  
`  

6、搭好之后快速开启mongo服务的方法  
1）三台虚拟机执行相同操作  

`
mongod -f /home/mongodb/conf/config.conf  
`  

`
mongod -f /home/mongodb/conf/shard1.conf
`  

`
mongod -f /home/mongodb/conf/shard2.conf`  

`  
mongod -f /home/mongodb/conf/shard3.conf  
`  

`mongos -f /home/mongodb/conf/mongos.conf
`  

2)在任意一台虚拟机上启动  

`mongo --host 虚拟机的ip --port 27017
`
## 2.项目开发
### 拉取项目
`git clone git@github.com:Messiahhhh/DistributedDatabase.git`

### 更改配置
进入/Database/Database/settings.py 19行代码里host=自己的ip  

`connect('E_MARKET',host='自己虚拟机的ip',port=27017,retryWrites="false")
`

### 功能编写
到/Database/e_marketSys/views.py编写自己负责的功能

### 运行
在/Database目录下输入  

`python manage.py runserver 自己电脑的ip:5000`  


对于GET请求浏览器输入  

`自己电脑ip:5000/功能函数对应的url(url在/Database/Database/url.py找对应的)  
`  

对于POST请求，使用postman模拟请求并且传递符合条件的参数  
https://www.postman.com/  

即可测试编写的功能

### 创建自己的分支  
在自己的分支上开发自己负责的功能，测试无误后合并到master  

`
git checkout -b 分支名
`  
### 过期自动删除功能  
1、解压redis到自己的电脑  

2、在redis目录下打开cmd，运行  

`
redis-server.exe redis.windows.conf
`  

启动redis服务  

2、进入项目目录执行以下指令  
`
pip install celery==5.1.2
`  

`
pip install redis==3.5.1
`  

`
pip install django-celery-beat==2.2.0
`  
3、启动项目时开三个终端，分别执行以下命令（有先后顺序）  

`python manage.py runserver 自己电脑的ip:5000`  

`celery -A Database beat -l info `  

`Celery -A Database worker -l info -P eventlet`

4、默认设置自动删除订单查询间隔为30s询问一次，如果想更改可以到`/Database/celery.py`第19行更改询问间隔  

5、pymongo的conns创建已经移入`/Database/settings.py`40行，可以绑定自己的虚拟机ip，mongoengine的连接ip在该文件的23行，也可以改成自己的虚拟机ip













        

    