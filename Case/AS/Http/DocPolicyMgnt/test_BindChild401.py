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
class Test_BindOneChild401(object):
    @allure.testcase("10820 解绑子域--关系域id/secret不正确--返回401 ")
    @pytest.fixture(scope="function")
    def teardown(self, metadata_host):
        father_host = metadata_host["replace.eisoo.com"]
        child_host1 = metadata_host["child.eisoo.com"]
        father_host = (father_host.split(":")[1]).strip("/")
        child_host1 = (child_host1.split(":")[1]).strip("/")
        # 新增策略
        policyid = CommonDocPolicyMgnt().AddPolicy('{"content":[{"name":"password_strength_meter",'
                                                   '"value":{"enable":False,"length":12}}],'
                                                   '"name":"policy1"}')
        # 获取子域凭据
        result = CommonAuthCredentialMgnt().get_credential(host=child_host1, credential_type="child", note="string")
        credential_id = result[0]
        credential_key = result[1]
        # 添加子域
        relation_id1 = CommonDocPolicyMgnt().AddChildDomain1(father_host=father_host, child_host=child_host1,
                                                             credential_id=credential_id, credential_key=credential_key)
        yield policyid, relation_id1, father_host, child_host1
        # 关系域删除
        deletedomain_url1 = "/api/document-domain-management/v1/domain/%s" % relation_id1
        delete_child1 = Http_client()
        delete_child1.delete(url=deletedomain_url1, header='{"Content-Type":"application/json"}')
        # 删除子域凭据
        CommonAuthCredentialMgnt().del_credential(host=child_host1, credential_id=credential_id)
        # 删除策略配置
        CommonDocPolicyMgnt().DeletePolicy(policyid)

    def test_BindOneChild401(self, teardown):
        policyid = teardown[0]
        relation_id1 = teardown[1]
        father_host = teardown[2]
        child_host1 = teardown[3]
        # 修改数据库中对应关系域f_token
        db = DB_connect(host=father_host)
        get_sql = "select f_token from t_relationship_domain where f_host='{host}'".format(host=child_host1)
        f_token = db.select_one(get_sql)
        update_sql = "update t_relationship_domain set f_token='111' where f_host='{host}'".format(host=child_host1)
        db.update(sql=update_sql)
        db.close()
        # 调用绑定子域接口
        bind_child = Http_client()
        bindurl = "/api/document-domain-management/v1/policy-tpl/%s/bound-domain/%s" % (policyid, relation_id1)
        bind_child.put(url=bindurl, header='{"Content-Type":"application/json"}')
        assert bind_child.status_code == 401
        assert bind_child.jsonResponse["code"] == 401014000
        assert bind_child.jsonResponse["message"] == "Unauthorization."
        db = DB_connect(host=father_host)
        update_sql = "update t_relationship_domain set f_token='{token}' where f_host='{host}'".format(token=f_token[0],
                                                                                                       host=child_host1)
        db.update(sql=update_sql)
        db.close()


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_BindOneChild400.py'])
