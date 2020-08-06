***一.目录***   
***Common***   
Common文件夹下包含EMail.py,http_requesrt.py,readConfig.py,readjson.py,thrift_client.py
Email.py实现发送测试报告到收件人邮箱;包含send_email()方法&&初始化方法 __init__(self)
 __init__(self)
```

    def __init__(self):
        readconf = readconfigs()
        self.smtpserver = readconf.get_emailconf('smtpserver')#获取配置文件信息smtpserver
        self.port = readconf.get_emailconf("port")#获取配置文件信息port
        self.username = readconf.get_emailconf('username')#获取配置文件信息邮箱账户username
        self.password = readconf.get_emailconf('password')#获取配置文件信息邮箱密码password
        self.sender = readconf.get_emailconf('sender')#获取配置文件信息发送邮箱sender
        self.receivers = eval(readconf.get_emailconf('receivers'))#获取配置文件信息收件人邮箱receivers
        self.mail_cclist=eval(readconf.get_emailconf('mail_cclist'))#获取配置文件信息抄送人邮箱mail_cclist
        self.subject = readconf.get_emailconf('subject')#获取配置文件信息邮件主题subject
        file = readconf.get_emailconf('sendfile')#获取配置文件信息测试报告目录sendfile
        self.sendfile = open(file, 'r', encoding="utf-8").read()
```

send_email()
```
#!/usr/bin/env python3
    def send_email(self):
        try:
            smtp = smtplib.SMTP()
            print(self.smtpserver,self.port)
            smtp.connect(self.smtpserver, port=self.port)
            smtp.ehlo()
            # smtp.starttls()
            print(self.username, self.password)
            smtp.login(user=self.username, password=self.password)
            smtp.sendmail(from_addr=self.sender, to_addrs=self.receivers, msg=self.attach_setup())
            smtp.quit()
        except smtplib.SMTPException:
            print("邮件发送失败！！")
        else:
            print("邮件发送成功！！")
```
http_requesrt.py实现了对HTTP协议的get,post,put,delete方法的封装;通过调用post&&get方法之后来获取其属性
Http_client.text是请求结果一个str类型对象,而Http_client.jsonBody是请求结果的一个dict类型对象;Http_client.status_code返回的状态码;Http_client.elapsed返回的总耗时,单位s

```

class Http_client():
    # 初始化api数据
    def __init__(self, ):
        readconfig = readconfigs()
        self.host = readconfig.get_http('baseUrl')
        self.timeout = float(readconfig.get_http('timeout'))
        self.status_code = None
        self.text = None
        # 一个str类型reponsedata对象
        self.jsonBody = None
        # 一个dict类型reponsedata对象
        self.headers = None
        self.URL = None
        self.elapsed = None
        # 完成一个请求总耗时，单位s
```
readConfig.py实现读取config.inin中数据;通过get_db(self, name),get_http(self, name),get_thriftSocket(self, name),get_emailconf(self, name)来获取你想要的数据
```

    # 获取[database]的配置信息
    def get_db(self, name):
        value = self.conf.get("database", name).strip("'").strip('"')
        if str(name).lower() == "port":
            value = int(value)
        else:
            return value
        return value

    # 获取[HTTP]的配置信息
    def get_http(self, name):
        value = self.conf.get("HTTP", name).strip("'").strip('"')
        return value

    # 获取[thriftSocket]配置信息
    def get_thriftSocket(self, name):
        value = self.conf.get("thriftSocket", name).strip("'").strip('"')
        return value

    def get_emailconf(self, name):
        value = self.conf.get("Email", name).strip("'").strip('"')
        return value
```
readjson.py读取Test_data中的json数据(暂时未使用到)

thrift_client.py 封装了thrift客户端连接client,使用之前import即可,声明对象时需要传入具体的service,例如:Thrift_client(ncTShareMgnt)
```

class Thrift_client(object):
    def __init__(self,service):
        readconf = readconfigs()
        self.host = readconf.get_thriftSocket("host")
        self.port = readconf.get_thriftSocket("port")

        transport = TSocket.TSocket(self.host, self.port)
        # 创建一个传输层对象（TTransport），设置调用的服务地址为本地，
        # 端口为 9090,TSocket传输方式
        self.transport = TTransport.TBufferedTransport(transport)
        self.protocol = TBinaryProtocol.TBinaryProtocol(transport)
        # 创建通信协议对象（TProtocol），设置传输协议为 TBinaryProtocol
        self.client = service.Client(self.protocol)
        # 创建一个Thrift客户端对象
        self.transport.open()
        print("transport已连接")

    def ping(self):
        self.client.ping()

    def close(self):

        self.transport.close()
```
使用EX:
```

from ThriftAPI.gen_py_tmp.ShareMgnt import ncTShareMgnt
from Common.thrift_client import Thrift_client
import os

UserUUid = "9fce4db8-f5fa-11e9-a3b1-005056828221"


def test_Usrm_GetUserInfo():
    tc = Thrift_client(ncTShareMgnt)
    response = tc.client.Usrm_GetUserInfo(UserUUid)
    assert response.user.loginName == 'ddd'
    #  assert断言，实际结果response和期望结果比较
    # assert response.user.email == 'ddd'
    print('body方法返回的信息为：', response)
    tc.close()

```
*****
*****

