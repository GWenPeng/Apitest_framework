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
from .ttypes import *
NCT_SHAREMGNT_PORT = 9600
NCT_USER_ADMIN = "266c6a42-6131-4d62-8f39-853e7093701c"
NCT_USER_AUDIT = "94752844-BDD0-4B9E-8927-1CA8D427E699"
NCT_USER_SYSTEM = "234562BE-88FF-4440-9BFF-447F139871A2"
NCT_USER_SECURIT = "4bb41612-a040-11e6-887d-005056920bea"
NCT_SYSTEM_ROLE_SUPPER = "7dcfcc9c-ad02-11e8-aa06-000c29358ad6"
NCT_SYSTEM_ROLE_ADMIN = "d2bd2082-ad03-11e8-aa06-000c29358ad6"
NCT_SYSTEM_ROLE_SECURIT = "d8998f72-ad03-11e8-aa06-000c29358ad6"
NCT_SYSTEM_ROLE_AUDIT = "def246f2-ad03-11e8-aa06-000c29358ad6"
NCT_SYSTEM_ROLE_ORG_MANAGER = "e63e1c88-ad03-11e8-aa06-000c29358ad6"
NCT_SYSTEM_ROLE_ORG_AUDIT = "f06ac18e-ad03-11e8-aa06-000c29358ad6"
NCT_SYSTEM_ROLE_SHARED_APPROVE = "f58622b2-ad03-11e8-aa06-000c29358ad6"
NCT_SYSTEM_ROLE_DOC_APPROVE = "fb648fac-ad03-11e8-aa06-000c29358ad6"
NCT_SYSTEM_ROLE_CSF_APPROVE = "01a78ac2-ad04-11e8-aa06-000c29358ad6"
NCT_DEFAULT_ORGANIZATION = "151bcb65-48ce-4b62-973f-0bb6685f9cb8"
NCT_UNDISTRIBUTE_USER_GROUP = "-1"
NCT_ALL_USER_GROUP = "-2"
NCT_DIRECT_DEPARTMENT = "-3"
NCT_DIRECT_ORGANIZATION = "-4"
NCT_DOC_EXCHANGE_PROCESSID = "-1"
NCT_MIN_CSF_LEVEL = 5