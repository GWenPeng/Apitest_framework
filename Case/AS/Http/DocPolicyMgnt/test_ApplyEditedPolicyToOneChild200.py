import pytest
import allure
import sys

sys.path.append("../../../../")
from Common.http_request import Http_client
from Common.readjson import JsonRead
from ShareMgnt import ncTShareMgnt
from Common.thrift_client import Thrift_client
from .CommonDocPolicyMgnt import CommonDocPolicyMgnt
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt


@pytest.mark.ASP_344
@pytest.mark.high
@allure.feature("文档域策略管控")
class Test_ApplyEditedPolicyToOneChild200(object):
    @allure.testcase("ID5375,用例名：应用策略配置--非子域应用策略至子域成功--返回200--编辑未更改和编辑策略")
    # 每条用例执行完成后执行，清除环境
    @pytest.fixture(scope="function")
    def teardown(self, metadata_host):
        father_host = metadata_host["replace.eisoo.com"]
        child_host = metadata_host["child.eisoo.com"]
        father_host = (father_host.split(":")[1]).strip("/")
        child_host = (child_host.split(":")[1]).strip("/")
        # 新增策略
        policyid = CommonDocPolicyMgnt().AddPolicy('{"content":[{"name":"password_strength_meter",'
                                                   '"value":{"enable":True,"length":22}}],"name":"policy"}')
        # 获取子域凭据
        result = CommonAuthCredentialMgnt().get_credential(host=child_host, credential_type="child", note="string")
        credential_id = result[0]
        credential_key = result[1]
        # 添加子域
        relation_id1 = CommonDocPolicyMgnt().AddChildDomain1(father_host=father_host, child_host=child_host,
                                                             credential_id=credential_id, credential_key=credential_key)
        # 绑定策略和子域
        CommonDocPolicyMgnt().BindChildDomain(policyid, domain1=relation_id1)
        yield policyid, relation_id1, child_host, father_host
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

    @pytest.mark.parametrize("jsondata", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_ApplyEditedPolicyToOneChild200.json").dict_value_join())
    def test_ApplyEditedPolicyToOneChild200(self, jsondata, teardown):
        policyid = teardown[0]
        relation_id1 = teardown[1]
        child_host = teardown[2]
        father_host = teardown[3]
        # 调用应用接口，应用策略至子域
        apply_client = Http_client()
        applyurl = "/api/document-domain-management/v1/policy-tpl/%s/bound-domain/%s/policy" % (policyid, relation_id1)
        apply_client.put(url=applyurl, header='{"Content-Type":"application/json"}')
        assert apply_client.status_code == 200

        # 调用编辑策略
        CommonDocPolicyMgnt().EditPolicy(host=father_host, id=policyid, jsondata=jsondata)

        # 再次调用应用接口，应用策略至子域
        apply_client2 = Http_client()
        applyurl2 = "/api/document-domain-management/v1/policy-tpl/%s/bound-domain/%s/policy" % (policyid, relation_id1)
        apply_client2.put(url=applyurl2, header='{"Content-Type":"application/json"}')
        assert apply_client2.status_code == 200

        # 调用获取所有策略信息,验证子域1被设置策略为锁定状态
        childpolicy = CommonDocPolicyMgnt().GetAllPolicyInfo(host=child_host)["data"]
        for name in childpolicy:
            if name["name"] == "password_strength_meter":
                assert name["locked"] == True

        # 将编辑数据的json字符串转为字典格式
        dic_jsondata = eval(jsondata[0])
        # 调用thrift接口查询对应配置项设置正确
        tc = Thrift_client(ncTShareMgnt, host=child_host)
        response = tc.client.Usrm_GetPasswordConfig()
        value = dic_jsondata['content'][0]['value']['length']
        assert response.strongPwdLength == value


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_ApplyNewPolicyToOneChild200.py'])
