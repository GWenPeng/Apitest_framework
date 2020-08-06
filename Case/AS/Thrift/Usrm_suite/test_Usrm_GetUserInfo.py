# coding: utf-8
import EThriftException
import pytest
from ShareMgnt import ncTShareMgnt
from Common.thrift_client import Thrift_client
import os

UserUUid = "15bff2c4-14d7-11ea-b37b-00505682d269"


# # @pytest.mark.parametrize("host","10.2.64.230")
# @pytest.mark.usefixtures('funtion_fixture')
# # usefixtures指定使用哪个fixture方法初始化;fixture方法参数autouse=True时,可以不指定
@pytest.mark.high
def test_Usrm_GetUserInfo():
    tc = Thrift_client(ncTShareMgnt)
    response = tc.client.Usrm_GetUserInfo(UserUUid)
    assert response.user.loginName == 'ddd'
    #  assert断言，实际结果response和期望结果比较
    # assert response.user.email == 'ddd'
    print('body方法返回的信息为：', response)
    tc.close()


if __name__ == '__main__':
    pytest.main(["-q"," test_Usrm_GetUserInfo.py"])
