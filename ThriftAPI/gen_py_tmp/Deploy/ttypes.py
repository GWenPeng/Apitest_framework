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
import ECMSManager.ttypes

from thrift.transport import TTransport
all_structs = []


class HaSys(object):
    NORMAL = 0
    BASIC = 1
    APP = 2
    STORAGE = 3
    DB = 4

    _VALUES_TO_NAMES = {
        0: "NORMAL",
        1: "BASIC",
        2: "APP",
        3: "STORAGE",
        4: "DB",
    }

    _NAMES_TO_VALUES = {
        "NORMAL": 0,
        "BASIC": 1,
        "APP": 2,
        "STORAGE": 3,
        "DB": 4,
    }


class ncTLVSSys(object):
    APP = 1
    STORAGE = 2

    _VALUES_TO_NAMES = {
        1: "APP",
        2: "STORAGE",
    }

    _NAMES_TO_VALUES = {
        "APP": 1,
        "STORAGE": 2,
    }


class ncTDeployManagerError(object):
    NCT_NOT_APPLICATION_NODE = 50001
    NCT_SERVICE_PACKAGE_MISSING = 50002
    NCT_SERVICE_ALREADY_INSTALLED = 50003
    NCT_SERVICE_NOT_INSTALL = 50004
    NCT_SERVICE_VERSION_LOWER = 50005
    NCT_SERVICE_PACKAGE_DAMAGE = 50006
    NCT_NODE_IS_OFFLINE = 50007
    NCT_NODE_IS_MASTER = 50008
    NCT_NODE_TYPE_IS_INVALID = 50009

    _VALUES_TO_NAMES = {
        50001: "NCT_NOT_APPLICATION_NODE",
        50002: "NCT_SERVICE_PACKAGE_MISSING",
        50003: "NCT_SERVICE_ALREADY_INSTALLED",
        50004: "NCT_SERVICE_NOT_INSTALL",
        50005: "NCT_SERVICE_VERSION_LOWER",
        50006: "NCT_SERVICE_PACKAGE_DAMAGE",
        50007: "NCT_NODE_IS_OFFLINE",
        50008: "NCT_NODE_IS_MASTER",
        50009: "NCT_NODE_TYPE_IS_INVALID",
    }

    _NAMES_TO_VALUES = {
        "NCT_NOT_APPLICATION_NODE": 50001,
        "NCT_SERVICE_PACKAGE_MISSING": 50002,
        "NCT_SERVICE_ALREADY_INSTALLED": 50003,
        "NCT_SERVICE_NOT_INSTALL": 50004,
        "NCT_SERVICE_VERSION_LOWER": 50005,
        "NCT_SERVICE_PACKAGE_DAMAGE": 50006,
        "NCT_NODE_IS_OFFLINE": 50007,
        "NCT_NODE_IS_MASTER": 50008,
        "NCT_NODE_TYPE_IS_INVALID": 50009,
    }


class ncTVersionCheck(object):
    NCT_PACKAGE_VERSION_EQ_SERVICE_VERSION = 1
    NCT_PACKAGE_VERSION_HIGER_THAN_SERVICE_VERSION = 2

    _VALUES_TO_NAMES = {
        1: "NCT_PACKAGE_VERSION_EQ_SERVICE_VERSION",
        2: "NCT_PACKAGE_VERSION_HIGER_THAN_SERVICE_VERSION",
    }

    _NAMES_TO_VALUES = {
        "NCT_PACKAGE_VERSION_EQ_SERVICE_VERSION": 1,
        "NCT_PACKAGE_VERSION_HIGER_THAN_SERVICE_VERSION": 2,
    }


