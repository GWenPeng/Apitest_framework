import pytest
import allure
import sys

sys.path.append("../../../../")
from Common.http_request import Http_client
from .CommonDocPolicyMgnt import CommonDocPolicyMgnt
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt

@pytest.mark.ASP_344
@pytest.mark.medium
@allure.severity('normal')  # 优先级
@allure.feature("文档域策略管控")
class Test_DeletePolicy409(object):
    @allure.testcase("ID5401,用例名：删除策略配置--非子域删除策略失败--返回409")
    @pytest.fixture(scope='function')
    def teardown(self, metadata_host):
        father_host = metadata_host["replace.eisoo.com"]
        child_host = metadata_host["child.eisoo.com"]
        father_host = (father_host.split(":")[1]).strip("/")
        child_host = (child_host.split(":")[1]).strip("/")
        # 新增策略
        policyid = CommonDocPolicyMgnt().AddPolicy('{"content":[{"name":"password_strength_meter",'
                                                   '"value":{"enable":False,"length":12}}],'
                                                   '"name":"policy1"}')
        # 获取子域凭据
        result = CommonAuthCredentialMgnt().get_credential(host=child_host, credential_type="child", note="string")
        credential_id = result[0]
        credential_key = result[1]
        # 添加子域
        relation_id1 = CommonDocPolicyMgnt().AddChildDomain1(father_host=father_host, child_host=child_host,
                                                             credential_id=credential_id, credential_key=credential_key)
        # 绑定策略和子域
        CommonDocPolicyMgnt().BindChildDomain(policyid, domain1=relation_id1)
        yield policyid, relation_id1
        # 解绑子域
        CommonDocPolicyMgnt().DeleteChildDomain(host=father_host, id=policyid, domain1=relation_id1)
        # 关系域删除
        deletedomain_url1 = "/api/document-domain-management/v1/domain/%s" % (relation_id1)
        delete_child1 = Http_client()
        delete_child1.delete(url=deletedomain_url1, header='{"Content-Type":"application/json"}')
        # 删除子域凭据
        CommonAuthCredentialMgnt().del_credential(host=child_host, credential_id=credential_id)
        # 删除策略配置
        CommonDocPolicyMgnt().DeletePolicy(policyid)

    def test_DeletePolicy409(self, teardown):
        policyid = teardown[0]
        relation_id1 = teardown[1]
        # 调用策略id到删除策略的path路径中
        deleteurl = "/api/document-domain-management/v1/policy-tpl/%s" % (policyid)
        # 调用删除接口，删除策略
        delete_client = Http_client()
        delete_client.delete(url=deleteurl, header='{"Content-Type":"application/json"}')
        assert delete_client.status_code == 409
        assert delete_client.jsonResponse["code"] == 409014221
        assert delete_client.jsonResponse["message"] == "The resource has been bound."

if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_DeletePolicy409.py'])

