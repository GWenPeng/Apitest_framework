import pytest
import allure
import sys
sys.path.append("../../../../")
from Common.http_request import Http_client
from .CommonDocPolicyMgnt import CommonDocPolicyMgnt

@pytest.mark.ASP_344
@pytest.mark.high
@allure.severity('blocker')  # 优先级
@allure.feature("文档域策略管控")
class Test_DeletePolicy200(object):
    @allure.testcase("ID5402,用例名：删除策略配置--非子域删除成功--返回200")
    @pytest.fixture(scope='function')
    def teardown(self):
        # 新增策略
        global policyid
        policyid = CommonDocPolicyMgnt().AddPolicy('{"content":[{"name":"password_strength_meter",'
                                                   '"value":{"enable":False,"length":12}}],'
                                                   '"name":"policy1"}')
        yield
        pass
    def test_DeletePolicy200(self,teardown):
        '''
        用例描述：该用例用于测试删除策略接口
        '''
        # 调用策略id到删除策略的path路径中
        deleteurl = "/api/document-domain-management/v1/policy-tpl/%s" % (policyid)
        #调用删除接口，删除策略
        delete_client = Http_client()
        delete_client.delete(url=deleteurl, header='{"Content-Type":"application/json"}')
        assert delete_client.status_code == 200

if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_DeletePolicy200.py'])
