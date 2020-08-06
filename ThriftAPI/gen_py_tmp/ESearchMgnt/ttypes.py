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


class ncTESearchMgntError(object):
    NCT_DB_OPERATE_FAILED = 10001
    NCT_UNKNOWN_ERROR = 10002
    NCT_CANT_ENABLE_KEYSCAN_CAUSE_FULLTEXT_INDEX_NOT_INSTALLED = 20001
    NCT_INVALID_USER_DICT_FNAME = 200002
    NCT_INVALID_USER_DICT_FCONTENT = 200003
    NCT_RENAMED_LENGTH_EXCEEDS = 200004
    NCT_USER_DICT_NOT_EXISTS = 200005
    NCT_EXCEED_MAX_DICT_COUNT = 200006
    NCT_EXCEED_FCONTENT_LENTH = 200007
    NCT_CANT_ENABLE_KEYSCAN_CAUSE_NO_USER_DICT = 200008
    NCT_HAVE_NO_ACTIVED_LICENSE = 200009
    NCT_SUMMARY_CONF_NO_SUCH_FIELD = 200101
    NCT_SUMMARY_DOES_NOT_SUPPORT_THIS_LANGUAGE = 200102
    NCT_SIZE_LESS_THAN_ZERO = 200103

    _VALUES_TO_NAMES = {
        10001: "NCT_DB_OPERATE_FAILED",
        10002: "NCT_UNKNOWN_ERROR",
        20001: "NCT_CANT_ENABLE_KEYSCAN_CAUSE_FULLTEXT_INDEX_NOT_INSTALLED",
        200002: "NCT_INVALID_USER_DICT_FNAME",
        200003: "NCT_INVALID_USER_DICT_FCONTENT",
        200004: "NCT_RENAMED_LENGTH_EXCEEDS",
        200005: "NCT_USER_DICT_NOT_EXISTS",
        200006: "NCT_EXCEED_MAX_DICT_COUNT",
        200007: "NCT_EXCEED_FCONTENT_LENTH",
        200008: "NCT_CANT_ENABLE_KEYSCAN_CAUSE_NO_USER_DICT",
        200009: "NCT_HAVE_NO_ACTIVED_LICENSE",
        200101: "NCT_SUMMARY_CONF_NO_SUCH_FIELD",
        200102: "NCT_SUMMARY_DOES_NOT_SUPPORT_THIS_LANGUAGE",
        200103: "NCT_SIZE_LESS_THAN_ZERO",
    }

    _NAMES_TO_VALUES = {
        "NCT_DB_OPERATE_FAILED": 10001,
        "NCT_UNKNOWN_ERROR": 10002,
        "NCT_CANT_ENABLE_KEYSCAN_CAUSE_FULLTEXT_INDEX_NOT_INSTALLED": 20001,
        "NCT_INVALID_USER_DICT_FNAME": 200002,
        "NCT_INVALID_USER_DICT_FCONTENT": 200003,
        "NCT_RENAMED_LENGTH_EXCEEDS": 200004,
        "NCT_USER_DICT_NOT_EXISTS": 200005,
        "NCT_EXCEED_MAX_DICT_COUNT": 200006,
        "NCT_EXCEED_FCONTENT_LENTH": 200007,
        "NCT_CANT_ENABLE_KEYSCAN_CAUSE_NO_USER_DICT": 200008,
        "NCT_HAVE_NO_ACTIVED_LICENSE": 200009,
        "NCT_SUMMARY_CONF_NO_SUCH_FIELD": 200101,
        "NCT_SUMMARY_DOES_NOT_SUPPORT_THIS_LANGUAGE": 200102,
        "NCT_SIZE_LESS_THAN_ZERO": 200103,
    }


class ncTKeyScanTaskFlag(object):
    NCT_ILLEGALCONTENT = 1
    NCT_WORDSCAN = 2

    _VALUES_TO_NAMES = {
        1: "NCT_ILLEGALCONTENT",
        2: "NCT_WORDSCAN",
    }

    _NAMES_TO_VALUES = {
        "NCT_ILLEGALCONTENT": 1,
        "NCT_WORDSCAN": 2,
    }


class ncTUserDictInfo(object):
    """
    Attributes:
     - id
     - name
     - upTime

    """


    def __init__(self, id=None, name=None, upTime=None,):
        self.id = id
        self.name = name
        self.upTime = upTime

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
                    self.id = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I64:
                    self.upTime = iprot.readI64()
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
        oprot.writeStructBegin('ncTUserDictInfo')
        if self.id is not None:
            oprot.writeFieldBegin('id', TType.STRING, 1)
            oprot.writeString(self.id.encode('utf-8') if sys.version_info[0] == 2 else self.id)
            oprot.writeFieldEnd()
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 2)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        if self.upTime is not None:
            oprot.writeFieldBegin('upTime', TType.I64, 3)
            oprot.writeI64(self.upTime)
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
all_structs.append(ncTUserDictInfo)
ncTUserDictInfo.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'id', 'UTF8', None, ),  # 1
    (2, TType.STRING, 'name', 'UTF8', None, ),  # 2
    (3, TType.I64, 'upTime', None, None, ),  # 3
)
fix_spec(all_structs)
del all_structs
