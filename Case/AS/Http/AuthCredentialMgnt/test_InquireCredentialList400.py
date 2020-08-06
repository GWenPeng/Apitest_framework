import pytest
import allure
from functools import lru_cache
from Common.readjson import JsonRead
from Common.http_request import Http_client
from Common.get_token import Token


@lru_cache()
def get_token(host=None):
    access_token = Token(host=host).get_token()["access_token"]
    return access_token


@pytest.mark.ASP_4581
@pytest.mark.medium
@allure.feature("认证凭据管理")
class Test_InquireCredentialList400(object):
    @allure.testcase("10716 认证凭据列表查询--offset参数异常--400")
    @allure.testcase("10718 认证凭据列表查询--limit参数异常--400")
    @pytest.mark.parametrize(argnames="params,remark",
                             argvalues=JsonRead("AS\\Http\\AuthCredentialMgnt\\testdata"
                                                "\\test_InquireCredentialList400.json").dict_value_join())
    def test_InquireCredentialList_offset400(self, params, remark, metadata_host):
        child_host = metadata_host["child.eisoo.com"]
        child_host = (child_host.split(":")[1]).strip("/")
        get_client = Http_client()
        token = get_token(host=child_host)
        get_url = "https://" + "{host}/api/document-domain-management/v1/credential".format(host=child_host)
        get_client.get(url=get_url,
                       params=params,
                       header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        assert get_client.status_code == 400
        assert get_client.jsonResponse["code"] == 400000000
        assert get_client.jsonResponse["message"] == "Invalid request."
