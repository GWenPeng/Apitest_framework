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
class Test_Domain_AddPolicy_ClientRestrictionCheck400(object):
    @allure.testcase("ID5322,用例名：新增策略配置--客户端登录限制，配置参数错误--返回400")
    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_AddPolicyClientRestriction400.json").dict_value_join())
    def test_Domain_AddPolicy_ClientRestrictionCheck400(self, url, jsondata, headers, checkpoint):
        '''
        用例描述：该用例用于测试新增策略接口中策略"名称的参数400检查"，详情可见禅道用例
        '''
        add_client = Http_client()
        add_client.post(url=url, jsondata=jsondata, header=headers)
        #print (client.text)
        #接口响应状态断言
        assert add_client.status_code == checkpoint['status_code']
        assert add_client.jsonResponse["code"] == checkpoint["code"]
        assert add_client.jsonResponse["message"] == checkpoint["message"]


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_AddPolicyClientRestriction400.py'])
