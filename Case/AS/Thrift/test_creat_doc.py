from Common.thrift_client import Thrift_client
from EFAST import ncTEFAST
from EFAST import ttypes


def test_create_doc():
    for i in range(601):
        info = ttypes.ncTAddCustomDocParam(name="文档库名称" + str(i), typeName="类型名称",
                                           createrId="266c6a42-6131-4d62-8f39-853e7093701c",
                                           ownerIds=["d8a26ac8-d6d9-11ea-bd6d-005056823c71"], spaceQuota=200,
                                           ossId="CBDFEDC4B8284FBBB7D867D7C367D37E",
                                           perm=ttypes.ncTDepartPerm(permValue=60, endTime=30000000))
        tc = Thrift_client(ncTEFAST, host="10.2.177.20", port=9121)
        rs = tc.client.EFAST_AddCustomDoc(info=info)
        print(rs)
