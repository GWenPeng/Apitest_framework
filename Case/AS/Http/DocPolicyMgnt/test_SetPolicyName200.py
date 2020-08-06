import pytest
import allure
import sys
sys.path.append("../../../../")
from Common.readjson import JsonRead
from Common.http_request import Http_client


@pytest.mark.ASP_344
@pytest.mark.high
@allure.severity('blocker')  # 优先级
@allure.feature("文档域策略管控")
class Test_SetPolicyName200(object):
    @allure.testcase("ID5479,用例名：设置策略内容--非子域name参数正向检查--返回200")
    @pytest.mark.parametrize("url, jsondata, headers, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_SetPolicyName200.json").dict_value_join())
    def test_SetPolicyName200(self, url, jsondata, headers, checkpoint):
        '''
        用例描述：该用例用于验证设置策略内容name404检查
        '''
        setpolicy_client = Http_client()
        setpolicy_client.put(url=url, data=jsondata, header=headers)
        assert setpolicy_client.status_code == checkpoint['status_code']

if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_SetPolicyName200.py'])
