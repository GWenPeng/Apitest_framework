import pytest
import allure
import sys

sys.path.append("../../../../")

from Common.http_request import Http_client
from Common.readjson import JsonRead
from .CommonDocPolicyMgnt import CommonDocPolicyMgnt
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt


@pytest.mark.ASP_344
@pytest.mark.medium
@allure.feature("文档域策略管控")
class Test_GetDomainBindedPolicy404(object):
    @allure.testcase("ID5468,用例名：获取文档域绑定的策略配置--子域获取失败--返回404")
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

    @pytest.mark.parametrize("error_url, headers, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_GetDomainBindedPolicy404.json").dict_value_join())
    def test_GetDomainBindedPolicy404(self, error_url, headers, checkpoint, teardown):
        bindpolicy_client1 = Http_client()
        bindpolicy_client1.get(url=error_url, header='{"Content-Type":"application/json"}')
        assert bindpolicy_client1.status_code == checkpoint['status_code']
        assert bindpolicy_client1.jsonResponse["code"] == checkpoint["code"]
        assert bindpolicy_client1.jsonResponse["message"] == checkpoint["message"]

        # 验证URI无域id，保留/场景
        bindpolicy_url2 = "/api/document-domain-management/v1/domain/bound-policy-tpl"
        bindpolicy_client2 = Http_client()
        bindpolicy_client2.get(url=bindpolicy_url2, header='{"Content-Type":"application/json"}')
        assert bindpolicy_client2.status_code == 404


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_GetDomainBindedPolicy404.py'])
