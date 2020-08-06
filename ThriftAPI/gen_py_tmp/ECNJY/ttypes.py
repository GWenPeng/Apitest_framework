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
import EThriftException.ttypes

from thrift.transport import TTransport
all_structs = []


class ncTECNJYProgress(object):
    """
    同步进度返回值

    Attributes:
     - hasfininum
     - notfininum
     - totalsize

    """


    def __init__(self, hasfininum=None, notfininum=None, totalsize=None,):
        self.hasfininum = hasfininum
        self.notfininum = notfininum
        self.totalsize = totalsize

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
                if ftype == TType.I64:
                    self.hasfininum = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I64:
                    self.notfininum = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I64:
                    self.totalsize = iprot.readI64()
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
        oprot.writeStructBegin('ncTECNJYProgress')
        if self.hasfininum is not None:
            oprot.writeFieldBegin('hasfininum', TType.I64, 1)
            oprot.writeI64(self.hasfininum)
            oprot.writeFieldEnd()
        if self.notfininum is not None:
            oprot.writeFieldBegin('notfininum', TType.I64, 2)
            oprot.writeI64(self.notfininum)
            oprot.writeFieldEnd()
        if self.totalsize is not None:
            oprot.writeFieldBegin('totalsize', TType.I64, 3)
            oprot.writeI64(self.totalsize)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.hasfininum is None:
            raise TProtocolException(message='Required field hasfininum is unset!')
        if self.notfininum is None:
            raise TProtocolException(message='Required field notfininum is unset!')
        if self.totalsize is None:
            raise TProtocolException(message='Required field totalsize is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class ncTECNJYPwd(object):
    """
    获取同步账户和密码

    Attributes:
     - partnerid
     - key

    """


    def __init__(self, partnerid=None, key=None,):
        self.partnerid = partnerid
        self.key = key

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
                    self.partnerid = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.key = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
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
        oprot.writeStructBegin('ncTECNJYPwd')
        if self.partnerid is not None:
            oprot.writeFieldBegin('partnerid', TType.STRING, 1)
            oprot.writeString(self.partnerid.encode('utf-8') if sys.version_info[0] == 2 else self.partnerid)
            oprot.writeFieldEnd()
        if self.key is not None:
            oprot.writeFieldBegin('key', TType.STRING, 2)
            oprot.writeString(self.key.encode('utf-8') if sys.version_info[0] == 2 else self.key)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.partnerid is None:
            raise TProtocolException(message='Required field partnerid is unset!')
        if self.key is None:
            raise TProtocolException(message='Required field key is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class ncTECNJYMechanism(object):
    """
    获取同步机制

    Attributes:
     - day
     - hour
     - min
     - sec

    """


    def __init__(self, day=None, hour=None, min=None, sec=None,):
        self.day = day
        self.hour = hour
        self.min = min
        self.sec = sec

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
                if ftype == TType.I32:
                    self.day = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I32:
                    self.hour = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.min = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.I32:
                    self.sec = iprot.readI32()
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
        oprot.writeStructBegin('ncTECNJYMechanism')
        if self.day is not None:
            oprot.writeFieldBegin('day', TType.I32, 1)
            oprot.writeI32(self.day)
            oprot.writeFieldEnd()
        if self.hour is not None:
            oprot.writeFieldBegin('hour', TType.I32, 2)
            oprot.writeI32(self.hour)
            oprot.writeFieldEnd()
        if self.min is not None:
            oprot.writeFieldBegin('min', TType.I32, 3)
            oprot.writeI32(self.min)
            oprot.writeFieldEnd()
        if self.sec is not None:
            oprot.writeFieldBegin('sec', TType.I32, 4)
            oprot.writeI32(self.sec)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.day is None:
            raise TProtocolException(message='Required field day is unset!')
        if self.hour is None:
            raise TProtocolException(message='Required field hour is unset!')
        if self.min is None:
            raise TProtocolException(message='Required field min is unset!')
        if self.sec is None:
            raise TProtocolException(message='Required field sec is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class ncTECNJYLog(object):
    """
    错误日志
    type：0为同步成功日志，1为同步失败日志

    Attributes:
     - id
     - btime
     - etime
     - description
     - type

    """


    def __init__(self, id=None, btime=None, etime=None, description=None, type=None,):
        self.id = id
        self.btime = btime
        self.etime = etime
        self.description = description
        self.type = type

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
                if ftype == TType.I64:
                    self.id = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I64:
                    self.btime = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I64:
                    self.etime = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.description = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.I32:
                    self.type = iprot.readI32()
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
        oprot.writeStructBegin('ncTECNJYLog')
        if self.id is not None:
            oprot.writeFieldBegin('id', TType.I64, 1)
            oprot.writeI64(self.id)
            oprot.writeFieldEnd()
        if self.btime is not None:
            oprot.writeFieldBegin('btime', TType.I64, 2)
            oprot.writeI64(self.btime)
            oprot.writeFieldEnd()
        if self.etime is not None:
            oprot.writeFieldBegin('etime', TType.I64, 3)
            oprot.writeI64(self.etime)
            oprot.writeFieldEnd()
        if self.description is not None:
            oprot.writeFieldBegin('description', TType.STRING, 4)
            oprot.writeString(self.description.encode('utf-8') if sys.version_info[0] == 2 else self.description)
            oprot.writeFieldEnd()
        if self.type is not None:
            oprot.writeFieldBegin('type', TType.I32, 5)
            oprot.writeI32(self.type)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.id is None:
            raise TProtocolException(message='Required field id is unset!')
        if self.btime is None:
            raise TProtocolException(message='Required field btime is unset!')
        if self.etime is None:
            raise TProtocolException(message='Required field etime is unset!')
        if self.description is None:
            raise TProtocolException(message='Required field description is unset!')
        if self.type is None:
            raise TProtocolException(message='Required field type is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class ncTECNJYLogSet(object):
    """
    GNS 对象集

    Attributes:
     - cnjyLogs

    """


    def __init__(self, cnjyLogs=None,):
        self.cnjyLogs = cnjyLogs

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
                if ftype == TType.LIST:
                    self.cnjyLogs = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in range(_size0):
                        _elem5 = ncTECNJYLog()
                        _elem5.read(iprot)
                        self.cnjyLogs.append(_elem5)
                    iprot.readListEnd()
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
        oprot.writeStructBegin('ncTECNJYLogSet')
        if self.cnjyLogs is not None:
            oprot.writeFieldBegin('cnjyLogs', TType.LIST, 1)
            oprot.writeListBegin(TType.STRUCT, len(self.cnjyLogs))
            for iter6 in self.cnjyLogs:
                iter6.write(oprot)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        if self.cnjyLogs is None:
            raise TProtocolException(message='Required field cnjyLogs is unset!')
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(ncTECNJYProgress)
ncTECNJYProgress.thrift_spec = (
    None,  # 0
    (1, TType.I64, 'hasfininum', None, None, ),  # 1
    (2, TType.I64, 'notfininum', None, None, ),  # 2
    (3, TType.I64, 'totalsize', None, None, ),  # 3
)
all_structs.append(ncTECNJYPwd)
ncTECNJYPwd.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'partnerid', 'UTF8', None, ),  # 1
    (2, TType.STRING, 'key', 'UTF8', None, ),  # 2
)
all_structs.append(ncTECNJYMechanism)
ncTECNJYMechanism.thrift_spec = (
    None,  # 0
    (1, TType.I32, 'day', None, None, ),  # 1
    (2, TType.I32, 'hour', None, None, ),  # 2
    (3, TType.I32, 'min', None, None, ),  # 3
    (4, TType.I32, 'sec', None, None, ),  # 4
)
all_structs.append(ncTECNJYLog)
ncTECNJYLog.thrift_spec = (
    None,  # 0
    (1, TType.I64, 'id', None, None, ),  # 1
    (2, TType.I64, 'btime', None, None, ),  # 2
    (3, TType.I64, 'etime', None, None, ),  # 3
    (4, TType.STRING, 'description', 'UTF8', None, ),  # 4
    (5, TType.I32, 'type', None, None, ),  # 5
)
all_structs.append(ncTECNJYLogSet)
ncTECNJYLogSet.thrift_spec = (
    None,  # 0
    (1, TType.LIST, 'cnjyLogs', (TType.STRUCT, [ncTECNJYLog, None], False), None, ),  # 1
)
fix_spec(all_structs)
del all_structs