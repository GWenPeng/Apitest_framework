#
# Autogenerated by Thrift Compiler (0.13.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys
import logging
from .ttypes import *
from thrift.Thrift import TProcessor
from thrift.transport import TTransport
all_structs = []


class Iface(object):
    """
    ECMSUpgradeAgent thrift 管理接口

    """
    def query_package(self, path):
        """
        查询升级包信息
        @param   string  path    升级包路径

        Parameters:
         - path

        """
        pass

    def import_package(self, path):
        """
        导入升级包
        @param   string  path    升级包路径

        Parameters:
         - path

        """
        pass

    def remove_package(self):
        """
        删除已导入的升级包, 未导入升级包不抛错

        """
        pass

    def start_upgrade(self, name):
        """
        当前节点启动升级
        @param   string  name        升级包名称

        Parameters:
         - name

        """
        pass


class Client(Iface):
    """
    ECMSUpgradeAgent thrift 管理接口

    """
    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    def query_package(self, path):
        """
        查询升级包信息
        @param   string  path    升级包路径

        Parameters:
         - path

        """
        self.send_query_package(path)
        return self.recv_query_package()

    def send_query_package(self, path):
        self._oprot.writeMessageBegin('query_package', TMessageType.CALL, self._seqid)
        args = query_package_args()
        args.path = path
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_query_package(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = query_package_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.exp is not None:
            raise result.exp
        raise TApplicationException(TApplicationException.MISSING_RESULT, "query_package failed: unknown result")

    def import_package(self, path):
        """
        导入升级包
        @param   string  path    升级包路径

        Parameters:
         - path

        """
        self.send_import_package(path)
        return self.recv_import_package()

    def send_import_package(self, path):
        self._oprot.writeMessageBegin('import_package', TMessageType.CALL, self._seqid)
        args = import_package_args()
        args.path = path
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_import_package(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = import_package_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.success is not None:
            return result.success
        if result.exp is not None:
            raise result.exp
        raise TApplicationException(TApplicationException.MISSING_RESULT, "import_package failed: unknown result")

    def remove_package(self):
        """
        删除已导入的升级包, 未导入升级包不抛错

        """
        self.send_remove_package()
        self.recv_remove_package()

    def send_remove_package(self):
        self._oprot.writeMessageBegin('remove_package', TMessageType.CALL, self._seqid)
        args = remove_package_args()
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_remove_package(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = remove_package_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.exp is not None:
            raise result.exp
        return

    def start_upgrade(self, name):
        """
        当前节点启动升级
        @param   string  name        升级包名称

        Parameters:
         - name

        """
        self.send_start_upgrade(name)

    def send_start_upgrade(self, name):
        self._oprot.writeMessageBegin('start_upgrade', TMessageType.ONEWAY, self._seqid)
        args = start_upgrade_args()
        args.name = name
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()


class Processor(Iface, TProcessor):
    def __init__(self, handler):
        self._handler = handler
        self._processMap = {}
        self._processMap["query_package"] = Processor.process_query_package
        self._processMap["import_package"] = Processor.process_import_package
        self._processMap["remove_package"] = Processor.process_remove_package
        self._processMap["start_upgrade"] = Processor.process_start_upgrade
        self._on_message_begin = None

    def on_message_begin(self, func):
        self._on_message_begin = func

    def process(self, iprot, oprot):
        (name, type, seqid) = iprot.readMessageBegin()
        if self._on_message_begin:
            self._on_message_begin(name, type, seqid)
        if name not in self._processMap:
            iprot.skip(TType.STRUCT)
            iprot.readMessageEnd()
            x = TApplicationException(TApplicationException.UNKNOWN_METHOD, 'Unknown function %s' % (name))
            oprot.writeMessageBegin(name, TMessageType.EXCEPTION, seqid)
            x.write(oprot)
            oprot.writeMessageEnd()
            oprot.trans.flush()
            return
        else:
            self._processMap[name](self, seqid, iprot, oprot)
        return True

    def process_query_package(self, seqid, iprot, oprot):
        args = query_package_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = query_package_result()
        try:
            result.success = self._handler.query_package(args.path)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except EThriftException.ttypes.ncTException as exp:
            msg_type = TMessageType.REPLY
            result.exp = exp
        except TApplicationException as ex:
            logging.exception('TApplication exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = ex
        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
        oprot.writeMessageBegin("query_package", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_import_package(self, seqid, iprot, oprot):
        args = import_package_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = import_package_result()
        try:
            result.success = self._handler.import_package(args.path)
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except EThriftException.ttypes.ncTException as exp:
            msg_type = TMessageType.REPLY
            result.exp = exp
        except TApplicationException as ex:
            logging.exception('TApplication exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = ex
        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
        oprot.writeMessageBegin("import_package", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_remove_package(self, seqid, iprot, oprot):
        args = remove_package_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = remove_package_result()
        try:
            self._handler.remove_package()
            msg_type = TMessageType.REPLY
        except TTransport.TTransportException:
            raise
        except EThriftException.ttypes.ncTException as exp:
            msg_type = TMessageType.REPLY
            result.exp = exp
        except TApplicationException as ex:
            logging.exception('TApplication exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = ex
        except Exception:
            logging.exception('Unexpected exception in handler')
            msg_type = TMessageType.EXCEPTION
            result = TApplicationException(TApplicationException.INTERNAL_ERROR, 'Internal error')
        oprot.writeMessageBegin("remove_package", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_start_upgrade(self, seqid, iprot, oprot):
        args = start_upgrade_args()
        args.read(iprot)
        iprot.readMessageEnd()
        try:
            self._handler.start_upgrade(args.name)
        except TTransport.TTransportException:
            raise
        except Exception:
            logging.exception('Exception in oneway handler')

# HELPER FUNCTIONS AND STRUCTURES


class query_package_args(object):
    """
    Attributes:
     - path

    """


    def __init__(self, path=None,):
        self.path = path

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.path = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('query_package_args')
        if self.path is not None:
            oprot.writeFieldBegin('path', TType.STRING, 1)
            oprot.writeString(self.path.encode('utf-8') if sys.version_info[0] == 2 else self.path)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(query_package_args)
query_package_args.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'path', 'UTF8', None, ),  # 1
)


class query_package_result(object):
    """
    Attributes:
     - success
     - exp

    """


    def __init__(self, success=None, exp=None,):
        self.success = success
        self.exp = exp

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRUCT:
                    self.success = ncTUpgradePackageInfo()
                    self.success.read(iprot)
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.exp = EThriftException.ttypes.ncTException()
                    self.exp.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('query_package_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRUCT, 0)
            self.success.write(oprot)
            oprot.writeFieldEnd()
        if self.exp is not None:
            oprot.writeFieldBegin('exp', TType.STRUCT, 1)
            self.exp.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(query_package_result)
query_package_result.thrift_spec = (
    (0, TType.STRUCT, 'success', [ncTUpgradePackageInfo, None], None, ),  # 0
    (1, TType.STRUCT, 'exp', [EThriftException.ttypes.ncTException, None], None, ),  # 1
)


class import_package_args(object):
    """
    Attributes:
     - path

    """


    def __init__(self, path=None,):
        self.path = path

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.path = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('import_package_args')
        if self.path is not None:
            oprot.writeFieldBegin('path', TType.STRING, 1)
            oprot.writeString(self.path.encode('utf-8') if sys.version_info[0] == 2 else self.path)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(import_package_args)
import_package_args.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'path', 'UTF8', None, ),  # 1
)


class import_package_result(object):
    """
    Attributes:
     - success
     - exp

    """


    def __init__(self, success=None, exp=None,):
        self.success = success
        self.exp = exp

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 0:
                if ftype == TType.STRING:
                    self.success = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 1:
                if ftype == TType.STRUCT:
                    self.exp = EThriftException.ttypes.ncTException()
                    self.exp.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('import_package_result')
        if self.success is not None:
            oprot.writeFieldBegin('success', TType.STRING, 0)
            oprot.writeString(self.success.encode('utf-8') if sys.version_info[0] == 2 else self.success)
            oprot.writeFieldEnd()
        if self.exp is not None:
            oprot.writeFieldBegin('exp', TType.STRUCT, 1)
            self.exp.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(import_package_result)
import_package_result.thrift_spec = (
    (0, TType.STRING, 'success', 'UTF8', None, ),  # 0
    (1, TType.STRUCT, 'exp', [EThriftException.ttypes.ncTException, None], None, ),  # 1
)


class remove_package_args(object):


    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('remove_package_args')
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(remove_package_args)
remove_package_args.thrift_spec = (
)


class remove_package_result(object):
    """
    Attributes:
     - exp

    """


    def __init__(self, exp=None,):
        self.exp = exp

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRUCT:
                    self.exp = EThriftException.ttypes.ncTException()
                    self.exp.read(iprot)
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('remove_package_result')
        if self.exp is not None:
            oprot.writeFieldBegin('exp', TType.STRUCT, 1)
            self.exp.write(oprot)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(remove_package_result)
remove_package_result.thrift_spec = (
    None,  # 0
    (1, TType.STRUCT, 'exp', [EThriftException.ttypes.ncTException, None], None, ),  # 1
)


class start_upgrade_args(object):
    """
    Attributes:
     - name

    """


    def __init__(self, name=None,):
        self.name = name

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('start_upgrade_args')
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 1)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(start_upgrade_args)
start_upgrade_args.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'name', 'UTF8', None, ),  # 1
)
fix_spec(all_structs)
del all_structs

