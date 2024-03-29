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
    def Keyscan_StopFullScan(self):
        """
        终止掉当前的扫描任务

        @return:

        """
        pass

    def SetIndexInterval(self, interval):
        """
        修改全文检索探测间隔

        @interval: 时间间隔，单位 秒

        Parameters:
         - interval

        """
        pass


class Client(Iface):
    def __init__(self, iprot, oprot=None):
        self._iprot = self._oprot = iprot
        if oprot is not None:
            self._oprot = oprot
        self._seqid = 0

    def Keyscan_StopFullScan(self):
        """
        终止掉当前的扫描任务

        @return:

        """
        self.send_Keyscan_StopFullScan()
        self.recv_Keyscan_StopFullScan()

    def send_Keyscan_StopFullScan(self):
        self._oprot.writeMessageBegin('Keyscan_StopFullScan', TMessageType.CALL, self._seqid)
        args = Keyscan_StopFullScan_args()
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_Keyscan_StopFullScan(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = Keyscan_StopFullScan_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.exp is not None:
            raise result.exp
        return

    def SetIndexInterval(self, interval):
        """
        修改全文检索探测间隔

        @interval: 时间间隔，单位 秒

        Parameters:
         - interval

        """
        self.send_SetIndexInterval(interval)
        self.recv_SetIndexInterval()

    def send_SetIndexInterval(self, interval):
        self._oprot.writeMessageBegin('SetIndexInterval', TMessageType.CALL, self._seqid)
        args = SetIndexInterval_args()
        args.interval = interval
        args.write(self._oprot)
        self._oprot.writeMessageEnd()
        self._oprot.trans.flush()

    def recv_SetIndexInterval(self):
        iprot = self._iprot
        (fname, mtype, rseqid) = iprot.readMessageBegin()
        if mtype == TMessageType.EXCEPTION:
            x = TApplicationException()
            x.read(iprot)
            iprot.readMessageEnd()
            raise x
        result = SetIndexInterval_result()
        result.read(iprot)
        iprot.readMessageEnd()
        if result.exp is not None:
            raise result.exp
        return


class Processor(Iface, TProcessor):
    def __init__(self, handler):
        self._handler = handler
        self._processMap = {}
        self._processMap["Keyscan_StopFullScan"] = Processor.process_Keyscan_StopFullScan
        self._processMap["SetIndexInterval"] = Processor.process_SetIndexInterval
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

    def process_Keyscan_StopFullScan(self, seqid, iprot, oprot):
        args = Keyscan_StopFullScan_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = Keyscan_StopFullScan_result()
        try:
            self._handler.Keyscan_StopFullScan()
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
        oprot.writeMessageBegin("Keyscan_StopFullScan", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

    def process_SetIndexInterval(self, seqid, iprot, oprot):
        args = SetIndexInterval_args()
        args.read(iprot)
        iprot.readMessageEnd()
        result = SetIndexInterval_result()
        try:
            self._handler.SetIndexInterval(args.interval)
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
        oprot.writeMessageBegin("SetIndexInterval", msg_type, seqid)
        result.write(oprot)
        oprot.writeMessageEnd()
        oprot.trans.flush()

# HELPER FUNCTIONS AND STRUCTURES


class Keyscan_StopFullScan_args(object):


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
        oprot.writeStructBegin('Keyscan_StopFullScan_args')
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
all_structs.append(Keyscan_StopFullScan_args)
Keyscan_StopFullScan_args.thrift_spec = (
)


class Keyscan_StopFullScan_result(object):
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
        oprot.writeStructBegin('Keyscan_StopFullScan_result')
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
all_structs.append(Keyscan_StopFullScan_result)
Keyscan_StopFullScan_result.thrift_spec = (
    None,  # 0
    (1, TType.STRUCT, 'exp', [EThriftException.ttypes.ncTException, None], None, ),  # 1
)


class SetIndexInterval_args(object):
    """
    Attributes:
     - interval

    """


    def __init__(self, interval=None,):
        self.interval = interval

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
                    self.interval = iprot.readI32()
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
        oprot.writeStructBegin('SetIndexInterval_args')
        if self.interval is not None:
            oprot.writeFieldBegin('interval', TType.I32, 1)
            oprot.writeI32(self.interval)
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
all_structs.append(SetIndexInterval_args)
SetIndexInterval_args.thrift_spec = (
    None,  # 0
    (1, TType.I32, 'interval', None, None, ),  # 1
)


class SetIndexInterval_result(object):
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
        oprot.writeStructBegin('SetIndexInterval_result')
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
all_structs.append(SetIndexInterval_result)
SetIndexInterval_result.thrift_spec = (
    None,  # 0
    (1, TType.STRUCT, 'exp', [EThriftException.ttypes.ncTException, None], None, ),  # 1
)
fix_spec(all_structs)
del all_structs

