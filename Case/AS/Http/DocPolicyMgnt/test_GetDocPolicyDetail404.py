import pytest
import allure
import sys
sys.path.append("../../../../")

from Common.http_request import Http_client
from .CommonDocPolicyMgnt import CommonDocPolicyMgnt

@pytest.mark.ASP_344
@pytest.mark.medium
@allure.severity('normal')  # 优先级
@allure.feature("文档域策略管控")
class Test_GetDocDomainPolicy_Detail404(object):
    @allure.testcase("ID5450,用例名：获取文档域策略的详细配置--非子域获取失败--返回404")
    @pytest.fixture(scope='function')
    def teardown(self):
        # 新增策略
        global policyid1,policyid2
        policyid1 = CommonDocPolicyMgnt().AddPolicy('{"content":[{"name":"password_strength_meter",'
                                                   '"value":{"enable":False,"length":12}}],'
                                                   '"name":"policy1"}')
        policyid2 = CommonDocPolicyMgnt().AddPolicy('{"content":[{"name":"password_strength_meter",'
                                                   '"value":{"enable":False,"length":12}}],'
                                                   '"name":"policy2"}')
        yield
        # 删除策略配置
        CommonDocPolicyMgnt().DeletePolicy(policyid1)
        CommonDocPolicyMgnt().DeletePolicy(policyid2)

    def test_GetDocumentDomainPolicy_Detail404(self,teardown):
        '''
        用例描述：该用例用于测试获取文档域策略详细配置接口404情况
        '''
        # 调用policy_id，组成查询接口url，验证传入不存在策略id
        detail_url1 = "/api/document-domain-management/v1/policy-tpl/111"
        # 调用获取文档域策略详细配置接口
        detail_client1 = Http_client()
        detail_client1.get(url=detail_url1, header='{"Content-Type":"application/json"}')
        assert detail_client1.status_code == 404
        assert detail_client1.jsonResponse["code"] == 404014000
        assert detail_client1.jsonResponse["message"] == "Resource not found."

        # 调用policy_id，组成查询接口url，验证传入多个有效策略id情况
        detail_url = "/api/document-domain-management/v1/policy-tpl/%s,%s"%(policyid1,policyid2)
        #调用获取文档域策略详细配置接口
        detail_client2 = Http_client()
        detail_client2.get(url=detail_url, header='{"Content-Type":"application/json"}')
        assert detail_client1.status_code == 404
        assert detail_client1.jsonResponse["code"] == 404014000
        assert detail_client1.jsonResponse["message"] == "Resource not found."

if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_GetDocumentDomainPolicy_Detail404.py'])