***DB_connect***   
 DB_connect.mysqlconnect.py实现对mySQL数据的连接,新增&&修改&&删除&&查询单条数据&&查询多条数据
新增数据
```
   # 插入表中数据
    def insert(self, sql):
        try:
            if "insert" in sql.lower() and "into" in sql.lower():
                self.open()
                row = self.cursor.execute(sql)
                self.db.commit()
                print("insert successfully! the number of rows affected:%d" % row)
            else:
                print("SQL syntax error, please enter insert into!")
                return
        except Exception as e:
            self.db.rollback()
            print('execute failure', e)
        self.close()
```
修改数据
```
 # 更新表中数据
    def update(self, sql):
        try:
            if "update" in sql.lower():
                self.open()
                row = self.cursor.execute(sql)
                self.db.commit()
                print("update successfully! the number of rows affected:%d" % row)
            else:
                print("SQL syntax error, please enter update!")
                return
        except Exception as e:
            self.db.rollback()
            print('execute failure', e)
        self.close()
```
删除数据,注:谨慎使用!主要用于清除一下脏数据.
```
  # 删除表中数据
    def delete(self, sql):
        try:
            if "delete" in sql.lower():
                self.open()
                row = self.cursor.execute(sql)
                self.db.commit()
                print("delete successfully! the number of rows affected:%d" % row)
            else:
                print("SQL syntax error, please enter delete!")
                return
        except Exception as e:
            self.db.rollback()
            print('execute failure', e)
        self.close()
```
查询第一条数据
```
    def select_one(self, sql):
        try:
            if "select" in sql.lower():
                self.open()
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                print(result)
            else:
                print("SQL syntax error, please enter select!")
                return
        except Exception as e:
            print('execute failure', e)
        self.close()
```
查询所有的数据
```
    # 查询表中所有数据
    def select_all(self, sql):
        try:
            if "select" in sql.lower():
                self.open()
                self.cursor.execute(sql)
                result = self.cursor.fetchall()
                print(result)
            else:
                print("SQL syntax error, please enter select!")
                return
        except Exception as e:
            print('execute failure', e)
        self.close()
```
*****
*****

***Report***  
allure测试报告&&测试数据存放目录   
***Test_data***   
存放测试数据txt,json,csv,excel等文件的目录        
***Testcase***   
所有测试用例存放目录，包含HTTP协议和Thrift协议的API接口测试用例   
1.***httpcase***     
HTTP协议的测试用例集   
2.***thriftcase***   
***ThrinfAPI***   
Thrift协议的API接口测试用例     
***config.ini***   
核心的配置文件信息    
***install_dependencies.py***   
安装的第三方依赖包    
***README.md***   
***run.py***    
执行程序入口，包含pytest各种执行模式    
 
***二.环境搭建***   
使用的语言: python 3.7+     
通过pip3安装的第三方依赖：pytest、pymysql、thrift、      requests、paramiko、 allure-pytest       
系统环境: Windows 10    
内存8G+  CPU4+    
环境变量设置: C:\Program Files\Git\bin ;C:Program Files\allure-2.13.0\bin     


***三.测试用例设计***   

***@pytest.mark.parametrize()参数化使用***  
````
@pytest.mark.parametrize("server, safeMode, port, email, password, open_relay",
                        argvalues=[("lisi", 1, 2, '4@q.com', '5', True), ("sdaf", 1, 2, '5@q.com', '5', True)])  
def test_SMTP_SetConfig(server, safeMode, port, email, password, open_relay):
````
***mysql数据库连接使用***   
mysqlconect.py #使用pymysql封装了数据库的新增、删除、修改、查询等方法      

***config.inin配置文件的使用***       
***thrift test Demo演示***   

***三.allure测试报告***   
通过下列命令可以生成allure测试报告        

os.system('pytest --alluredir="Report/data"')  # 生成测试数据    

os.system('allure generate Report/data -o  Report/result --clean')  # 生成测试报告     


