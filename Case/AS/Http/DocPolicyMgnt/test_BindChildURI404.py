import pytest
import allure
import sys
sys.path.append("../../../../")
from Common.readjson import JsonRead
from Common.http_request import Http_client
from .CommonDocPolicyMgnt import CommonDocPolicyMgnt
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt


@pytest.mark.ASP_344
@pytest.mark.medium
@allure.feature("文档域策略管控")
class Test_BindChildURI404(object):
    @allure.testcase("ID5339,用例名：绑定子域--非子域绑定参数错误，绑定失败--返回404")
    @pytest.fixture(scope="function")
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
        yield relation_id1
        # 关系域删除
        deletedomain_url1 = "/api/document-domain-management/v1/domain/%s" % relation_id1
        delete_child1 = Http_client()
        delete_child1.delete(url=deletedomain_url1, header='{"Content-Type":"application/json"}')
        # 删除子域凭据
        CommonAuthCredentialMgnt().del_credential(host=child_host, credential_id=credential_id)
        # 删除策略配置
        CommonDocPolicyMgnt().DeletePolicy(policyid)

    @pytest.mark.parametrize("error_url, headers, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_BindChildURI404.json").dict_value_join())
    def test_BindChildURI404(self, error_url, headers, checkpoint, teardown):
        relation_id1 = teardown
        # 调用绑定子域接口
        bind_child = Http_client()
        bind_url = error_url + relation_id1
        bind_child.put(url=bind_url, header='{"Content-Type":"application/json"}')
        assert bind_child.status_code == checkpoint['status_code']
        assert bind_child.jsonResponse["code"] == checkpoint["code"]
        assert bind_child.jsonResponse["message"] == checkpoint["message"]

if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_BindChildURI404.py'])

