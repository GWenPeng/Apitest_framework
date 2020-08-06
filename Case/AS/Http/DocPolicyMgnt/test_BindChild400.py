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
class Test_BindOneChild400(object):
    @allure.testcase("ID5970,用例名：解绑子文档域--解绑前修改子域端口，解绑失败--返回400 ")
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
        # 修改数据库子域端口
        db = DB_connect()
        update_sql = "update t_relationship_domain set f_port=445 where f_host='{host}'".format(host=child_host)
        db.update(update_sql)
        yield policyid, relation_id1
        # 修改数据库子域端口
        db = DB_connect()
        update_sql = "update t_relationship_domain set f_port=443 where f_host='{host}'".format(host=child_host)
        db.update(update_sql)
        # 关系域删除
        deletedomain_url1 = "/api/document-domain-management/v1/domain/%s" % relation_id1
        delete_child1 = Http_client()
        delete_child1.delete(url=deletedomain_url1, header='{"Content-Type":"application/json"}')
        # 删除子域凭据
        CommonAuthCredentialMgnt().del_credential(host=child_host, credential_id=credential_id)
        # 删除策略配置
        CommonDocPolicyMgnt().DeletePolicy(policyid)

    def test_BindOneChild400(self, teardown):
        policyid = teardown[0]
        relation_id1 = teardown[1]
        # 调用绑定子域接口
        bind_child = Http_client()
        bindurl = "/api/document-domain-management/v1/policy-tpl/%s/bound-domain/%s" % (policyid, relation_id1)
        bind_child.put(url=bindurl, header='{"Content-Type":"application/json"}')
        assert bind_child.status_code == 400
        assert bind_child.jsonResponse["code"] == 400014205
        assert bind_child.jsonResponse["message"] == "Linked failed"


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_BindOneChild400.py'])
