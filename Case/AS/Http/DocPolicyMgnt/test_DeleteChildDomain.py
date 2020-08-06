import pytest
import allure
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect
from .CommonDocPolicyMgnt import CommonDocPolicyMgnt
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt


@pytest.mark.ASP_344
@pytest.mark.high
@allure.feature("文档域策略管控")
class Test_DeleteChildDomain(object):
    @allure.testcase("ID5400,用例名：解绑子域--非子域解绑成功--返回200")
    @pytest.fixture(scope="function")
    def create_childdomain(self, metadata_host):
        father_host = metadata_host["replace.eisoo.com"]
        child_host1 = metadata_host["child.eisoo.com"]
        child_host2 = metadata_host["self.eisoo.com"]
        child_host3 = metadata_host["parallel.eisoo.com"]
        father_host = (father_host.split(":")[1]).strip("/")
        child_host1 = (child_host1.split(":")[1]).strip("/")
        child_host2 = (child_host2.split(":")[1]).strip("/")
        child_host3 = (child_host3.split(":")[1]).strip("/")
        # 新增策略
        policyid = CommonDocPolicyMgnt().AddPolicy('{"content":[{"name":"password_strength_meter",'
                                                   '"value":{"enable":True,"length":22}}],"name":"policy"}')
        # 获取子域凭据
        result1 = CommonAuthCredentialMgnt().get_credential(host=child_host1, credential_type="child", note="string")
        credential_id1 = result1[0]
        credential_key1 = result1[1]
        result2 = CommonAuthCredentialMgnt().get_credential(host=child_host2, credential_type="child", note="string")
        credential_id2 = result2[0]
        credential_key2 = result2[1]
        result3 = CommonAuthCredentialMgnt().get_credential(host=child_host3, credential_type="child", note="string")
        credential_id3 = result3[0]
        credential_key3 = result3[1]
        # 添加子域
        relation_id1 = CommonDocPolicyMgnt().AddChildDomain1(father_host=father_host, child_host=child_host1,
                                                             credential_id=credential_id1,
                                                             credential_key=credential_key1)
        relation_id2 = CommonDocPolicyMgnt().AddChildDomain2(father_host=father_host, child_host=child_host2,
                                                             credential_id=credential_id2,
                                                             credential_key=credential_key2)
        relation_id3 = CommonDocPolicyMgnt().AddChildDomain2(father_host=father_host, child_host=child_host3,
                                                             credential_id=credential_id3,
                                                             credential_key=credential_key3)
        # 绑定策略和子域
        CommonDocPolicyMgnt().BindChildDomain(policyid, domain1=relation_id1)
        CommonDocPolicyMgnt().BindChildDomain(policyid, domain1=relation_id2)
        CommonDocPolicyMgnt().BindChildDomain(policyid, domain1=relation_id3)
        yield policyid, relation_id1, relation_id2, relation_id3
        # 关系域删除
        deletedomain_url1 = "/api/document-domain-management/v1/domain/%s" % relation_id1
        delete_child1 = Http_client()
        delete_child1.delete(url=deletedomain_url1, header='{"Content-Type":"application/json"}')
        deletedomain_url2 = "/api/document-domain-management/v1/domain/%s" % relation_id2
        delete_child2 = Http_client()
        delete_child2.delete(url=deletedomain_url2, header='{"Content-Type":"application/json"}')
        deletedomain_url3 = "/api/document-domain-management/v1/domain/%s" % relation_id3
        delete_child3 = Http_client()
        delete_child3.delete(url=deletedomain_url3, header='{"Content-Type":"application/json"}')
        # 删除子域凭据
        CommonAuthCredentialMgnt().del_credential(host=child_host1, credential_id=credential_id1)
        CommonAuthCredentialMgnt().del_credential(host=child_host2, credential_id=credential_id2)
        CommonAuthCredentialMgnt().del_credential(host=child_host3, credential_id=credential_id3)
        # 删除策略配置
        CommonDocPolicyMgnt().DeletePolicy(policyid)

    def test_DeleteChildDomain200(self, create_childdomain):
        policyid = create_childdomain[0]
        relation_id1 = create_childdomain[1]
        relation_id2 = create_childdomain[2]
        relation_id3 = create_childdomain[3]
        # 解绑单个子域
        delete_url = "/api/document-domain-management" \
                     "/v1/policy-tpl/{id}/bound-domain/{domain}".format(id=policyid, domain=relation_id1)
        delete_client = Http_client()
        delete_client.delete(url=delete_url, header="{\"Content-Type\":\"application/json\"}")
        assert delete_client.status_code == 200
        assert delete_client.elapsed <= 20.0
        # 解绑多个子域
        delete_url = "/api/document-domain-management/v1/policy-tpl/{id}/" \
                     "bound-domain/{domain1},{domain2}".format(id=policyid, domain1=relation_id2, domain2=relation_id3)
        delete_client = Http_client()
        delete_client.delete(url=delete_url, header="{\"Content-Type\":\"application/json\"}")
        assert delete_client.status_code == 200
        assert delete_client.elapsed <= 20.0

    @allure.testcase("ID5399,用例名：解绑子域--非子域环境解绑参数错误，解绑失败--返回404")
    @allure.testcase("ID5795,用例名：解绑子域--子域环境调用解绑接口，解绑失败--返回404")
    @pytest.fixture(scope="function")
    def create_onechilddomain(self, metadata_host):
        father_host = metadata_host["replace.eisoo.com"]
        child_host1 = metadata_host["child.eisoo.com"]
        child_host2 = metadata_host["self.eisoo.com"]
        father_host = (father_host.split(":")[1]).strip("/")
        child_host1 = (child_host1.split(":")[1]).strip("/")
        child_host2 = (child_host2.split(":")[1]).strip("/")
        # 新增策略
        policyid1 = CommonDocPolicyMgnt().AddPolicy('{"content":[{"name":"password_strength_meter",'
                                                    '"value":{"enable":True,"length":22}}],"name":"policy1"}')
        policyid2 = CommonDocPolicyMgnt().AddPolicy('{"content":[{"name":"password_strength_meter",'
                                                    '"value":{"enable":True,"length":22}}],"name":"policy2"}')
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
        # 绑定策略和子域
        CommonDocPolicyMgnt().BindChildDomain(policyid1, domain1=relation_id1)
        yield policyid1, policyid2, relation_id1, relation_id2, child_host1
        # 解绑子域
        CommonDocPolicyMgnt().DeleteChildDomain(host=father_host, id=policyid1, domain1=relation_id1)
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
        CommonDocPolicyMgnt().DeletePolicy(policyid1)
        CommonDocPolicyMgnt().DeletePolicy(policyid2)

    def test_DeleteChildDomains404(self, create_onechilddomain):
        policyid1 = create_onechilddomain[0]
        policyid2 = create_onechilddomain[1]
        relation_id1 = create_onechilddomain[2]
        relation_id2 = create_onechilddomain[3]
        # 缺少策略ID参数404且删除/符号
        client = Http_client()
        delete_url = "/api/document-domain-management/v1/policy-tpl/bound-domain/11".format(domain=relation_id1)
        client.delete(url=delete_url, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 404
        assert client.text == '<html><title>404: Not Found</title><body>404: Not Found</body></html>'
        assert client.elapsed <= 20.0

        # 缺少策略ID参数404且保留/符号
        delete_url = "/api/document-domain-management/v1/policy-tpl//bound-domain/{domain}".format(domain=relation_id1)
        client.delete(url=delete_url, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 404
        assert client.text == '<html><title>404: Not Found</title><body>404: Not Found</body></html>'
        assert client.elapsed <= 20.0

        # 策略ID不存在
        delete_url = "/api/document-domain-management/v1/policy-tpl/11/bound-domain/{domain}".format(
            domain=relation_id1)
        client.delete(url=delete_url, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 404
        assert client.jsonResponse['message'] == 'Resource not found.'
        assert client.elapsed <= 20.0

        # 传入多个有效策略ID
        delete_url = "/api/document-domain-management/v1/policy-tpl" \
                     "/{id1},{id2}/bound-domain/{domain}".format(id1=policyid1, id2=policyid2, domain=relation_id1)
        client.delete(url=delete_url, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 404
        assert client.jsonResponse['message'] == 'Resource not found.'
        assert client.elapsed <= 20.0

        # 缺少子域ID
        delete_url = "/api/document-domain-management/v1/policy-tpl/{id}/bound-domain/".format(id=policyid1)
        client.delete(url=delete_url, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 405
        assert client.elapsed <= 20.0

        # 子域ID不存在
        delete_url = "/api/document-domain-management/v1/policy-tpl/{id}/bound-domain/111".format(id=policyid1)
        client.delete(url=delete_url, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 404
        assert client.jsonResponse['message'] == 'Resource not found.'
        assert client.elapsed <= 20.0

        # 子域ID存在，但为其他父域的关联子域
        delete_url = "/api/document-domain-management/v1/policy-tpl/{id}/" \
                     "bound-domain/9b04d18d-6c15-45a6-8c8c-6b8dc67a8689".format(id=policyid1)
        client.delete(url=delete_url, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 404
        assert client.jsonResponse['message'] == 'Resource not found.'
        assert client.elapsed <= 20.0

        # ID存在，但域ID为平级域
        delete_url = "/api/document-domain-management/v1/policy-tpl/{id}/" \
                     "bound-domain/9b04d18d-6c15-45a6-8c8c-6b8dc67a8689".format(id=policyid1)
        client.delete(url=delete_url, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 404
        assert client.jsonResponse['message'] == 'Resource not found.'
        assert client.elapsed <= 20.0

        # 子域ID正确，但该子域ID未绑定策略
        delete_url = "/api/document-domain-management/v1/policy-tpl/{id}/" \
                     "bound-domain/{domain}".format(id=policyid1, domain=relation_id2)
        client.delete(url=delete_url, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 404
        assert client.jsonResponse['message'] == 'Resource not found.'
        assert client.elapsed <= 20.0

        # ID存在，但该ID为自身域ID
        delete_url = "/api/document-domain-management/v1/policy-tpl/{id}/" \
                     "bound-domain/4aaf1948-e0b6-4685-b293-561f012cf284".format(id=policyid1)
        client.delete(url=delete_url, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 404
        assert client.jsonResponse['message'] == 'Resource not found.'
        assert client.elapsed <= 20.0

        # ID存在，但该ID为父域ID
        delete_url = "/api/document-domain-management/v1/policy-tpl/{id}/" \
                     "bound-domain/4aaf1948-e0b6-4685-b293-561f012cf284".format(id=policyid1)
        client.delete(url=delete_url, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 404
        assert client.jsonResponse['message'] == 'Resource not found.'
        assert client.elapsed <= 20.0

    @allure.testcase("ID6585,用例名：解绑子文档域前修改子域端口，解绑失败")
    def test_DeleteChildDomain400(self, create_onechilddomain):
        policyid1 = create_onechilddomain[0]
        relation_id1 = create_onechilddomain[2]
        child_host1 = create_onechilddomain[4]
        delete_url = "/api/document-domain-management/v1/policy-tpl/{id}/" \
                     "bound-domain/{domain}".format(id=policyid1, domain=relation_id1)
        # 修改子域端口
        conn = DB_connect()
        update_sql = "update t_relationship_domain set f_port=8001 where f_host='{host}'".format(host=child_host1)
        conn.update(update_sql)
        conn.close()
        # 解绑子文档域url
        client = Http_client()
        client.delete(url=delete_url, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 400
        assert client.jsonResponse['code'] == 400014205
        assert client.elapsed <= 20.0
        # 恢复子域端口
        conn = DB_connect()
        update_sql = "update t_relationship_domain set f_port=443 where f_host='{host}'".format(host=child_host1)
        conn.update(update_sql)
        conn.close()


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_DeleteChildDomain.py'])
