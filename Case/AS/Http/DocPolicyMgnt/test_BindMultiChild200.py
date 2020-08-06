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
class Test_BindMultiChild200(object):
    @allure.testcase("ID5340,用例名：绑定子域--非子域绑定成功--返回200 ")
    @pytest.fixture(scope="function")
    def teardown(self, metadata_host):
        father_host = metadata_host["replace.eisoo.com"]
        child_host1 = metadata_host["child.eisoo.com"]
        child_host2 = metadata_host["self.eisoo.com"]
        father_host = (father_host.split(":")[1]).strip("/")
        child_host1 = (child_host1.split(":")[1]).strip("/")
        child_host2 = (child_host2.split(":")[1]).strip("/")
        # 新增策略
        policyid = CommonDocPolicyMgnt().AddPolicy('{"content":[{"name":"password_strength_meter",'
                                                   '"value":{"enable":False,"length":12}}],'
                                                   '"name":"policy1"}')
        # 获取子域凭据
        result1 = CommonAuthCredentialMgnt().get_credential(host=child_host1, credential_type="child", note="string")
        credential_id1 = result1[0]
        credential_key1 = result1[1]
        result2 = CommonAuthCredentialMgnt().get_credential(host=child_host2, credential_type="child", note="string")
        credential_id2 = result2[0]
        credential_key2 = result2[1]
        # 添加子域
        relation_id1 = CommonDocPolicyMgnt().AddChildDomain1(father_host=father_host, child_host=child_host1,
                                                             credential_id=credential_id1,
                                                             credential_key=credential_key1)
        relation_id2 = CommonDocPolicyMgnt().AddChildDomain2(father_host=father_host, child_host=child_host2,
                                                             credential_id=credential_id2,
                                                             credential_key=credential_key2)
        yield policyid, relation_id1, relation_id2
        # 解绑子域
        CommonDocPolicyMgnt().DeleteChildDomain(host=father_host, id=policyid, domain1=relation_id1, domain2=relation_id2)
        # 关系域删除
        deletedomain_url1 = "/api/document-domain-management/v1/domain/%s" % relation_id1
        delete_child1 = Http_client()
        delete_child1.delete(url=deletedomain_url1, header='{"Content-Type":"application/json"}')
        deletedomain_url2 = "/api/document-domain-management/v1/domain/%s" % relation_id2
        delete_child2 = Http_client()
        delete_child2.delete(url=deletedomain_url2, header='{"Content-Type":"application/json"}')
        # 删除子域凭据
        CommonAuthCredentialMgnt().del_credential(host=child_host1, credential_id=credential_id1)
        CommonAuthCredentialMgnt().del_credential(host=child_host2, credential_id=credential_id2)
        # 删除策略配置
        CommonDocPolicyMgnt().DeletePolicy(policyid)

    def test_BindMultiChild200(self, teardown):
        policyid = teardown[0]
        relation_id1 = teardown[1]
        relation_id2 = teardown[2]
        # 调用绑定子域接口
        bind_child = Http_client()
        bindurl = "/api/document-domain-management/v1/policy-tpl/%s/bound-domain/%s,%s" % (
            policyid, relation_id1, relation_id2)
        bind_child.put(url=bindurl, header='{"Content-Type":"application/json"}')
        assert bind_child.status_code == 200
        # 调用与文档域绑定的策略配置接口，验证绑定成功
        binded1 = CommonDocPolicyMgnt().GetBindedPolicy(relation_id1)
        policyid == binded1["id"]
        binded2 = CommonDocPolicyMgnt().GetBindedPolicy(relation_id2)
        policyid == binded2["id"]


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_BindMultiChild200.py'])