class ncTServiceInfos(object):
    """
    Attributes:
     - service_name
     - service_version
     - exception_nodes
     - installed_nodes

    """


    def __init__(self, service_name=None, service_version=None, exception_nodes=None, installed_nodes=None,):
        self.service_name = service_name
        self.service_version = service_version
        self.exception_nodes = exception_nodes
        self.installed_nodes = installed_nodes

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
                    self.service_name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.service_version = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.LIST:
                    self.exception_nodes = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in range(_size0):
                        _elem5 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        self.exception_nodes.append(_elem5)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.LIST:
                    self.installed_nodes = []
                    (_etype9, _size6) = iprot.readListBegin()
                    for _i10 in range(_size6):
                        _elem11 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        self.installed_nodes.append(_elem11)
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
        oprot.writeStructBegin('ncTServiceInfos')
        if self.service_name is not None:
            oprot.writeFieldBegin('service_name', TType.STRING, 1)
            oprot.writeString(self.service_name.encode('utf-8') if sys.version_info[0] == 2 else self.service_name)
            oprot.writeFieldEnd()
        if self.service_version is not None:
            oprot.writeFieldBegin('service_version', TType.STRING, 2)
            oprot.writeString(self.service_version.encode('utf-8') if sys.version_info[0] == 2 else self.service_version)
            oprot.writeFieldEnd()
        if self.exception_nodes is not None:
            oprot.writeFieldBegin('exception_nodes', TType.LIST, 3)
            oprot.writeListBegin(TType.STRING, len(self.exception_nodes))
            for iter12 in self.exception_nodes:
                oprot.writeString(iter12.encode('utf-8') if sys.version_info[0] == 2 else iter12)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.installed_nodes is not None:
            oprot.writeFieldBegin('installed_nodes', TType.LIST, 4)
            oprot.writeListBegin(TType.STRING, len(self.installed_nodes))
            for iter13 in self.installed_nodes:
                oprot.writeString(iter13.encode('utf-8') if sys.version_info[0] == 2 else iter13)
            oprot.writeListEnd()
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


class ncTPackageInfo(object):
    """
    Attributes:
     - service_name
     - package_name
     - package_version
     - upload_time
     - package_size
     - package_md5
     - object_id
     - oss_id

    """


    def __init__(self, service_name=None, package_name=None, package_version=None, upload_time=None, package_size=None, package_md5=None, object_id=None, oss_id=None,):
        self.service_name = service_name
        self.package_name = package_name
        self.package_version = package_version
        self.upload_time = upload_time
        self.package_size = package_size
        self.package_md5 = package_md5
        self.object_id = object_id
        self.oss_id = oss_id

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
                    self.service_name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.package_name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.package_version = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.I64:
                    self.upload_time = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.I64:
                    self.package_size = iprot.readI64()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.STRING:
                    self.package_md5 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 7:
                if ftype == TType.STRING:
                    self.object_id = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 8:
                if ftype == TType.STRING:
                    self.oss_id = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
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
        oprot.writeStructBegin('ncTPackageInfo')
        if self.service_name is not None:
            oprot.writeFieldBegin('service_name', TType.STRING, 1)
            oprot.writeString(self.service_name.encode('utf-8') if sys.version_info[0] == 2 else self.service_name)
            oprot.writeFieldEnd()
        if self.package_name is not None:
            oprot.writeFieldBegin('package_name', TType.STRING, 2)
            oprot.writeString(self.package_name.encode('utf-8') if sys.version_info[0] == 2 else self.package_name)
            oprot.writeFieldEnd()
        if self.package_version is not None:
            oprot.writeFieldBegin('package_version', TType.STRING, 3)
            oprot.writeString(self.package_version.encode('utf-8') if sys.version_info[0] == 2 else self.package_version)
            oprot.writeFieldEnd()
        if self.upload_time is not None:
            oprot.writeFieldBegin('upload_time', TType.I64, 4)
            oprot.writeI64(self.upload_time)
            oprot.writeFieldEnd()
        if self.package_size is not None:
            oprot.writeFieldBegin('package_size', TType.I64, 5)
            oprot.writeI64(self.package_size)
            oprot.writeFieldEnd()
        if self.package_md5 is not None:
            oprot.writeFieldBegin('package_md5', TType.STRING, 6)
            oprot.writeString(self.package_md5.encode('utf-8') if sys.version_info[0] == 2 else self.package_md5)
            oprot.writeFieldEnd()
        if self.object_id is not None:
            oprot.writeFieldBegin('object_id', TType.STRING, 7)
            oprot.writeString(self.object_id.encode('utf-8') if sys.version_info[0] == 2 else self.object_id)
            oprot.writeFieldEnd()
        if self.oss_id is not None:
            oprot.writeFieldBegin('oss_id', TType.STRING, 8)
            oprot.writeString(self.oss_id.encode('utf-8') if sys.version_info[0] == 2 else self.oss_id)
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


