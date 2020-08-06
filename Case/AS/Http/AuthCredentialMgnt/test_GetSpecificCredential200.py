import pytest
import allure
from functools import lru_cache
from Common.http_request import Http_client
from Common.get_token import Token
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt


@lru_cache()
def get_token(host=None):
    access_token = Token(host=host).get_token()["access_token"]
    return access_token


@pytest.mark.ASP_4581
@pytest.mark.high
@allure.feature("认证凭据管理")
class Test_GetSpecificCredential200(object):
    @allure.testcase("10722 查看指定认证凭据--查看成功--200")
    @pytest.fixture(scope="function")
    def create_two_credential(self, metadata_host):
        child_host = metadata_host["child.eisoo.com"]
        child_host = (child_host.split(":")[1]).strip("/")
        # 生成平级域和父子域凭据
        result1 = CommonAuthCredentialMgnt().create_credential(host=child_host)
        result2 = CommonAuthCredentialMgnt().create_credential(host=child_host, credential_type="child")
        credential1 = result1[1]
        credential2 = result2[1]
        yield credential1, credential2, child_host
        CommonAuthCredentialMgnt().del_credential(host=child_host, credential_id=credential1)
        CommonAuthCredentialMgnt().del_credential(host=child_host, credential_id=credential2)

    def test_GetSpecificCredential200(self, create_two_credential):
        credential1 = create_two_credential[0]
        credential2 = create_two_credential[1]
        child_host = create_two_credential[2]
        get_client = Http_client()
        token = get_token(host=child_host)
        get_url = "https://" + "{host}/api/document-domain-management/" \
                               "v1/credential/{id}".format(host=child_host, id=credential1)
        get_client.get(url=get_url, header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        assert get_client.status_code == 200
        assert get_client.jsonResponse["credential_id"] == credential1
        get_url = "https://" + "{host}/api/document-domain-management/" \
                               "v1/credential/{id}".format(host=child_host, id=credential2)
        get_client.get(url=get_url, header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        assert get_client.status_code == 200
        assert get_client.jsonResponse["credential_id"] == credential2
