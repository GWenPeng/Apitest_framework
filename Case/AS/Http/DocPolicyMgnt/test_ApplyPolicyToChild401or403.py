import pytest
import allure
import sys
sys.path.append("../../../../")
from Common.http_request import Http_client
from .CommonDocPolicyMgnt import CommonDocPolicyMgnt
from DB_connect.mysqlconnect import DB_connect
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt


@pytest.mark.ASP_344
@pytest.mark.medium
@allure.feature("文档域策略管控")
class Test_ApplyPolicyToChild401or403(object):
    @allure.testcase("ID5376,用例名：应用策略配置--子域应用策略至其他域环境失败--返回403或404")
    @pytest.fixture(scope="function")
    def teardown(self, metadata_host):
        father_host = metadata_host["replace.eisoo.com"]
        child_host1 = metadata_host["child.eisoo.com"]
        child_host2 = metadata_host["parallel.eisoo.com"]
        father_host = (father_host.split(":")[1]).strip("/")
        child_host1 = (child_host1.split(":")[1]).strip("/")
        child_host2 = (child_host2.split(":")[1]).strip("/")
        # 新增策略
        policyid = CommonDocPolicyMgnt().AddPolicy('{"content":[{"name":"password_strength_meter",'
                                                   '"value":{"enable":True,"length":25}}],"name":"policy"}')
        # 获取子域凭据
        result1 = CommonAuthCredentialMgnt().get_credential(host=child_host1, credential_type="child")
        credential_id1 = result1[0]
        credential_key1 = result1[1]
        result2 = CommonAuthCredentialMgnt().get_credential(host=child_host2, credential_type="child")
        credential_id2 = result2[0]
        credential_key2 = result2[1]
        # 添加子域
        relation_id1 = CommonDocPolicyMgnt().AddChildDomain1(father_host=father_host, child_host=child_host1,
                                                             credential_id=credential_id1,
                                                             credential_key=credential_key1)
        relation_id2 = CommonDocPolicyMgnt().AddChildDomain2(father_host=father_host, child_host=child_host2,
                                                             credential_id=credential_id2,
                                                             credential_key=credential_key2)
        # 绑定策略和子域
        CommonDocPolicyMgnt().BindChildDomain(policyid, domain1=relation_id1, domain2=relation_id2)
        yield policyid, relation_id1, relation_id2, child_host1, father_host, credential_key1
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

    def test_ApplyinvalidPolicyToChild403(self, teardown):
        policyid = teardown[0]
        relation_id1 = teardown[1]
        relation_id2 = teardown[2]
        child_host1 = teardown[3]
        # 调用应用接口，验证子域应用至自身
        apply_client1 = Http_client(tagname="HTTP_child1")
        applyurl1 = "/api/document-domain-management/v1/policy-tpl/%s/bound-domain/%s/policy" % (policyid, relation_id1)
        token = CommonDocPolicyMgnt().get_token(host=child_host1)
        apply_client1.put(url=applyurl1, header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        print(apply_client1.jsonResponse)
        assert apply_client1.status_code == 403
        assert apply_client1.jsonResponse["code"] == 403014000
        assert apply_client1.jsonResponse["message"] == "No permission to do this operation."

        # 调用应用接口，验证子域应用策略至其他有效子域
        apply_client2 = Http_client(tagname="HTTP_child1")
        applyurl2 = "/api/document-domain-management/v1/policy-tpl/%s/bound-domain/%s/policy" % (policyid, relation_id2)
        token = CommonDocPolicyMgnt().get_token(host=child_host1)
        apply_client2.put(url=applyurl2, header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        print(apply_client2.jsonResponse)
        assert apply_client2.status_code == 403
        assert apply_client2.jsonResponse["code"] == 403014000
        assert apply_client2.jsonResponse["message"] == "No permission to do this operation."

        # 调用应用接口，验证子域应用策略至不存在子域环境
        apply_client2 = Http_client(tagname="HTTP_child1")
        applyurl2 = "/api/document-domain-management/v1/policy-tpl/%s/bound-domain/1%s/policy" % (policyid, relation_id2)
        token = CommonDocPolicyMgnt().get_token(host=child_host1)
        apply_client2.put(url=applyurl2, header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        print(apply_client2.jsonResponse)
        assert apply_client2.status_code == 403
        assert apply_client2.jsonResponse["code"] == 403014000
        assert apply_client2.jsonResponse["message"] == "No permission to do this operation."

    @allure.testcase("10816 应用策略配置--关系域id/secret不正确--返回401")
    def test_ApplyPolicyToChild401(self, teardown):
        policyid = teardown[0]
        relation_id1 = teardown[1]
        child_host1 = teardown[3]
        father_host = teardown[4]
        # 修改数据库中对应关系域f_token
        db = DB_connect(host=father_host)
        get_sql = "select f_token from t_relationship_domain where f_host='{host}'".format(host=child_host1)
        f_token = db.select_one(get_sql)
        print(f_token[0])
        update_sql = "update t_relationship_domain set f_token='111' where f_host='{host}'".format(host=child_host1)
        db.update(sql=update_sql)
        db.close()
        apply_client1 = Http_client()
        apply_url = "/api/document-domain-management/v1/policy-tpl/%s/bound-domain/%s/policy" % (policyid, relation_id1)
        apply_client1.put(url=apply_url,
                          header={"Content-Type": "application/json"})
        assert apply_client1.status_code == 401
        assert apply_client1.jsonResponse["code"] == 401014000
        assert apply_client1.jsonResponse["message"] == "Unauthorization."
        db = DB_connect(host=father_host)
        update_sql = "update t_relationship_domain set f_token='{token}' where f_host='{host}'".format(token=f_token[0], host=child_host1)
        db.update(sql=update_sql)
        db.close()


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_ApplyPolicyToChild403.py'])
