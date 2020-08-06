import pytest
import allure
from functools import lru_cache
from Common.readjson import JsonRead
from Common.http_request import Http_client
from Common.get_token import Token
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt
from Case.AS.Http.DocDomainMgnt.CommonDocDomain import CommonDocDomain


@lru_cache()
def get_token(host=None):
    access_token = Token(host=host).get_token()["access_token"]
    return access_token


@pytest.mark.ASP_4581
@pytest.mark.medium
@allure.feature("认证凭据管理")
class Test_DelCredential404or405or409(object):
    @allure.testcase("10712 删除认证凭据--凭据id不存在--404--传入两个有效id")
    @pytest.fixture(scope="function")
    def create_two_credential(self, metadata_host):
        parallel_host = metadata_host["parallel.eisoo.com"]
        parallel_host = (parallel_host.split(":")[1]).strip("/")
        # 生成两个平级域凭据
        credential1 = CommonAuthCredentialMgnt().create_credential(host=parallel_host)
        credential2 = CommonAuthCredentialMgnt().create_credential(host=parallel_host)
        yield credential1, credential2, parallel_host
        CommonAuthCredentialMgnt().del_credential(host=parallel_host, credential_id=credential1[1])
        CommonAuthCredentialMgnt().del_credential(host=parallel_host, credential_id=credential2[1])

    def test_delcredential_twovaild404(self, create_two_credential):
        credential1 = create_two_credential[0][1]
        credential2 = create_two_credential[1][1]
        parallel_host = create_two_credential[2]
        # 拼接两组有效id为一个id传入
        credential_id = "{},{}".format(credential1, credential2)
        del_client = Http_client()
        token = get_token(host=parallel_host)
        del_url = "https://" + "{host}/api/document-domain-management/v1" \
                               "/credential/{id}".format(host=parallel_host, id=credential_id)
        del_client.delete(url=del_url, header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        assert del_client.status_code == 404
        assert del_client.jsonResponse["code"] == 404014000
        assert del_client.jsonResponse["message"] == "Resource not found."

    @allure.testcase("10712 删除认证凭据--凭据id不存在--404--步骤1-5")
    @pytest.mark.parametrize(argnames="credential_id,remark",
                             argvalues=JsonRead("AS\\Http\\AuthCredentialMgnt\\"
                                                "testdata\\test_DelCredential404.json").dict_value_join())
    def test_delcredential_invaild404(self, credential_id, remark, metadata_host):
        parallel_host = metadata_host["parallel.eisoo.com"]
        parallel_host = (parallel_host.split(":")[1]).strip("/")
        del_client = Http_client()
        token = get_token(host=parallel_host)
        del_url = "https://" + "{host}/api/document-domain-management/v1" \
                               "/credential/{id}".format(host=parallel_host, id=credential_id)
        del_client.delete(url=del_url, header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        assert del_client.status_code == 404
        assert del_client.jsonResponse["code"] == 404014000
        assert del_client.jsonResponse["message"] == "Resource not found."

    @allure.testcase("10711 删除认证凭据--缺少凭据id--405")
    def test_delcredential405(self, metadata_host):
        parallel_host = metadata_host["parallel.eisoo.com"]
        parallel_host = (parallel_host.split(":")[1]).strip("/")
        del_client = Http_client()
        token = get_token(host=parallel_host)
        del_url = "https://" + "{host}/api/document-domain-management/v1" \
                               "/credential".format(host=parallel_host)
        del_client.delete(url=del_url, header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        assert del_client.status_code == 405

    @allure.testcase("10713 删除认证凭据--删除已绑定认证凭据--409")
    @pytest.fixture(scope="function")
    def bind_credential(self, metadata_host):
        father_host = metadata_host["self.eisoo.com"]
        child_host = metadata_host["child.eisoo.com"]
        parallel_host = metadata_host["parallel.eisoo.com"]
        father_host = (father_host.split(":")[1]).strip("/")
        child_host = (child_host.split(":")[1]).strip("/")
        parallel_host = (parallel_host.split(":")[1]).strip("/")
        # 获取平级域和子域凭据一对~
        result1 = CommonAuthCredentialMgnt().get_credential(host=parallel_host)
        credential_id1 = result1[0]
        credential_key1 = result1[1]
        result2 = CommonAuthCredentialMgnt().get_credential(host=child_host, credential_type="child")
        credential_id2 = result2[0]
        credential_key2 = result2[1]
        # 添加平级域
        domain_id1 = CommonDocDomain().addRelationDomain(httphost=father_host, host=parallel_host, port=443,
                                                         domaintype="parallel",
                                                         credential_id=credential_id1, credential_key=credential_key1)
        # 添加父子域
        domain_id2 = CommonDocDomain().addRelationDomain(httphost=father_host, host=child_host, port=443,
                                                         domaintype="child",
                                                         credential_id=credential_id2, credential_key=credential_key2)

        yield credential_id1, credential_id2, parallel_host, child_host
        # 删除关系域和父子域凭据
        CommonDocDomain().delRelationDomain(host=father_host, uuid=domain_id1[0])
        CommonDocDomain().delRelationDomain(host=father_host, uuid=domain_id2[0])
        CommonAuthCredentialMgnt().del_credential(host=parallel_host, credential_id=credential_id1)
        CommonAuthCredentialMgnt().del_credential(host=child_host, credential_id=credential_id2)

    def test_delcredential409(self, bind_credential):
        credential_id1 = bind_credential[0]
        credential_id2 = bind_credential[1]
        parallel_host = bind_credential[2]
        child_host = bind_credential[3]
        del_client1 = Http_client()
        del_client2 = Http_client()
        token1 = get_token(host=parallel_host)
        token2 = get_token(host=child_host)
        del_url1 = "https://" + "{host}/api/document-domain-management/v1" \
                               "/credential/{id}".format(host=parallel_host, id=credential_id1)
        del_url2 = "https://" + "{host}/api/document-domain-management/v1" \
                                "/credential/{id}".format(host=child_host, id=credential_id2)
        del_client1.delete(url=del_url1,
                          header={"Content-Type": "application/json", "Authorization": "Bearer " + token1})
        del_client2.delete(url=del_url2,
                          header={"Content-Type": "application/json", "Authorization": "Bearer " + token2})
        assert del_client1.status_code == 409
        assert del_client1.jsonResponse["code"] == 409014000
        assert del_client1.jsonResponse["message"] == "Conflict resource."

        assert del_client2.status_code == 409
        assert del_client2.jsonResponse["code"] == 409014000
        assert del_client2.jsonResponse["message"] == "Conflict resource."
