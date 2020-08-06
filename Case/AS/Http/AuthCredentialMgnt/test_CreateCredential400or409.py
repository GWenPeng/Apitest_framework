import pytest
import allure
from Common.readjson import JsonRead
from Common.http_request import Http_client
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt
from Case.AS.Http.DocPolicyMgnt.CommonDocPolicyMgnt import CommonDocPolicyMgnt


@pytest.mark.ASP_4581
@pytest.mark.medium
@allure.feature("认证凭据管理")
class Test_CreateCredential400or409(object):
    @allure.testcase("10702 新建认证凭据--缺少必填参数--400")
    @allure.testcase("10703 新建认证凭据--必填参数无值--400")
    @allure.testcase("10705 新建认证凭据--参数名称错误--400")
    @allure.testcase("10706 新建认证凭据--参数类型错误--400")
    @pytest.mark.parametrize(argnames="jsondata,remark",
                             argvalues=JsonRead("AS\\Http\\AuthCredentialMgnt"
                                                "\\testdata\\test_CreateCredential400.json").dict_value_join())
    def test_create_credential400(self, jsondata, remark, metadata_host):
        child_host = metadata_host["child.eisoo.com"]
        child_host = (child_host.split(":")[1]).strip("/")
        create_client = Http_client()
        token = CommonDocPolicyMgnt().get_token(host=child_host)
        post_url = "https://" + "{host}/api/document-domain-management/v1/credential".format(host=child_host)
        create_client.post(url=post_url,
                           jsondata=jsondata,
                           header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        # print(create_client.status_code, create_client.jsonResponse)
        assert create_client.status_code == 400
        assert create_client.jsonResponse["code"] == 400000000
        assert create_client.jsonResponse["message"] == "Invalid request."

    @allure.testcase("10707 新建认证凭据--重复添加父子域--409")
    @pytest.fixture(scope="function")
    def create_credential(self, metadata_host):
        child_host = metadata_host["child.eisoo.com"]
        child_host = (child_host.split(":")[1]).strip("/")
        # 新建父子域凭据
        credential_id = CommonAuthCredentialMgnt().create_credential(host=child_host, credential_type="child")
        yield child_host
        CommonAuthCredentialMgnt().del_credential(host=child_host, credential_id=credential_id[1])

    def test_create_credential409(self, create_credential):
        child_host = create_credential
        create_client = Http_client()
        token = CommonDocPolicyMgnt().get_token(host=child_host)
        post_url = "https://" + "{host}/api/document-domain-management/v1/credential".format(host=child_host)
        create_client.post(url=post_url,
                           jsondata={"credential_type": "child"},
                           header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        # print(create_client.status_code, create_client.jsonResponse)
        assert create_client.status_code == 409
        assert create_client.jsonResponse["code"] == 409014000
        assert create_client.jsonResponse["message"] == "Conflict resource."
