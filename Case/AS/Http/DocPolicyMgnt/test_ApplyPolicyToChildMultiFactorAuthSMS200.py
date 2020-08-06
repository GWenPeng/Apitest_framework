import pytest
import allure
import json
import sys
sys.path.append("../../../../")
from Common.http_request import Http_client
from ShareMgnt import ncTShareMgnt
from Common.thrift_client import Thrift_client
from .CommonDocPolicyMgnt import CommonDocPolicyMgnt
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt


@pytest.mark.ASP_344
@pytest.mark.high
@allure.feature("文档域策略管控")
class Test_ApplyPolicyToChildMultiFactorAuthSMS200(object):
    @allure.testcase("ID5712,用例名：应用策略配置--非子域应用双因子认证至子域成功--返回200")
    @pytest.fixture(scope="function")
    def teardown(self, metadata_host):
        father_host = metadata_host["replace.eisoo.com"]
        child_host = metadata_host["child.eisoo.com"]
        father_host = (father_host.split(":")[1]).strip("/")
        child_host = (child_host.split(":")[1]).strip("/")
        # 新增策略
        policyid = CommonDocPolicyMgnt().AddPolicy("{\"content\":[{\"name\":\"multi_factor_auth\","
                                                   "\"value\":{\"enable\":True,\"image_vcode\":False,\"otp\":False,"
                                                   "\"password_error_count\":50,\"sms_vcode\":True}}], "
                                                   "\"name\":\"policy\"}")
        # 获取子域凭据
        result = CommonAuthCredentialMgnt().get_credential(host=child_host, credential_type="child", note="string")
        credential_id = result[0]
        credential_key = result[1]
        # 添加子域
        relation_id1 = CommonDocPolicyMgnt().AddChildDomain1(father_host=father_host, child_host=child_host,
                                                             credential_id=credential_id, credential_key=credential_key)
        # 绑定策略和子域
        CommonDocPolicyMgnt().BindChildDomain(policyid, domain1=relation_id1)
        yield policyid, relation_id1, child_host
        # 解绑子域
        CommonDocPolicyMgnt().DeleteChildDomain(host=father_host, id=policyid, domain1=relation_id1)
        # 关系域删除
        deletedomain_url1 = "/api/document-domain-management/v1/domain/%s" % relation_id1
        delete_child1 = Http_client()
        delete_child1.delete(url=deletedomain_url1, header='{"Content-Type":"application/json"}')
        # 删除子域凭据
        CommonAuthCredentialMgnt().del_credential(host=child_host, credential_id=credential_id)
        # 删除策略配置
        CommonDocPolicyMgnt().DeletePolicy(policyid)

    def test_ApplyPolicyToChildMultiFactorAuthSMS200(self, teardown):
        policyid = teardown[0]
        relation_id1 = teardown[1]
        child_host = teardown[2]
        # 调用应用接口，应用策略至子域
        apply_client = Http_client()
        applyurl = "/api/document-domain-management/v1/policy-tpl/%s/bound-domain/%s/policy" % (policyid, relation_id1)
        apply_client.put(url=applyurl, header='{"Content-Type":"application/json"}')
        assert apply_client.status_code == 200

        # 调用获取所有策略信息,验证子域1被设置策略为锁定状态
        childpolicy = CommonDocPolicyMgnt().GetAllPolicyInfo(host=child_host)["data"]
        for name in childpolicy:
            if name["name"] == "multi_factor_auth":
                assert name["locked"] == True

        # 调用thrift接口查询对应配置项设置正确
        tc = Thrift_client(ncTShareMgnt, host=child_host)
        response = tc.client.GetCustomConfigOfString("dualfactor_auth_server_status")
        response_dict = json.loads(response)
        assert response_dict['auth_by_sms'] == True


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_ApplyPolicyToChildMultiFactorAuthSMS200.py'])
