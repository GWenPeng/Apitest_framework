import pytest
import allure
import sys
sys.path.append("../../../../")
from Common.readjson import JsonRead
from Common.http_request import Http_client


@pytest.mark.ASP_344
@pytest.mark.medium
@allure.severity('normal')  # 优先级
@allure.feature("文档域策略管控")
class Test_Domain_AddPolicy_NameCheck400(object):
    @allure.testcase("ID5314,用例名：新增策略配置--非子域环境新增策略，策略配置项非法检查--返回400")
    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_AddPolicyConfigurationItem400.json").dict_value_join())
    def test_Domain_AddPolicy_NameCheck400(self, url, jsondata, headers, checkpoint):
        add_client = Http_client()
        add_client.post(url=url, jsondata=jsondata, header=headers)
        print (add_client.jsonResponse)
        # 接口响应状态断言
        assert add_client.status_code == checkpoint['status_code']
        assert add_client.jsonResponse["code"] == checkpoint["code"]
        assert add_client.jsonResponse["message"] == checkpoint["message"]


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_AddPolicyConfigurationItem400.py'])
