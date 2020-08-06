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
class Test_AddPolicy_SharingCheck400(object):
    @allure.testcase("ID5326,用例名：新增策略配置--内外链共享，配置参数错误--返回400")
    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_AddPolicySharing400.json").dict_value_join())
    def test_AddPolicySharingCheck400(self, url, jsondata, headers, checkpoint):
        client = Http_client()
        client.post(url=url, jsondata=jsondata, header=headers)
        assert client.status_code== checkpoint['status_code']
        assert client.jsonResponse["code"] == checkpoint["code"]
        assert client.jsonResponse["message"] == checkpoint["message"]

if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_AddPolicyShare400.py'])
