import pytest
import allure
from Common.http_request import Http_client
from Common.readjson import JsonRead
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt
from Case.AS.Http.DocPolicyMgnt.CommonDocPolicyMgnt import CommonDocPolicyMgnt


@pytest.mark.ASP_4581
@pytest.mark.high
@allure.feature("认证凭据管理")
class Test_CreateCredential201(object):
    @allure.testcase("10704 新建认证凭据--参数冗余--201")
    @allure.testcase("10710 新建认证凭据--note参数正向检查--201")
    @pytest.mark.parametrize(argnames="jsondata,remark",
                             argvalues=JsonRead("AS\\Http\\AuthCredentialMgnt\\"
                                                "testdata\\test_CreateCredential201.json").dict_value_join())
    def test_CreateCredential_201(self, jsondata, remark, metadata_host):
        child_host = metadata_host["child.eisoo.com"]
        child_host = (child_host.split(":")[1]).strip("/")
        create_client = Http_client()
        token = CommonDocPolicyMgnt().get_token(host=child_host)
        post_url = "https://" + "{host}/api/document-domain-management/v1/credential".format(host=child_host)
        create_client.post(url=post_url,
                           jsondata=jsondata,
                           header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        credential_id = create_client.respheaders["Location"].split("/")[-1]
        location = "/api/document-domain-management/v1/credential/{id}".format(id=credential_id)
        if create_client.status_code != 201:
            print(create_client.jsonResponse)
        else:
            assert create_client.status_code == 201
            assert create_client.respheaders["Location"] == location
            CommonAuthCredentialMgnt().del_credential(host=child_host, credential_id=credential_id)

    @allure.testcase("10708 新建认证凭据--新建父子域凭据--201")
    def test_CreateCredential_father201(self, metadata_host):
        child_host = metadata_host["child.eisoo.com"]
        child_host = (child_host.split(":")[1]).strip("/")
        # 新建父子域凭据
        create_client = Http_client()
        token = CommonDocPolicyMgnt().get_token(host=child_host)
        post_url = "https://" + "{host}/api/document-domain-management/v1/credential".format(host=child_host)
        create_client.post(url=post_url,
                           jsondata={"credential_type": "child"},
                           header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        credential_id = create_client.respheaders["Location"].split("/")[-1]
        location = "/api/document-domain-management/v1/credential/{id}".format(id=credential_id)
        # 断言新建成功/location正确
        assert create_client.status_code == 201
        assert create_client.respheaders["Location"] == location
        # 调用查看指定认证凭据,验证新建成功
        status_code = CommonAuthCredentialMgnt().get_specific_credential(host=child_host, credential_id=credential_id)
        assert status_code[0] == 200
        # 删除先前生成的父子域凭据
        CommonAuthCredentialMgnt().del_credential(host=child_host, credential_id=credential_id)
        # 验证再次生成父子域成功，note字段错误
        create_client = Http_client()
        token = CommonDocPolicyMgnt().get_token(host=child_host)
        post_url = "https://" + "{host}/api/document-domain-management/v1/credential".format(host=child_host)
        create_client.post(url=post_url,
                           jsondata={"credential_type": "child", "note111": "xx"},
                           header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        credential_id2 = create_client.respheaders["Location"].split("/")[-1]
        location = "/api/document-domain-management/v1/credential/{id}".format(id=credential_id2)
        assert create_client.status_code == 201
        assert create_client.respheaders["Location"] == location
        # 调用查看指定认证凭据,验证新建成功
        status_code = CommonAuthCredentialMgnt().get_specific_credential(host=child_host, credential_id=credential_id2)
        assert status_code[0] == 200
        # 删除生成的父子域凭据
        CommonAuthCredentialMgnt().del_credential(host=child_host, credential_id=credential_id2)

    @allure.testcase("10709 新建认证凭据--新建平级域凭据--201")
    def test_CreateCredential_parallel201(self, metadata_host):
        parallel_host = metadata_host["parallel.eisoo.com"]
        parallel_host = (parallel_host.split(":")[1]).strip("/")
        # 新建平级域凭据
        create_client = Http_client()
        token = CommonDocPolicyMgnt().get_token(host=parallel_host)
        post_url = "https://" + "{host}/api/document-domain-management/v1/credential".format(host=parallel_host)
        create_client.post(url=post_url,
                           jsondata={"credential_type": "parallel"},
                           header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        credential_id = create_client.respheaders["Location"].split("/")[-1]
        location = "/api/document-domain-management/v1/credential/{id}".format(id=credential_id)
        assert create_client.status_code == 201
        assert create_client.respheaders["Location"] == location
        # 调用查看指定认证凭据,验证新建成功
        status_code = CommonAuthCredentialMgnt().get_specific_credential(host=parallel_host, credential_id=credential_id)
        assert status_code[0] == 200
        # 验证再次生成平级域凭据成功
        create_client = Http_client()
        token = CommonDocPolicyMgnt().get_token(host=parallel_host)
        post_url = "https://" + "{host}/api/document-domain-management/v1/credential".format(host=parallel_host)
        create_client.post(url=post_url,
                           jsondata={"credential_type": "parallel", "note111": "xx"},
                           header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        credential_id2 = create_client.respheaders["Location"].split("/")[-1]
        location = "/api/document-domain-management/v1/credential/{id}".format(id=credential_id2)
        assert create_client.status_code == 201
        assert create_client.respheaders["Location"] == location
        # 调用查看指定认证凭据,验证新建成功
        status_code = CommonAuthCredentialMgnt().get_specific_credential(host=parallel_host, credential_id=credential_id2)
        assert status_code[0] == 200
        # 删除生成的平级域凭据
        CommonAuthCredentialMgnt().del_credential(host=parallel_host, credential_id=credential_id)
        CommonAuthCredentialMgnt().del_credential(host=parallel_host, credential_id=credential_id2)
