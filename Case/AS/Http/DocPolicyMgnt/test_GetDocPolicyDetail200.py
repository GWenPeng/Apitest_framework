import pytest
import allure
import sys
sys.path.append("../../../../")

from Common.readjson import JsonRead
from Common.http_request import Http_client
from .CommonDocPolicyMgnt import CommonDocPolicyMgnt

@pytest.mark.ASP_344
@pytest.mark.high
@allure.severity('blocker')  # 优先级
@allure.feature("文档域策略管控")
class Test_GetDocDomainPolicy_Detail200(object):
    @allure.testcase("ID5465,用例名：获取文档域策略的详细配置--非子域获取成功--返回200 ")
    @pytest.mark.parametrize("url, headers, jsondata", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_GetDocPolicyDetail200.json").dict_value_join())
    @pytest.fixture(scope='function')
    def teardown(self, jsondata):
        # 新增策略
        global policyid
        policyid = CommonDocPolicyMgnt().AddPolicy(jsondata)
        yield
        # 删除策略配置
        CommonDocPolicyMgnt().DeletePolicy(policyid)

    @pytest.mark.parametrize("url, headers, jsondata", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_GetDocPolicyDetail200.json").dict_value_join())
    def test_GetDocumentDomainPolicy_Detail200(self, url, headers, jsondata, teardown):
        '''
        用例描述：该用例用于测试获取文档域策略详细配置接口
        '''
        # 调用policy_id，组成查询接口url
        detail_url = "/api/document-domain-management/v1/policy-tpl/%s"%(policyid)
        #调用获取文档域策略详细配置接口
        detail_client = Http_client()
        detail_client.get(url=detail_url, header='{"Content-Type":"application/json"}')
        #将配置文件中json字符串转为字典
        addpolicy_json = eval(jsondata)
        #查询信息和配置文件中信息对比
        assert detail_client.jsonResponse["content"] == addpolicy_json["content"]
        assert detail_client.jsonResponse["name"] == addpolicy_json["name"]

if __name__ == '__main__':

    pytest.main(['-q', '-v', 'test_GetDocPolicyDetail200.py'])