class ncTMongoDBInfo(object):
    """
    Attributes:
     - hosts
     - port

    """


    def __init__(self, hosts=[
    ], port=0,):
        if hosts is self.thrift_spec[1][4]:
            hosts = [
            ]
        self.hosts = hosts
        self.port = port

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
                    self.hosts = []
                    (_etype17, _size14) = iprot.readListBegin()
                    for _i18 in range(_size14):
                        _elem19 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        self.hosts.append(_elem19)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I32:
                    self.port = iprot.readI32()
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
        oprot.writeStructBegin('ncTMongoDBInfo')
        if self.hosts is not None:
            oprot.writeFieldBegin('hosts', TType.LIST, 1)
            oprot.writeListBegin(TType.STRING, len(self.hosts))
            for iter20 in self.hosts:
                oprot.writeString(iter20.encode('utf-8') if sys.version_info[0] == 2 else iter20)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.port is not None:
            oprot.writeFieldBegin('port', TType.I32, 2)
            oprot.writeI32(self.port)
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


class VipInfo(object):
    """
    Attributes:
     - ovip
     - ivip
     - mask
     - nic
     - sys

    """


    def __init__(self, ovip="", ivip="", mask="", nic="", sys=1,):
        self.ovip = ovip
        self.ivip = ivip
        self.mask = mask
        self.nic = nic
        self.sys = sys

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
                    self.ovip = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.ivip = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.mask = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.nic = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.I32:
                    self.sys = iprot.readI32()
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
        oprot.writeStructBegin('VipInfo')
        if self.ovip is not None:
            oprot.writeFieldBegin('ovip', TType.STRING, 1)
            oprot.writeString(self.ovip.encode('utf-8') if sys.version_info[0] == 2 else self.ovip)
            oprot.writeFieldEnd()
        if self.ivip is not None:
            oprot.writeFieldBegin('ivip', TType.STRING, 2)
            oprot.writeString(self.ivip.encode('utf-8') if sys.version_info[0] == 2 else self.ivip)
            oprot.writeFieldEnd()
        if self.mask is not None:
            oprot.writeFieldBegin('mask', TType.STRING, 3)
            oprot.writeString(self.mask.encode('utf-8') if sys.version_info[0] == 2 else self.mask)
            oprot.writeFieldEnd()
        if self.nic is not None:
            oprot.writeFieldBegin('nic', TType.STRING, 4)
            oprot.writeString(self.nic.encode('utf-8') if sys.version_info[0] == 2 else self.nic)
            oprot.writeFieldEnd()
        if self.sys is not None:
            oprot.writeFieldBegin('sys', TType.I32, 5)
            oprot.writeI32(self.sys)
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


class HaNodeInfo(object):
    """
    Attributes:
     - node_uuid
     - node_ip
     - is_master
     - ha_sys

    """


    def __init__(self, node_uuid="", node_ip="", is_master=False, ha_sys=0,):
        self.node_uuid = node_uuid
        self.node_ip = node_ip
        self.is_master = is_master
        self.ha_sys = ha_sys

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
                    self.node_uuid = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.node_ip = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.BOOL:
                    self.is_master = iprot.readBool()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.I32:
                    self.ha_sys = iprot.readI32()
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
        oprot.writeStructBegin('HaNodeInfo')
        if self.node_uuid is not None:
            oprot.writeFieldBegin('node_uuid', TType.STRING, 1)
            oprot.writeString(self.node_uuid.encode('utf-8') if sys.version_info[0] == 2 else self.node_uuid)
            oprot.writeFieldEnd()
        if self.node_ip is not None:
            oprot.writeFieldBegin('node_ip', TType.STRING, 2)
            oprot.writeString(self.node_ip.encode('utf-8') if sys.version_info[0] == 2 else self.node_ip)
            oprot.writeFieldEnd()
        if self.is_master is not None:
            oprot.writeFieldBegin('is_master', TType.BOOL, 3)
            oprot.writeBool(self.is_master)
            oprot.writeFieldEnd()
        if self.ha_sys is not None:
            oprot.writeFieldBegin('ha_sys', TType.I32, 4)
            oprot.writeI32(self.ha_sys)
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


