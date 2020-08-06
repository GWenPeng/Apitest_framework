import pytest
import allure
from functools import lru_cache
from Common.readjson import JsonRead
from Common.http_request import Http_client
from Common.get_token import Token
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt


@lru_cache()
def get_token(host=None):
    access_token = Token(host=host).get_token()["access_token"]
    return access_token


@pytest.mark.ASP_4581
@pytest.mark.medium
@allure.feature("认证凭据管理")
class Test_GetSpecificCredential404(object):
    @allure.testcase("10721 查看指定认证凭据--凭据id不存在--404--传入两个有效id")
    @pytest.fixture(scope="function")
    def create_two_credential(self, metadata_host):
        parallel_host = metadata_host["parallel.eisoo.com"]
        parallel_host = (parallel_host.split(":")[1]).strip("/")
        result1 = CommonAuthCredentialMgnt().create_credential(host=parallel_host)
        result2 = CommonAuthCredentialMgnt().create_credential(host=parallel_host)
        credential1 = result1[1]
        credential2 = result2[1]
        yield credential1, credential2, parallel_host
        CommonAuthCredentialMgnt().del_credential(host=parallel_host, credential_id=credential1)
        CommonAuthCredentialMgnt().del_credential(host=parallel_host, credential_id=credential2)

    def test_validcredential_not_found(self, create_two_credential):
        # 拼接成查询id
        credential_id = []
        credential_id.append(create_two_credential[0])
        credential_id.append(create_two_credential[1])
        parallel_host = create_two_credential[2]
        get_client = Http_client()
        token = get_token(host=parallel_host)
        get_url = "https://" + "{host}/api/document-domain-management/v1" \
                               "/credential/{id}".format(host=parallel_host, id=credential_id)
        get_client.get(url=get_url, header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        assert get_client.status_code == 404
        assert get_client.jsonResponse["code"] == 404014000
        assert get_client.jsonResponse["message"] == "Resource not found."

    @allure.testcase("10721 查看指定认证凭据--凭据id不存在--404")
    @pytest.mark.parametrize(argnames="credential_id",
                             argvalues=JsonRead("AS\\Http\\AuthCredentialMgnt\\testdata"
                                                "\\test_GetSpecificCredential404.json").dict_value_join())
    def test_invalidcredential_not_found(self, credential_id, metadata_host):
        parallel_host = metadata_host["parallel.eisoo.com"]
        parallel_host = (parallel_host.split(":")[1]).strip("/")
        get_client = Http_client()
        token = get_token(host=parallel_host)
        get_url = "https://" + "{host}/api/document-domain-management/v1" \
                               "/credential/{id}".format(host=parallel_host, id=credential_id)
        get_client.get(url=get_url, header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        assert get_client.status_code == 404
        assert get_client.jsonResponse["code"] == 404014000
        assert get_client.jsonResponse["message"] == "Resource not found."

