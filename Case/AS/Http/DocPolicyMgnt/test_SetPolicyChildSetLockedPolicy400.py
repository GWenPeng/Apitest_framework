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
class Test_SetPolicyChildSetLockedPolicy400(object):
    @allure.testcase("ID5798,用例名：设置策略内容--子域设定已被锁定的策略--返回400")
    @pytest.mark.parametrize("configuration, addpolicy", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_SetPolicyChildSetLockedPolicy400.json").dict_value_join())
    @pytest.fixture(scope='function')
    def teardown(self,configuration, addpolicy, metadata_host):
        father_host = metadata_host["replace.eisoo.com"]
        child_host = metadata_host["child.eisoo.com"]
        father_host = (father_host.split(":")[1]).strip("/")
        child_host = (child_host.split(":")[1]).strip("/")
        # 新增策略
        policyid = CommonDocPolicyMgnt().AddPolicy(addpolicy)
        # 获取子域凭据
        result = CommonAuthCredentialMgnt().get_credential(host=child_host, credential_type="child", note="string")
        credential_id = result[0]
        credential_key = result[1]
        # 添加子域
        relation_id1 = CommonDocPolicyMgnt().AddChildDomain1(father_host=father_host, child_host=child_host,
                                                             credential_id=credential_id, credential_key=credential_key)
        # 绑定策略和子域
        CommonDocPolicyMgnt().BindChildDomain(policyid, domain1=relation_id1)
        #应用策略
        CommonDocPolicyMgnt().ApplyPolicy(policyid, domain1=relation_id1)
        yield
        # 解除子域锁定
        edits = "/api/policy-management/v1/general/" + configuration + "/state"
        client = Http_client(tagname="HTTP_child1")
        client.put(url=edits, json={"locked": False}, header='{"Content-Type":"application/json"}')
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

    @pytest.mark.parametrize("configuration, addpolicy, jsondata, headers, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_SetPolicyChildSetLockedPolicy400.json").dict_value_join())
    def test_SetPolicyChildSetLockedPolicy400(self, configuration, jsondata, headers, checkpoint, teardown):
        #子域设定被锁定策略
        setpolicy_client = Http_client(tagname="HTTP_child1")
        seturl = "/api/policy-management/v1/general/" + configuration + "/value"
        setpolicy_client.put(url=seturl, data=eval(jsondata), header=headers)
        print (setpolicy_client.jsonResponse)
        assert setpolicy_client.status_code == checkpoint['status_code']


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_SetPolicyChildSetLockedPolicy400.py'])