class ReleaseInfo(object):
    """
    Attributes:
     - release_name

    """


    def __init__(self, release_name="",):
        self.release_name = release_name

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
                    self.release_name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
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
        oprot.writeStructBegin('ReleaseInfo')
        if self.release_name is not None:
            oprot.writeFieldBegin('release_name', TType.STRING, 1)
            oprot.writeString(self.release_name.encode('utf-8') if sys.version_info[0] == 2 else self.release_name)
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


class CSNodeInfo(object):
    """
    Attributes:
     - cs_node_name
     - node_uuid

    """


    def __init__(self, cs_node_name="", node_uuid="",):
        self.cs_node_name = cs_node_name
        self.node_uuid = node_uuid

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
                    self.cs_node_name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.node_uuid = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
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
        oprot.writeStructBegin('CSNodeInfo')
        if self.cs_node_name is not None:
            oprot.writeFieldBegin('cs_node_name', TType.STRING, 1)
            oprot.writeString(self.cs_node_name.encode('utf-8') if sys.version_info[0] == 2 else self.cs_node_name)
            oprot.writeFieldEnd()
        if self.node_uuid is not None:
            oprot.writeFieldBegin('node_uuid', TType.STRING, 2)
            oprot.writeString(self.node_uuid.encode('utf-8') if sys.version_info[0] == 2 else self.node_uuid)
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


class ContainerizedServiceInfo(object):
    """
    Attributes:
     - service_name
     - available_version
     - installed_version
     - nodes
     - available_package
     - replicas

    """


    def __init__(self, service_name="", available_version="", installed_version="", nodes=[
    ], available_package="", replicas=0,):
        self.service_name = service_name
        self.available_version = available_version
        self.installed_version = installed_version
        if nodes is self.thrift_spec[4][4]:
            nodes = [
            ]
        self.nodes = nodes
        self.available_package = available_package
        self.replicas = replicas

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
                    self.service_name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.STRING:
                    self.available_version = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.STRING:
                    self.installed_version = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.LIST:
                    self.nodes = []
                    (_etype24, _size21) = iprot.readListBegin()
                    for _i25 in range(_size21):
                        _elem26 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        self.nodes.append(_elem26)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.STRING:
                    self.available_package = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.I32:
                    self.replicas = iprot.readI32()
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
        oprot.writeStructBegin('ContainerizedServiceInfo')
        if self.service_name is not None:
            oprot.writeFieldBegin('service_name', TType.STRING, 1)
            oprot.writeString(self.service_name.encode('utf-8') if sys.version_info[0] == 2 else self.service_name)
            oprot.writeFieldEnd()
        if self.available_version is not None:
            oprot.writeFieldBegin('available_version', TType.STRING, 2)
            oprot.writeString(self.available_version.encode('utf-8') if sys.version_info[0] == 2 else self.available_version)
            oprot.writeFieldEnd()
        if self.installed_version is not None:
            oprot.writeFieldBegin('installed_version', TType.STRING, 3)
            oprot.writeString(self.installed_version.encode('utf-8') if sys.version_info[0] == 2 else self.installed_version)
            oprot.writeFieldEnd()
        if self.nodes is not None:
            oprot.writeFieldBegin('nodes', TType.LIST, 4)
            oprot.writeListBegin(TType.STRING, len(self.nodes))
            for iter27 in self.nodes:
                oprot.writeString(iter27.encode('utf-8') if sys.version_info[0] == 2 else iter27)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.available_package is not None:
            oprot.writeFieldBegin('available_package', TType.STRING, 5)
            oprot.writeString(self.available_package.encode('utf-8') if sys.version_info[0] == 2 else self.available_package)
            oprot.writeFieldEnd()
        if self.replicas is not None:
            oprot.writeFieldBegin('replicas', TType.I32, 6)
            oprot.writeI32(self.replicas)
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


