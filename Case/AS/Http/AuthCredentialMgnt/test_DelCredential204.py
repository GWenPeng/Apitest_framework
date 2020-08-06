import pytest
import allure
from Common.http_request import Http_client
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt
from Case.AS.Http.DocDomainMgnt.CommonDocDomain import CommonDocDomain
from Case.AS.Http.DocPolicyMgnt.CommonDocPolicyMgnt import CommonDocPolicyMgnt


@pytest.mark.ASP_4581
@pytest.mark.high
@allure.feature("认证凭据管理")
class Test_DelCredential204(object):
    @allure.testcase("10714 删除认证凭据--删除父子域凭据--204--删除未绑定的父子域凭据")
    @pytest.fixture(scope="function")
    def create_father_credential(self, metadata_host):
        # 新建子域凭据
        child_host = metadata_host["child.eisoo.com"]
        child_host = (child_host.split(":")[1]).strip("/")
        result = CommonAuthCredentialMgnt().create_credential(host=child_host, credential_type="child")
        credential_id = result[1]
        yield credential_id, child_host
        pass

    def test_del_unbind_fathercredential204(self, create_father_credential):
        credential_id = create_father_credential[0]
        child_host = create_father_credential[1]
        # 删除未绑定的父子域凭据
        del_client = Http_client()
        token = CommonDocPolicyMgnt().get_token(host=child_host)
        del_url = "https://" + "{host}/api/document-domain-management" \
                               "/v1/credential/{id}".format(host=child_host, id=credential_id)
        del_client.delete(url=del_url, header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        assert del_client.status_code == 204
        # 查询被删除的凭据，报错404
        result = CommonAuthCredentialMgnt().get_specific_credential(host=child_host, credential_id=credential_id)
        get_status_code = result[0]
        assert get_status_code == 404

    @allure.testcase("10714 删除认证凭据--删除父子域凭据--204--删除已解绑的父子域凭据")
    @pytest.fixture(scope="function")
    def untie_father_credential(self, metadata_host):
        father_host = metadata_host["self.eisoo.com"]
        child_host = metadata_host["child.eisoo.com"]
        father_host = (father_host.split(":")[1]).strip("/")
        child_host = (child_host.split(":")[1]).strip("/")
        # 获取子域凭据并绑定
        result = CommonAuthCredentialMgnt().get_credential(host=child_host, credential_type="child")
        credential_id = result[0]
        credential_key = result[1]
        # 添加父子域
        domain_id = CommonDocDomain().addRelationDomain(httphost=father_host, host=child_host, port=443,
                                                        domaintype="child",
                                                        credential_id=credential_id, credential_key=credential_key)
        # 解绑父子域
        CommonDocDomain().delRelationDomain(host=father_host, uuid=domain_id[0])
        yield credential_id, child_host
        pass

    def test_del_untie_credential204(self, untie_father_credential):
        credential_id = untie_father_credential[0]
        child_host = untie_father_credential[1]
        token = CommonDocPolicyMgnt().get_token(host=child_host)
        # 删除被解绑的父子域凭据
        del_client = Http_client()
        token = CommonDocPolicyMgnt().get_token(host=child_host)
        del_url = "https://" + "{host}/api/document-domain-management/v1" \
                               "/credential/{id}".format(host=child_host, id=credential_id)
        del_client.delete(url=del_url, header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        assert del_client.status_code == 204
        # 查询被删除的凭据，报错404
        result = CommonAuthCredentialMgnt().get_specific_credential(host=child_host, credential_id=credential_id)
        get_status_code = result[0]
        assert get_status_code == 404

    @allure.testcase("10715 删除认证凭据--删除平级域凭据--204--删除未绑定的平级域凭据")
    @pytest.fixture(scope="function")
    def create_parallel_credential(self, metadata_host):
        parallel_host = metadata_host["parallel.eisoo.com"]
        parallel_host = (parallel_host.split(":")[1]).strip("/")
        # 获取平级域凭据
        result = CommonAuthCredentialMgnt().get_credential(host=parallel_host, credential_type="parallel")
        credential_id = result[0]
        yield credential_id, parallel_host
        pass

    def test_del_unbind_paralllelcredential204(self, create_parallel_credential):
        credential_id = create_parallel_credential[0]
        parallel_host = create_parallel_credential[1]
        # 删除未绑定的平级域凭据
        del_client = Http_client()
        token = CommonDocPolicyMgnt().get_token(host=parallel_host)
        del_url = "https://" + "{host}/api/document-domain-management/v1" \
                               "/credential/{id}".format(host=parallel_host, id=credential_id)
        del_client.delete(url=del_url, header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        assert del_client.status_code == 204
        # 查询被删除的凭据，报错404
        result = CommonAuthCredentialMgnt().get_specific_credential(host=parallel_host, credential_id=credential_id)
        get_status_code = result[0]
        assert get_status_code == 404

    @allure.testcase("10715 删除认证凭据--删除平级域凭据--204--删除被解绑的平级域凭据")
    @pytest.fixture(scope="function")
    def untie_parallel_credential(self, metadata_host):
        father_host = metadata_host["self.eisoo.com"]
        parallel_host = metadata_host["parallel.eisoo.com"]
        father_host = (father_host.split(":")[1]).strip("/")
        parallel_host = (parallel_host.split(":")[1]).strip("/")
        # 获取平级域凭据一对~
        result = CommonAuthCredentialMgnt().get_credential(host=parallel_host, credential_type="parallel")
        credential_id = result[0]
        credential_key = result[1]
        # 添加平级域
        domain_id = CommonDocDomain().addRelationDomain(httphost=father_host, host=parallel_host, port=443,
                                                        domaintype="parallel",
                                                        credential_id=credential_id, credential_key=credential_key)
        # 解绑平级域
        CommonDocDomain().delRelationDomain(host=father_host, uuid=domain_id[0])
        yield credential_id, parallel_host
        pass

    def test_del_untie_paralllelcredential204(self, untie_parallel_credential):
        credential_id = untie_parallel_credential[0]
        parallel_host = untie_parallel_credential[1]
        # 删除被解绑的平级域凭据
        del_client = Http_client()
        token = CommonDocPolicyMgnt().get_token(host=parallel_host)
        del_url = "https://" + "{host}/api/document-domain-management/v1" \
                               "/credential/{id}".format(host=parallel_host, id=credential_id)
        del_client.delete(url=del_url, header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        assert del_client.status_code == 204
        # 查询被删除的凭据，报错404
        result = CommonAuthCredentialMgnt().get_specific_credential(host=parallel_host, credential_id=credential_id)
        get_status_code = result[0]
        assert get_status_code == 404
