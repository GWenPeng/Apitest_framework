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
class Test_DeletePolicyURI404(object):
    @allure.testcase("ID5401,用例名：删除策略配置--非子域删除失败--返回404")
    @pytest.fixture(scope='function')
    def teardown(self):
        # 新增策略
        global policyid1, policyid2
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

    def test_DeletePolicyURI404(self, teardown):
        '''
            用例描述：该用例用于测试删除策略接口
        '''
        # 调用删除接口，验证缺少策略id的url
        delete_client = Http_client()
        deleteurl = "/api/document-domain-management/v1/policy-tpl/"
        delete_client.delete(url=deleteurl, header='{"Content-Type":"application/json"}')
        assert delete_client.status_code == 405

        # 调用删除接口，验证删除不存在策略id
        delete_client1 = Http_client()
        delete_client1.delete(url="/api/document-domain-management/v1/policy-tpl/111", header='{"Content-Type":"application/json"}')
        assert delete_client1.status_code == 404
        assert delete_client1.jsonResponse["code"] == 404014000
        assert delete_client1.jsonResponse["message"] == "Resource not found."

        # 调用策略id到删除策略的path路径中,验证删除多个策略场景
        deleteurl2 = "/api/document-domain-management/v1/policy-tpl/%s,%s" % (policyid1, policyid2)
        delete_client2 = Http_client()
        delete_client2.delete(url=deleteurl2, header='{"Content-Type":"application/json"}')
        assert delete_client2.status_code == 404
        assert delete_client2.jsonResponse["code"] == 404014000
        assert delete_client2.jsonResponse["message"] == "Resource not found."


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_DeletePolicyURI404.py'])