class ServiceConf(object):
    """
    Attributes:
     - service_name
     - node_ips

    """


    def __init__(self, service_name="", node_ips=[
    ],):
        self.service_name = service_name
        if node_ips is self.thrift_spec[2][4]:
            node_ips = [
            ]
        self.node_ips = node_ips

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
                    self.service_name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.LIST:
                    self.node_ips = []
                    (_etype31, _size28) = iprot.readListBegin()
                    for _i32 in range(_size28):
                        _elem33 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                        self.node_ips.append(_elem33)
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
        oprot.writeStructBegin('ServiceConf')
        if self.service_name is not None:
            oprot.writeFieldBegin('service_name', TType.STRING, 1)
            oprot.writeString(self.service_name.encode('utf-8') if sys.version_info[0] == 2 else self.service_name)
            oprot.writeFieldEnd()
        if self.node_ips is not None:
            oprot.writeFieldBegin('node_ips', TType.LIST, 2)
            oprot.writeListBegin(TType.STRING, len(self.node_ips))
            for iter34 in self.node_ips:
                oprot.writeString(iter34.encode('utf-8') if sys.version_info[0] == 2 else iter34)
            oprot.writeListEnd()
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
all_structs.append(ncTServiceInfos)
ncTServiceInfos.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'service_name', 'UTF8', None, ),  # 1
    (2, TType.STRING, 'service_version', 'UTF8', None, ),  # 2
    (3, TType.LIST, 'exception_nodes', (TType.STRING, 'UTF8', False), None, ),  # 3
    (4, TType.LIST, 'installed_nodes', (TType.STRING, 'UTF8', False), None, ),  # 4
)
all_structs.append(ncTPackageInfo)
ncTPackageInfo.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'service_name', 'UTF8', None, ),  # 1
    (2, TType.STRING, 'package_name', 'UTF8', None, ),  # 2
    (3, TType.STRING, 'package_version', 'UTF8', None, ),  # 3
    (4, TType.I64, 'upload_time', None, None, ),  # 4
    (5, TType.I64, 'package_size', None, None, ),  # 5
    (6, TType.STRING, 'package_md5', 'UTF8', None, ),  # 6
    (7, TType.STRING, 'object_id', 'UTF8', None, ),  # 7
    (8, TType.STRING, 'oss_id', 'UTF8', None, ),  # 8
)
all_structs.append(ncTMongoDBInfo)
ncTMongoDBInfo.thrift_spec = (
    None,  # 0
    (1, TType.LIST, 'hosts', (TType.STRING, 'UTF8', False), [
    ], ),  # 1
    (2, TType.I32, 'port', None, 0, ),  # 2
)
all_structs.append(VipInfo)
VipInfo.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'ovip', 'UTF8', "", ),  # 1
    (2, TType.STRING, 'ivip', 'UTF8', "", ),  # 2
    (3, TType.STRING, 'mask', 'UTF8', "", ),  # 3
    (4, TType.STRING, 'nic', 'UTF8', "", ),  # 4
    (5, TType.I32, 'sys', None, 1, ),  # 5
)
all_structs.append(HaNodeInfo)
HaNodeInfo.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'node_uuid', 'UTF8', "", ),  # 1
    (2, TType.STRING, 'node_ip', 'UTF8', "", ),  # 2
    (3, TType.BOOL, 'is_master', None, False, ),  # 3
    (4, TType.I32, 'ha_sys', None, 0, ),  # 4
)
all_structs.append(ReleaseInfo)
ReleaseInfo.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'release_name', 'UTF8', "", ),  # 1
)
all_structs.append(CSNodeInfo)
CSNodeInfo.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'cs_node_name', 'UTF8', "", ),  # 1
    (2, TType.STRING, 'node_uuid', 'UTF8', "", ),  # 2
)
all_structs.append(ContainerizedServiceInfo)
ContainerizedServiceInfo.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'service_name', 'UTF8', "", ),  # 1
    (2, TType.STRING, 'available_version', 'UTF8', "", ),  # 2
    (3, TType.STRING, 'installed_version', 'UTF8', "", ),  # 3
    (4, TType.LIST, 'nodes', (TType.STRING, 'UTF8', False), [
    ], ),  # 4
    (5, TType.STRING, 'available_package', 'UTF8', "", ),  # 5
    (6, TType.I32, 'replicas', None, 0, ),  # 6
)
all_structs.append(ServiceConf)
ServiceConf.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'service_name', 'UTF8', "", ),  # 1
    (2, TType.LIST, 'node_ips', (TType.STRING, 'UTF8', False), [
    ], ),  # 2
)
fix_spec(all_structs)
del all_structs
