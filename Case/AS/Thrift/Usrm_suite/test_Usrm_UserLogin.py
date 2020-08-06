# coding: utf-8
from EThriftException.ttypes import ncTException
import pytest
from ShareMgnt import ncTShareMgnt
from ShareMgnt import ttypes
from Common.thrift_client import Thrift_client
import allure


# # @pytest.mark.parametrize("host","10.2.64.230")
# @pytest.mark.usefixtures('funtion_fixture')
# # usefixtures指定使用哪个fixture方法初始化;fixture方法参数autouse=True时,可以不指定
@allure.issue(url="https://jira.eisoo.com/browse/ASP-4331", name="BUG号 ：ASP-4331")
@pytest.mark.high
def test_Usrm_UserLogin():
    tc = Thrift_client(ncTShareMgnt)
    option = ttypes.ncTUserLoginOption(vcode="", uuid="", loginIp="192.168.184.61", vcodeType=None, isPlainPwd=None,
                                       OTP=None, isModify=None)
    with pytest.raises(ncTException) as error:
        tc.client.Usrm_UserLogin(userName="baby@test2.develop.cn", newPassword="", option=option)

    assert '用户名或密码不正确' in error.value.expMsg
    assert error.value.errID == 20108
    tc.close()


if __name__ == '__main__':
    pytest.main(["-q", " test_Usrm_UserLogin.py"])
