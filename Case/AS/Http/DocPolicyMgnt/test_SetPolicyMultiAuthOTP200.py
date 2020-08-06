import pytest
import allure
import sys
import json
sys.path.append("../../../../")
from ShareMgnt import ncTShareMgnt
from Common.thrift_client import Thrift_client
from Common.http_request import Http_client


@pytest.mark.ASP_344
@pytest.mark.high
@allure.severity('blocker')  # 优先级
@allure.feature("文档域策略管控")
class Test_SetPolicyMultiAuthOTP200(object):
    @allure.testcase("ID5484,用例名：设置策略内容--非子域双因子认证，配置参数成功--返回200")
    def test_SetPolicyMultiAuth200(self):
        setpolicy_client = Http_client()
        setpolicy_client.put(url="/api/policy-management/v1/general/multi_factor_auth/value",
                            data="[{\"name\":\"multi_factor_auth\",\"value\":{\"enable\":true,\"image_vcode\":false,\"otp\":true,\"password_error_count\":0,\"sms_vcode\":false}}]",
                            header="{\"Content-Type\":\"application/json\"}")
        assert setpolicy_client.status_code == 200

        tc = Thrift_client(ncTShareMgnt)
        response = tc.client.GetCustomConfigOfString("dualfactor_auth_server_status")
        response_dict = json.loads(response)
        assert response_dict['auth_by_OTP'] == True

if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_SetPolicyMultiAuthOTP200.py'])
