# coding=utf-8
import pytest
import allure

from Common.http_request import Http_client
from Common.readjson import JsonRead
from .CommonDocDomain import CommonDocDomain
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt


@pytest.mark.ASP_317
@allure.feature("域详情编辑接口")
class Test_PutMgntV1DomainDetail(object):
    """
    Test_suite测试域详情编辑接口
    """

    @allure.testcase("5280,域详情编辑--平级域数据port,credential_id,credential_key更改，返回200")
    @allure.testcase("5273,域详情编辑--校验字段非必填项值为null，返回200")
    @allure.testcase("5272,域详情编辑--非必填项值为空，返回200 ")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/PutMgntV1DomainDetailParallel.json").dict_value_join())
    def test_PutDocDomainDetailParallel(self, url, header, jsondata, checkpoint):
        """
        修改平级域port、credential_id、credential_key、secret
        :param url: 域详情编辑接口请求地址
        :param header: 请求头
        :param jsondata: 请求body参数
        :param checkpoint: 断言，检查点
        :return: None
        """

        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.180.162")  # 清空一个平级域关系域
        uuid = CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="parallel")[0]  # 添加一个平级域
        # header = eval(header)
        # token = get_token()
        # header["Authorization"] = "Bearer " + token
        jsondata = eval(jsondata)
        credential = CommonDocDomain.get_credential(host="10.2.180.162", domain_type="parallel")
        if "credential_id" in jsondata:
            if jsondata["credential_id"] == "admin":
                jsondata["credential_id"] = credential[0]
                print(jsondata)
        if "credential_key" in jsondata:
            if jsondata["credential_key"] == "eisoo.com":
                jsondata["credential_key"] = credential[1]
        client = Http_client(tagname="HTTPGWP")
        client.put(url=url + uuid, header=header, json=jsondata)
        print(client.jsonResponse)
        assert client.status_code == checkpoint['status_code']
        if "code" in checkpoint:
            assert client.jsonResponse["code"] == checkpoint["code"]
        if "message" in checkpoint:
            assert client.jsonResponse["message"] == checkpoint["message"]
        print(client.jsonResponse)
        assert client.elapsed <= 20.0

    @pytest.mark.high
    @allure.testcase("5279,域详情编辑--子域数据port,credential_id,credential_key更改，返回200")
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/PutMgntV1DomainDetailChild.json").dict_value_join())
    def test_PutDocDomainDetailChild(self, url, header, jsondata, checkpoint):
        """
        修改子域port、credential_id、credential_key、secret
        :param url: 域详情编辑接口请求地址
        :param header: 请求头
        :param jsondata: 请求body参数
        :param checkpoint: 断言，检查点
        :return: None
         """
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.208")  # 清空一个子域关系域
        domain_data = CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")
        uuid = domain_data[0]  # 添加一个平级域
        jsondata = eval(jsondata)
        credential = CommonDocDomain.get_credential(host="10.2.176.208", domain_type="child")
        if "credential_id" in jsondata:
            if jsondata["credential_id"] == "admin":
                jsondata["credential_id"] = credential[0]

        if "credential_key" in jsondata:
            if jsondata["credential_key"] == "eisoo.com":
                jsondata["credential_key"] = credential[1]

        client = Http_client(tagname="HTTPGWP")
        client.put(url=url + uuid, header=header, json=jsondata)
        assert client.status_code == checkpoint['status_code']
        print(client.jsonResponse)
        if "code" in checkpoint:
            assert client.jsonResponse["code"] == checkpoint["code"]
        if "message" in checkpoint:
            assert client.jsonResponse["message"] == checkpoint["message"]
        assert client.elapsed <= 20.0
        CommonDocDomain().setRelationDomain(uuid=uuid, domaintype="child", credential_id=domain_data[1],
                                            credential_key=domain_data[2])

    @pytest.fixture(scope="function", params=[("child", "parallel"), ("parallel", "child")])
    def setupAddRelationDomain(self, request, fatherdomain="10.2.176.245", domain="10.2.180.162",
                               otherdomain="10.2.176.176"):
        """

        :return:
        """
        CommonDocDomain().clearRelationDomain(host=fatherdomain)  # 清空父域的关系域
        CommonDocDomain().clearRelationDomain(host=domain)  # 清空一个关系域
        CommonDocDomain().clearRelationDomain(host=otherdomain)  # 清空一个关系域
        print(request.param[0])
        uuid = CommonDocDomain().addRelationDomain(host=domain, domaintype=request.param[0], httphost=fatherdomain)
        return request.param[1], uuid

    @allure.testcase("5278,域详情编辑--域类型修改失败，返回409")
    def test_PutDocDomainDetail409(self, setupAddRelationDomain):
        """

        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.put(url="/api/document-domain-management/v1/domain/" + setupAddRelationDomain[1][0],
                   header={"Content-Type": "application/json"},
                   json={"type": setupAddRelationDomain[0], "port": 80, "credential_id": setupAddRelationDomain[1][1],
                         "credential_key": setupAddRelationDomain[1][2],
                         "secret": "secret"})
        assert client.status_code == 409

    @allure.testcase("5277,域详情编辑--不存在的Id，返回404")
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/PutDocDomainDetail404.json").dict_value_join())
    def test_PutDocDomainDetail404(self, url, header, jsondata, checkpoint):
        """
        :return:
        """
        # header = eval(header)
        # token = get_token()
        # header["Authorization"] = "Bearer " + token
        client = Http_client(tagname="HTTPGWP")
        client.put(url=url, header=header, json=jsondata)
        assert client.status_code == checkpoint["status_code"]
        assert client.jsonResponse["cause"] == checkpoint["cause"]
        print(client.jsonResponse)
        assert client.jsonResponse["detail"]["notfound_params"][0] == checkpoint["detail.notfound_resource"]

    @allure.testcase("5276,域详情编辑--端口号非法,返回400")
    @allure.testcase("5275,域详情编辑--type类型不存在，返回400")
    @allure.testcase("5274,域详情编辑--参数类型错误，返回400")
    @allure.testcase("5271,域详情编辑--校验字段值为null，返回400")
    @pytest.mark.parametrize("url,header,jsondata,checkpoint,domaintype",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/PutDocDomainDetail400.json").dict_value_join())
    def test_PutDocDomainDetail400(self, url, header, jsondata, checkpoint, domaintype):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :return:
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")
        CommonDocDomain().clearRelationDomain(host="10.2.180.162")
        CommonDocDomain().clearRelationDomain(host="10.2.176.176")
        credential = CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype=domaintype)
        uuid = credential[0]
        # jsondata = eval(jsondata)
        # credential = CommonDocDomain.get_credential(host="10.2.180.162", domain_type="child")
        if "credential_id" in jsondata:
            if jsondata["credential_id"] == "admin":
                jsondata["credential_id"] = credential[1]

        if "credential_key" in jsondata:
            if jsondata["credential_key"] == "eisoo.com":
                jsondata["credential_key"] = credential[2]

        client = Http_client(tagname="HTTPGWP")
        client.put(url=url + uuid, header=header, json=jsondata)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if "cause" in checkpoint:
            assert client.jsonResponse["cause"] == checkpoint["cause"]
        if "detail.invalid_params" in checkpoint:
            assert client.jsonResponse["detail"]["invalid_params"][0] == checkpoint["detail.invalid_params"]
        if "message" in checkpoint:
            assert client.jsonResponse["message"] == checkpoint["message"]
        if "code" in checkpoint:
            assert client.jsonResponse["code"] == checkpoint["code"]
        # print(client.jsonResponse)

    @allure.testcase("5269,域详情编辑--校验字段是否必填，返回400")
    @allure.testcase("5270,域详情编辑--校验字段值为空，返回400")
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/PutDocDomainDetailKeyEmpty.json").dict_value_join())
    def test_PutDocDomainDetailKeyEmpty(self, url, header, jsondata, checkpoint):
        """
        :param self:
        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :return:
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")
        CommonDocDomain().clearRelationDomain(host="10.2.180.162")
        uuid = CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="child")[0]
        # token = get_token()
        # header["Authorization"] = "Bearer " + token
        client = Http_client(tagname="HTTPGWP")
        client.put(url=url + uuid, header=header, json=jsondata)
        assert client.status_code == checkpoint["status_code"]
        assert client.jsonResponse["cause"] == checkpoint["cause"]
        print(client.jsonResponse)

    def test__is_required_credential_id(self, metadata_host):
        """
        校验凭据是否必填
        :return:
        """
        CommonDocDomain().clearRelationDomain(host=metadata_host["self.eisoo.com"].split("//")[-1])
        uuid = CommonDocDomain().addRelationDomain(host=metadata_host["child.eisoo.com"].split("//")[-1],
                                                   domaintype="child")[
            0]
        client = Http_client()
        client.put(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain/" + uuid,
                   header={"Content-Type": "application/json"},
                   json={"type": "child", "port": 443})
        print(client.jsonResponse)
        assert client.status_code == 400
        assert client.jsonResponse["code"] == 400000000
        assert client.jsonResponse["message"] == 'Invalid request.'
        assert client.jsonResponse["cause"] == "'credential_id' is a required property"
        assert client.jsonResponse["detail"] == {'invalid_params': [{'type': 'child', 'port': 443}]}

        client.put(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain/" + uuid,
                   header={"Content-Type": "application/json"},
                   json={"type": "child", "port": 443, "credential_id": "credential_id"})
        print(client.jsonResponse)
        assert client.status_code == 400
        assert client.jsonResponse["code"] == 400000000
        assert client.jsonResponse["message"] == 'Invalid request.'
        assert client.jsonResponse["cause"] == "'credential_key' is a required property"
        assert client.jsonResponse["detail"] == {
            'invalid_params': [{'type': 'child', 'port': 443, "credential_id": "credential_id"}]}

        uuid = CommonDocDomain().addRelationDomain(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                                   domaintype="parallel")[0]
        client.put(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain/" + uuid,
                   header={"Content-Type": "application/json"},
                   json={"type": "parallel", "port": 443})
        print(client.jsonResponse)
        assert client.status_code == 200

    def test_is_not_exist_credential_id(self, metadata_host):
        """
        修改使用不存在的凭据
        :return:
        """
        CommonDocDomain().clearRelationDomain(host=metadata_host["self.eisoo.com"].split("//")[-1])
        uuid = CommonDocDomain().addRelationDomain(host=metadata_host["child.eisoo.com"].split("//")[-1],
                                                   domaintype="child")[
            0]
        client = Http_client()
        client.put(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain/" + uuid,
                   header={"Content-Type": "application/json"},
                   json={"type": "child", "port": 443, "credential_id": "a1dd3cae-bfc61-4cb91-82c9-db6136e1566e",
                         "credential_key": "8LkG71NrYOBwIg"})
        print(client.jsonResponse)
        assert client.status_code == 401
        assert client.jsonResponse["code"] == 401014201
        assert client.jsonResponse["message"] == 'Invalid client'
        assert client.jsonResponse["cause"] == 'invalid_client'

        uuid = CommonDocDomain().addRelationDomain(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                                   domaintype="parallel")[0]
        client.put(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain/" + uuid,
                   header={"Content-Type": "application/json"},
                   json={"type": "parallel", "port": 443, "credential_id": "a1dd3cae-bfc6-4c6b91-82c9-db6136e1566e",
                         "credential_key": "8LkG7Nr6YOBwIg", "secret": "secret"})
        print(client.jsonResponse)
        assert client.status_code == 401
        assert client.jsonResponse["code"] == 401014201
        assert client.jsonResponse["message"] == 'Invalid client'
        assert client.jsonResponse["cause"] == 'invalid_client'

    def test_is_del_credential_id(self, metadata_host):
        """
        修改使用被删除的凭据
        :return:
        """
        CommonDocDomain().clearRelationDomain(host=metadata_host["self.eisoo.com"].split("//")[-1])
        domain_data = CommonDocDomain().addRelationDomain(host=metadata_host["child.eisoo.com"].split("//")[-1],
                                                          domaintype="child")
        CommonDocDomain().delRelationDomain(host=metadata_host["self.eisoo.com"].split("//")[-1], uuid=domain_data[0])
        CommonAuthCredentialMgnt().del_credential(host=metadata_host["child.eisoo.com"].split("//")[-1],
                                                  credential_id=domain_data[1])
        uuid = CommonDocDomain().addRelationDomain(host=metadata_host["child.eisoo.com"].split("//")[-1],
                                                   domaintype="child")[0]
        credential_id = domain_data[1]
        credential_key = domain_data[2]
        client = Http_client()
        client.put(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain/" + uuid,
                   header={"Content-Type": "application/json"},
                   json={"type": "child", "port": 443, "credential_id": credential_id,
                         "credential_key": credential_key})
        print(credential_id, credential_key)
        print(client.jsonResponse)
        assert client.status_code == 403
        assert client.jsonResponse["code"] == 403014000
        assert client.jsonResponse["message"] == "No permission to do this operation."
        assert client.jsonResponse["cause"] == "client_id does not match"

        domain_data = CommonDocDomain().addRelationDomain(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                                          domaintype="parallel")
        credential_id = domain_data[1]
        credential_key = domain_data[2]
        CommonDocDomain().delRelationDomain(host=metadata_host["self.eisoo.com"].split("//")[-1], uuid=domain_data[0])
        CommonAuthCredentialMgnt().del_credential(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                                  credential_id=domain_data[1])
        uuid = CommonDocDomain().addRelationDomain(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                                   domaintype="parallel")[0]
        client.put(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain/" + uuid,
                   header={"Content-Type": "application/json"},
                   json={"type": "parallel", "port": 443, "credential_id": credential_id,
                         "credential_key": credential_key})
        print(credential_id, credential_key)
        print(client.jsonResponse)
        assert client.status_code == 403
        assert client.jsonResponse["code"] == 403014000
        assert client.jsonResponse["message"] == "No permission to do this operation."
        assert client.jsonResponse["cause"] == "client_id does not match"

    # @pytest.mark.skip(reason="ASP-8113 文档域域详情编辑，修改平级域凭据为无效凭据，结果修改成功了")
    def test_invalid_credential_id(self, metadata_host):
        """
        修改使用无效的凭据 子域不存在此场景
        :return:
        """
        CommonDocDomain().clearRelationDomain(host=metadata_host["self.eisoo.com"].split("//")[-1])

        uuid = CommonDocDomain().addRelationDomain(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                                   domaintype="parallel")[0]
        credential = CommonDocDomain.get_credential(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                                    domain_type="parallel", f_status="invalid")
        client = Http_client()
        client.put(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain/" + uuid,
                   header={"Content-Type": "application/json"},
                   json={"type": "parallel", "port": 443, "credential_id": credential[0],
                         "credential_key": credential[1]})
        print(client.jsonResponse)
        assert client.status_code == 409
        assert client.jsonResponse["code"] == 409014206
        assert client.jsonResponse["message"] == "Credential type is not available"
        assert client.jsonResponse["cause"] == "Credential type is not available"
        assert client.jsonResponse["detail"] == [credential[0], credential[1]]

    @pytest.fixture(scope="function")
    def clear_data(self, metadata_host):
        """

        :param metadata_host:
        :return:
        """
        yield
        CommonDocDomain().clearRelationDomain(
            host=[metadata_host["self.eisoo.com"].split("//")[-1], metadata_host["child.eisoo.com"].split("//")[-1]])

        CommonDocDomain.del_invalid_credential(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                               domain_type="parallel")

    def test_repeat_used_credential_id(self, metadata_host, clear_data):
        """
        使用已使用的凭据 使用别人已使用的凭据
        :return:
        """
        CommonDocDomain().clearRelationDomain(host=metadata_host["self.eisoo.com"].split("//")[-1])
        uuid = CommonDocDomain().addRelationDomain(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                                   domaintype="parallel")[0]
        credential = CommonDocDomain().addRelationDomain(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                                         httphost=metadata_host["child.eisoo.com"].split("//")[-1],
                                                         domaintype="parallel")

        client = Http_client()
        client.put(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain/" + uuid,
                   header={"Content-Type": "application/json"},
                   json={"type": "parallel", "port": 443, "credential_id": credential[1],
                         "credential_key": credential[2]})
        print(client.jsonResponse)
        assert client.status_code == 409
        assert client.jsonResponse["code"] == 409014206
        assert client.jsonResponse["message"] == 'Credential type is not available'
        assert client.jsonResponse["cause"] == 'Credential type is not available'
        assert client.jsonResponse["detail"] == [credential[1], credential[2]]

    def test_update_credential_id(self, metadata_host, clear_data):
        """
        更新凭据成功，子域不存在更新凭据成功，只有平级域更新成功
        :return:
        """
        CommonDocDomain().clearRelationDomain(host=metadata_host["self.eisoo.com"].split("//")[-1])
        uuid = CommonDocDomain().addRelationDomain(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                                   domaintype="parallel")[0]
        credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(
            host=metadata_host["parallel.eisoo.com"].split("//")[-1],
            credential_type="parallel")
        client = Http_client()
        client.put(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain/" + uuid,
                   header={"Content-Type": "application/json"},
                   json={"type": "parallel", "port": 443, "credential_id": credential_id,
                         "credential_key": credential_key})

        assert client.status_code == 200
        res = CommonDocDomain().getRelationDomain(uuid=uuid, host=metadata_host["self.eisoo.com"].split("//")[-1])
        print(res)
        assert res["id"] == uuid
        assert res["host"] == metadata_host["parallel.eisoo.com"].split("//")[-1]
        assert res["type"] == "parallel"
        assert res["network_type"] == "direct"
        assert res["port"] == 443
        assert res["credential_id"] == credential_id
        assert res["credential_key"] == credential_key

    @pytest.fixture(scope="function")
    def del_parallel(self, metadata_host):
        yield
        CommonDocDomain().clearRelationDomain(host=metadata_host["self.eisoo.com"].split("//")[-1])

    @pytest.mark.parametrize("domaintype", argvalues=["child", "parallel"])
    def test_repeat_self_used_credential_id(self, metadata_host, domaintype, del_parallel):
        """
        使用自己已使用的凭据，包含子域&&平级域
        :return:
        """
        CommonDocDomain().clearRelationDomain(host=metadata_host["self.eisoo.com"].split("//")[-1])
        domain_data = CommonDocDomain().addRelationDomain(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                                          domaintype=domaintype)
        uuid = domain_data[0]

        client = Http_client()
        client.put(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain/" + uuid,
                   header={"Content-Type": "application/json"},
                   json={"type": domaintype, "port": 443, "credential_id": domain_data[1],
                         "credential_key": domain_data[2]})
        assert client.status_code == 200

        res = CommonDocDomain().getRelationDomain(uuid=uuid, host=metadata_host["self.eisoo.com"].split("//")[-1])
        print(res)
        assert res["id"] == uuid
        assert res["host"] == metadata_host["parallel.eisoo.com"].split("//")[-1]
        assert res["type"] == domaintype
        assert res["network_type"] == "direct"
        assert res["port"] == 443
        assert res["credential_id"] == domain_data[1]
        assert res["credential_key"] == domain_data[2]

    @pytest.mark.parametrize("domaintype,credential_type", argvalues=[("child", "parallel"),("parallel", "child")])
    def test_edit_Inconsistent_credentials(self, metadata_host, domaintype, credential_type, clear_data):
        """
        编辑类型不一致的凭据，状态为未使用的
        :return:
        """
        CommonDocDomain().clearRelationDomain(host=metadata_host["self.eisoo.com"].split("//")[-1])
        CommonDocDomain.del_invalid_credential(host=metadata_host["parallel.eisoo.com"].split("//")[-1])
        uuid = CommonDocDomain().addRelationDomain(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                                   domaintype=domaintype)[0]

        credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(
            host=metadata_host["parallel.eisoo.com"].split("//")[-1],
            credential_type=credential_type)
        client = Http_client()
        client.put(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain/" + uuid,
                   header={"Content-Type": "application/json"},
                   json={"type": domaintype, "port": 443, "credential_id": credential_id,
                         "credential_key": credential_key})
        print(client.jsonResponse)
        assert client.status_code == 409
        assert client.jsonResponse["code"] == 409014205
        assert client.jsonResponse["message"] == 'Credential type is not match'
        assert client.jsonResponse["cause"] == 'Credential type is not match'
        assert client.jsonResponse["detail"] == [credential_id, credential_key]
