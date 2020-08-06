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
@pytest.mark.high
@allure.feature("认证凭据管理")
@pytest.fixture(scope="class")
def create_parallel(metadata_host):
    child_host = metadata_host["child.eisoo.com"]
    child_host = (child_host.split(":")[1]).strip("/")
    credential_list = []
    for i in range(202):
        result = CommonAuthCredentialMgnt().create_credential(host=child_host, credential_type="parallel")
        credential_list.append(result[1])
    yield child_host
    for i in credential_list:
        CommonAuthCredentialMgnt().del_credential(host=child_host, credential_id=i)


class Test_InquireCredentialList200(object):
    @allure.testcase("10717 认证凭据列表查询--offset参数正向检查--200")
    @pytest.mark.parametrize(argnames="params,checkpoint,remark",
                             argvalues=JsonRead("AS\\Http\\AuthCredentialMgnt\\testdata"
                                                "\\test_InquireCredentialList200.json").dict_value_join())
    def test_InquireCredentialList_offset200(self, params, checkpoint, remark, create_parallel):
        child_host = create_parallel
        get_client = Http_client()
        token = get_token(host=child_host)
        get_url = "https://" + "{host}/api/document-domain-management/v1/credential".format(host=child_host)
        get_client.get(url=get_url,
                       params=params,
                       header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        assert get_client.status_code == 200
        assert checkpoint["count"] == get_client.jsonResponse["count"]
        assert checkpoint["data"] == len(get_client.jsonResponse["data"])
