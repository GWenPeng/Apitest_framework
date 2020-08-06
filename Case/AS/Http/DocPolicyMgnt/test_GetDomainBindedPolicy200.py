import pytest
import allure
import sys
sys.path.append("../../../../")
from Common.http_request import Http_client
from .CommonDocPolicyMgnt import CommonDocPolicyMgnt
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt


@pytest.mark.ASP_344
@pytest.mark.high
@allure.feature("文档域策略管控")
class Test_GetDomainBindedPolicy200(object):
    @allure.testcase("ID5469,用例名：获取文档域绑定的策略配置--子域获取成功--返回200")
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

    def test_GetDomainBindedPolicy200(self, teardown):
        policyid = teardown[0]
        relation_id1 = teardown[1]
        #调用子域1id，形成查询文档域绑定的策略配置url
        bindpolicy_url1 = "/api/document-domain-management/v1/domain/%s/bound-policy-tpl"%(relation_id1)
        bindpolicy_client1 = Http_client()
        bindpolicy_client1.get(url=bindpolicy_url1,header='{"Content-Type":"application/json"}')
        assert bindpolicy_client1.status_code == 200

        #将返回值和策略配置内容对比
        assert bindpolicy_client1.jsonResponse['id'] == policyid
        assert bindpolicy_client1.jsonResponse['name'] == "policy1"

if __name__ == '__main__':
    # main()
    pytest.main(['-q', '-v', 'test_GetDomainBindedPolicy200.py'])