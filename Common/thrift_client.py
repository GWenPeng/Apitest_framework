# sys.path.append('gen-py')

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from Common.readConfig import readconfigs
from ShareMgnt import ncTShareMgnt


class Thrift_client(object):
    def __init__(self, service=ncTShareMgnt, tagname="thriftSocket_ShareMgnt", host=None, port=None):
        readconf = readconfigs()
        if host is None:
            self.host = readconf.get_thriftSocket(tagname=tagname, name="host")
        else:
            self.host = host
        if port is None:
            self.port = readconf.get_thriftSocket(tagname=tagname, name="port")
        else:
            self.port = port

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
