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

`mongos -f /home/mongodb/conf/mongos.conf`
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




        

    