# coding=utf-8
import pytest
import allure
from Common.readjson import JsonRead
from .CommonDocDomain import CommonDocDomain
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect
from Common.get_token import Token
from functools import lru_cache
from ..AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt


@lru_cache()
def get_token(host="10.2.176.245"):
    access_token = Token(host=host).get_token()["access_token"]
    return access_token


@pytest.mark.ASP_317
@allure.feature("添加文档域")
class Test_PostMgntV1Domain(object):
    """
         Test_suite添加文档域
     """

    @allure.testcase("5264, 添加文档域--本域类型为子域类型，添加成功，返回201")
    @pytest.mark.high
    def test_PostDocDomainChildAddParallel(self):
        """
        # 添加文档域--本域类型为子域即先添加子域,添加平级域

        :return: None
        """
        host = "10.2.176.208"
        token = get_token(host)

        CommonDocDomain().clearRelationDomain(host="10.2.176.208")  # 清除子域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")  # 添加子域

        client = Http_client(tagname="HTTPGWP")
        client.post(url="https://" + host + "/api/document-domain-management/v1/domain/",
                    header={"Content-Type": "application/json", "Authorization": "Bearer " + token},
                    jsondata={"host": "10.2.176.176", "port": 443, "type": "parallel", "network_type": "indirect"})
        print(client.respheaders)
        assert client.status_code == 201
        assert "/api/document-domain-management/v1/domain/" in client.respheaders['Location']
        assert client.elapsed <= 20.0

    @allure.testcase("5259-1, 添加文档域-- 本域类型非子域类型，添加成功，返回201")
    @pytest.mark.high
    def test_PostDocDomainParallelAddChild(self):
        """
         # 本域类型A为平级域，添加子域B;
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host=["10.2.176.208", "10.2.176.245"])  # 清空域
        res = CommonDocDomain().getSelfDomain(host="10.2.176.245")
        assert res["type"] == "parallel"
        uuid = CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")[0]  # 添加一个子域
        parent = CommonDocDomain().getSelfDomain(host="10.2.176.245")  # 查询本域详情
        child = CommonDocDomain().getRelationDomain(uuid=uuid, host="10.2.176.245")  # 查询关系域详情

        assert parent["type"] == "parent"
        assert child["type"] == "child"
        assert child["port"] == 443
        assert child["host"] == "10.2.176.208"

    @allure.testcase("5259-2, 添加文档域-- 本域类型非子域类型，添加成功，返回201")
    @pytest.mark.high
    def test_PostDocDomainParentAddChild(self):
        """
          # A为父域已添加子域B,再添加子域C;
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.208")  # 清除子域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.176")  # 清除子域2的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")  # 添加一个子域
        res = CommonDocDomain().getSelfDomain(host="10.2.176.245")
        assert res["type"] == "parent"
        uuid = CommonDocDomain().addRelationDomain(host="10.2.176.176", domaintype="child")[0]  # 再次添加一个子域2
        parent = CommonDocDomain().getSelfDomain(host="10.2.176.245")  # 查询本域详情
        child = CommonDocDomain().getRelationDomain(uuid=uuid, host="10.2.176.245")  # 查询关系域详情

        assert parent["type"] == "parent"
        assert child["type"] == "child"
        assert child["port"] == 443
        assert child["host"] == "10.2.176.176"

    @allure.testcase("5259-3, 添加文档域-- 本域类型非子域类型，添加成功，返回201")
    @pytest.mark.high
    def test_PostDocDomainParallelAddParallel(self):
        """
        # 本域类型平级域，添加平级域C;
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.176")  # 清空平级域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空本域的关系域
        res = CommonDocDomain().getSelfDomain(host="10.2.176.245")
        assert res["type"] == "parallel"
        uuid = CommonDocDomain().addRelationDomain(host="10.2.176.176", domaintype="parallel")[0]  # 添加一个平级域
        slf = CommonDocDomain().getSelfDomain(host="10.2.176.245")  # 查询本域详情
        parallel = CommonDocDomain().getRelationDomain(uuid=uuid, host="10.2.176.245")  # 查询关系域详情
        assert slf["type"] == "parallel"
        assert parallel["type"] == "parallel"
        assert parallel["port"] == 443
        assert parallel["host"] == "10.2.176.176"

    @allure.testcase("5259-4, 添加文档域-- 本域类型非子域类型，添加成功，返回201")
    @pytest.mark.high
    def test_PostDocDomainParentAddParallel(self):
        """
        # A父域,已添加子域B,再添加平级域C;
        :return:None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.208")  # 清除子域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.180.162")  # 清空平级域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        childUuid = CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")[0]  # 添加一个子域
        assert CommonDocDomain().getRelationDomain(host="10.2.176.245", uuid=childUuid)["type"] == "child"
        parallelUuid = CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="parallel")[0]  # 再添加一个平级域
        parent = CommonDocDomain().getSelfDomain(host="10.2.176.245")  # 查询本域详情
        parallel = CommonDocDomain().getRelationDomain(uuid=parallelUuid, host="10.2.176.245")  # 查询关系域详情
        assert parent["type"] == "parent"
        assert parallel["type"] == "parallel"
        assert parallel["port"] == 443
        assert parallel["host"] == "10.2.180.162"

    @allure.testcase("5245 添加文档域--校验字段不填，返回201")
    @allure.testcase("5247,添加文档域--校验字段值为空，返回201 ")
    @allure.testcase("5246, 添加文档域--校验字段值为空，返回400")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/PostMgntV1DomainEmpty.json").dict_value_join())
    def test_PostDocDomainAddParallelCheckEmpty(self, url, header, jsondata, checkpoint):
        """
        # 校验字段值可以为check为空,返回400;

        :param url:请求地址
        :param header:请求头
        :param jsondata:请求body参数
        :param checkpoint:断言，检查点
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.180.162")  # 清空平级域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        # token = get_token()
        client = Http_client(tagname="HTTPGWP")
        client.post(url=url, header={"Content-Type": "application/json"},
                    jsondata=jsondata)
        # print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if checkpoint["status_code"] == 201:
            assert "/api/document-domain-management/v1/domain/" in client.respheaders['Location']
        assert client.elapsed <= 20.0

    @allure.testcase("5249,添加文档域--校验字段值为null，返回201")
    @allure.testcase("5248,添加文档域--校验字段值为null，返回400 ")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/PostMgntV1DomainNull.json").dict_value_join())
    def test_PostDocDomainAddParallelCheckNull(self, url, header, jsondata, checkpoint):
        """
        # 校验字段值可以为null和空,返回201;
        :param url:请求地址
        :param header:请求头
        :param jsondata:请求body参数
        :param checkpoint:断言，检查点
        :return:None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.208")  # 清空平级域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        # header = eval(header)
        # token = get_token()
        # header["Authorization"] = "Bearer " + token
        client = Http_client(tagname="HTTPGWP")
        client.post(url=url, header=header, jsondata=jsondata)
        assert client.status_code == checkpoint["status_code"]
        assert client.elapsed <= 20.0

    @pytest.mark.high
    def test_PostDocDomainParentAddTwoParallel(self):
        """
        父域添加多个平级域
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.208")  # 清空子域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.180.162")  # 清空平级域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.176")  # 清空平级域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")  # 添加一个子域
        CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="parallel")  # 再次添加一个添加平级域
        CommonDocDomain().addRelationDomain(host="10.2.176.176", domaintype="parallel")  # 再次添加一个添加平级域
        res = CommonDocDomain().getRelationDomainList()
        assert res["count"] == 3
        assert len(res["data"]) == 3
        for index in range(len(res["data"])):
            if res["data"][index]["host"] == "10.2.176.208":
                assert res["data"][index]["type"] == "child"
            elif res["data"][index]["host"] == "10.2.180.162":
                assert res["data"][index]["type"] == "parallel"
            elif res["data"][index]["host"] == "10.2.176.176":
                assert res["data"][index]["type"] == "parallel"
            else:
                assert 1 == 2

    @pytest.mark.high
    def test_PostDocDomainParallelAddTwoParallel(self):
        """
        平级域添加多个平级域
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.208")  # 清空平级域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.180.162")  # 清空平级域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="parallel")  # 添加一个平级域
        CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="parallel")  # 再次添加一个添加平级域
        res = CommonDocDomain().getRelationDomainList()
        assert res["count"] == 2
        for index in range(len(res["data"])):
            if res["data"][index]["host"] == "10.2.176.208":
                assert res["data"][index]["type"] == "parallel"
            elif res["data"][index]["host"] == "10.2.180.162":
                assert res["data"][index]["type"] == "parallel"
            else:
                assert 1 == 2

    @pytest.mark.high
    def test_PostDocDomainChildAddTwoParallel(self):
        """
        子域添加多个平级域
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.208")  # 清空子域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.180.162")  # 清空平级域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.176")  # 清空平级域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")  # 添加一个子域

        CommonDocDomain().addRelationDomain(httphost="10.2.176.208", host="10.2.180.162",
                                            domaintype="parallel")  # 子域添加一个添加平级域
        CommonDocDomain().addRelationDomain(httphost="10.2.176.208", host="10.2.176.176",
                                            domaintype="parallel")  # 子域再次添加一个添加平级域
        res = CommonDocDomain().getRelationDomainList(host="10.2.176.208")  # 查询子域的关系域列表
        assert res["count"] == 2
        for index in range(len(res["data"])):
            if res["data"][index]["host"] == "10.2.180.162":
                assert res["data"][index]["type"] == "parallel"
            elif res["data"][index]["host"] == "10.2.176.176":
                assert res["data"][index]["type"] == "parallel"
            else:
                assert 1 == 2

    @allure.step("初始化清除关系域并添加一条关系域")
    @pytest.fixture(scope='function',
                    params=[("child", "child"), ("parallel", "parallel"), ("child", "parallel"), ("parallel", "child")])
    def setupClearDomain(self, request, fatherdomain="10.2.176.245", domain="10.2.180.162"):
        CommonDocDomain().clearRelationDomain(host=domain)  # 清空关系域
        CommonDocDomain().clearRelationDomain(host=fatherdomain)  # 清空父域的关系域
        CommonDocDomain().addRelationDomain(host=domain, httphost=fatherdomain, domaintype=request.param[0])
        return request.param[1], fatherdomain, domain

    @allure.testcase("5255,添加文档域-- 重复添加，返回409")
    def test_addDomainRepeat409(self, setupClearDomain):
        """
        :return:
        """
        # print(setupClearDomain)
        # token = get_token(setupClearDomain[1])
        client = Http_client(tagname="HTTPGWP")
        client.post(url="https://" + setupClearDomain[1] + ":443/api/document-domain-management/v1/domain/",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": setupClearDomain[2], "port": 80, "type": setupClearDomain[0],
                              "credential_id": "admin",
                              "credential_key": "eisoo", "network_type": "direct"})
        assert client.status_code == 409
        assert client.jsonResponse["cause"] == "host already exist"  # 断言关系域已存在

    @allure.step("初始化设置本域为子域")
    @pytest.fixture(scope="function", params=["child"])
    def setupSetSelfDomainChild(self, request, fatherdomain="10.2.176.245", domain="10.2.180.162",
                                otherdomain="10.2.180.180"):
        CommonDocDomain().clearRelationDomain(host=domain)  # 清空关系域
        CommonDocDomain().clearRelationDomain(host=fatherdomain)  # 清空父域的关系域
        CommonDocDomain().addRelationDomain(host=domain, httphost=fatherdomain, domaintype=request.param)
        return otherdomain, domain, request.param

    @allure.testcase("5263,添加文档域--本域类型为子域类型，添加失败，返回409")
    def test_ChildDomainAddChildDomain(self, setupSetSelfDomainChild):
        """
        :return:
        """
        token = get_token(setupSetSelfDomainChild[1])
        client = Http_client(tagname="HTTPGWP")
        client.post(url="https://" + setupSetSelfDomainChild[1] + ":443/api/document-domain-management/v1/domain/",
                    header={"Content-Type": "application/json", "Authorization": "Bearer " + token},
                    jsondata={"host": setupSetSelfDomainChild[0], "port": 443, "type": setupSetSelfDomainChild[2],
                              "credential_id": "admin", "credential_key": "eisoo"})
        assert client.status_code == 409
        assert client.jsonResponse["code"] == 409014204
        assert client.jsonResponse[
                   "cause"] == "Add failed, the current domain has been added as a subdomain by 10.2.176.245"

    @allure.step("初始化本域")
    @pytest.fixture(scope="function", params=["child", "parallel"])
    def setupSelfDoamin(self, request, selfdomain="10.2.176.245"):
        """

        :return:
        """
        CommonDocDomain().clearRelationDomain(host=selfdomain)  # 清空本域域的关系域
        return selfdomain, request.param

    @allure.testcase("5698,添加文档域-- 本域添加本域为关系域，返回409")
    def test_selfDomainAddSelfDomain(self, setupSelfDoamin):
        """

        :return:
        """
        # token = get_token(setupSelfDoamin[0])
        client = Http_client(tagname="HTTPGWP")
        client.post(url="https://" + setupSelfDoamin[0] + ":443/api/document-domain-management/v1/domain/",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": setupSelfDoamin[0], "port": 443, "type": setupSelfDoamin[1],
                              "credential_id": "admin", "credential_key": "eisoo"})
        assert client.status_code == 409
        assert client.jsonResponse["code"] == 409014201
        assert client.jsonResponse["message"] == "Domains cannot be added domainself"

    @allure.testcase("5244, 添加文档域--校验字段非必填，返回400")
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/PostMgntV1Domain400.json").dict_value_join())
    def test_addDocDomainReturn400(self, url, header, jsondata, checkpoint):
        """
        test:添加文档域--校验字段非必填，返回400
        :return:
        """
        # header=eval(header)
        # token = get_token()
        # header["Authorization"] = "Bearer " + token
        client = Http_client(tagname="HTTPGWP")
        client.post(url=url, header=header, jsondata=jsondata)
        assert client.status_code == checkpoint["status_code"]
        assert client.jsonResponse["cause"] == checkpoint["cause"]
        print(client.jsonResponse)

    @allure.testcase("5250, 添加文档域-- 校验参数类型错误，返回400")
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/PostMgntV1DomainTypeError.json").dict_value_join())
    def test_addDocDomainTypeError(self, url, header, jsondata, checkpoint):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :return:
        """
        # header=eval(header)
        # token = get_token()
        # header["Authorization"] = "Bearer " + token
        CommonDocDomain().clearRelationDomain(host=["10.2.176.245"])  # 清空父域的关系域
        client = Http_client(tagname="HTTPGWP")
        client.post(url=url, header=header, jsondata=jsondata)
        assert client.status_code == checkpoint["status_code"]
        if "cause" in checkpoint:
            assert client.jsonResponse["cause"] == checkpoint["cause"]
        if "code" in checkpoint:
            assert client.jsonResponse["code"] == checkpoint["code"]
        print(client.jsonResponse)

    @allure.testcase("5251, 添加文档域-- 枚举type类型不存在，返回400")
    @allure.testcase("5252,添加文档域-- 端口合法验证，返回400 ")
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/PostMgntV1DomainTypeParent.json").dict_value_join())
    def test_addDocDomainTypePort400(self, url, header, jsondata, checkpoint):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :return:
        """
        # header=eval(header)
        # token = get_token()
        # header["Authorization"] = "Bearer " + token
        client = Http_client(tagname="HTTPGWP")
        client.post(url=url, header=header, jsondata=jsondata)
        assert client.status_code == checkpoint["status_code"]
        assert client.jsonResponse["cause"] == checkpoint["cause"]
        print(client.jsonResponse)

    @allure.testcase("5254,添添加文档域-- IP非法验证，返回400 ")
    @allure.testcase("5253,添加文档域-- 域名非法，返回400 ")
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/PostMgntV1DomainIllegalDomain.json").dict_value_join())
    def test_addIllegalHostDomain(self, url, header, jsondata, checkpoint):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :return:
        """
        # header=eval(header)
        # token = get_token()
        # header["Authorization"] = "Bearer " + token
        client = Http_client(tagname="HTTPGWP")
        client.post(url=url, header=header, jsondata=jsondata)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        assert client.jsonResponse["cause"] == checkpoint["cause"]
        if "code" in checkpoint:
            assert client.jsonResponse["code"] == checkpoint["code"]
        if "message" in checkpoint:
            assert client.jsonResponse["message"] == checkpoint["message"]

    @allure.testcase("5959, 添加文档域-- 该文档域已是父域,不允许添加为子域409014202 ")
    def test_adddomain409014202(self):
        """
        409014202:该文档域域已是父域，不允许添加为子域
        :return:
        """
        CommonDocDomain().clearRelationDomain(host=["10.2.180.162", "10.2.176.176", "10.2.176.245"])  # 清空平级域的关系域
        CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="child")  # 添加一个子域
        CommonDocDomain.del_invalid_credential(host="10.2.176.245", domain_type="child")
        credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(host="10.2.176.245",
                                                                                  credential_type="child")
        token = get_token(host="10.2.176.176")
        client = Http_client(tagname="HTTP")
        client.post(url="/api/document-domain-management/v1/domain/",
                    header={"Content-Type": "application/json", "Authorization": "Bearer " + token},
                    jsondata={"host": "10.2.176.245", "port": 443, "type": "child", "credential_id": credential_id,
                              "credential_key": credential_key})
        print(client.jsonResponse)
        assert client.status_code == 409
        assert client.jsonResponse["code"] == 409014202
        assert client.jsonResponse["message"] == "The domain cannot added as subdomains"

    @allure.testcase("5960,  添加文档域-- 该文档域已被'XXX域名'添加为子域 409014203  ")
    def test_adddomain409014203(self):
        """
        409014203:该文档域已被'XXX域名'添加为子域
        :return:
        """
        CommonDocDomain().clearRelationDomain(host=["10.2.180.162", "10.2.176.176", "10.2.176.245"])  # 清空域
        CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="child")  # 添加一个子域
        token = get_token(host="10.2.176.176")
        credential = CommonDocDomain.get_credential(host="10.2.180.162", domain_type="child")
        # print(credential)
        client = Http_client(tagname="HTTP")
        client.post(url="/api/document-domain-management/v1/domain/",
                    header={"Content-Type": "application/json", "Authorization": "Bearer " + token},
                    jsondata={"host": "10.2.180.162", "port": 443, "type": "child", "credential_id": credential[0],
                              "credential_key": credential[1]})
        print(client.jsonResponse)
        assert client.status_code == 409
        assert client.jsonResponse["code"] == 409014203
        assert client.jsonResponse["message"] == "The domain has be added"
        assert client.jsonResponse["cause"] == "The domain has be added by ['10.2.176.245']"

    @allure.testcase("5961,  添加文档域-- 添加本域父域为平级域成功")
    def test_addMyFatherDomain(self):
        """
        子域可以添加父域为平级域，平级域不限制，不再抛出409014204
        :return:
        """
        CommonDocDomain().clearRelationDomain(host=["10.2.180.162", "10.2.176.245"])  # 清空平级域的关系域
        CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="child")  # 添加一个子域
        token = get_token("10.2.180.162")
        credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(host="10.2.176.245",
                                                                                  credential_type="parallel")
        client = Http_client(tagname="HTTP_child2")
        client.post(url="/api/document-domain-management/v1/domain/",
                    header={"Content-Type": "application/json", "Authorization": "Bearer " + token},
                    jsondata={"host": "10.2.176.245", "port": 443, "type": "parallel", "credential_id": credential_id,
                              "credential_key": credential_key, "network_type": "direct"})
        print(client.jsonResponse)
        CommonDocDomain.del_invalid_credential(host="10.2.176.245", domain_type="parallel")
        assert client.status_code == 201
        # assert client.jsonResponse["code"] == 409014204
        # assert client.jsonResponse["message"] == "Domains cannot be added who is parent domain"

    @allure.step("释放脏数据")
    @pytest.fixture(scope="function")
    def teardownDoaminData(self):
        """

        :return:
        """
        CommonDocDomain().clearRelationDomain(
            host=["10.2.180.162", "10.2.176.245", "10.2.176.176", "10.2.176.208"])  # 清空关系域
        CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="child")  # 添加一个子域
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child", httphost="10.2.176.176")
        yield
        CommonDocDomain().clearRelationDomain(
            host=["10.2.180.162", "10.2.176.245", "10.2.176.176", "10.2.176.208"])  # 清空关系域
        CommonDocDomain.del_invalid_credential(host="10.2.176.245", domain_type="parallel")

    def test_addfatherdomainToparallel(self, teardownDoaminData):
        """
        # BUG ASP-5414:添加文档域接口，子域添加父域成为平级域成功，期望添加失败
        解决方案，子域可以添加平级域；以上问题不存在
        :return:
        """
        token = get_token("10.2.176.208")
        credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(host="10.2.176.245",
                                                                                  credential_type="parallel")
        client = Http_client(tagname="HTTP_child1")
        client.post(url="/api/document-domain-management/v1/domain/",
                    header={"Content-Type": "application/json", "Authorization": "Bearer " + token},
                    jsondata={"host": "10.2.176.245", "port": 443, "type": "parallel", "credential_id": credential_id,
                              "credential_key": credential_key, "network_type": "direct"})
        print(client.jsonResponse)
        assert client.status_code == 201

    def test_verifyPortHostValid(self):
        """
        ASP-5111:添加文档域接口，添加平级域时未验证域名host和port是否可用
        :return:
        """
        # token = get_token()
        client = Http_client(tagname="HTTPGWP")
        credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(host="10.2.180.162",
                                                                                  credential_type="parallel")
        client.post(url="/api/document-domain-management/v1/domain/",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "10.2.180.162", "port": 8081, "type": "parallel", "credential_id": credential_id,
                              "credential_key": credential_key, "network_type": "direct"})
        assert client.jsonResponse["code"] == 400014205
        assert client.jsonResponse["message"] == "Linked failed"
        assert client.jsonResponse["cause"] == "Connection refused"
        assert client.jsonResponse["detail"] == ['10.2.180.162']
        CommonDocDomain.del_invalid_credential(host="10.2.180.162", domain_type="parallel")
        client.post(url="/api/document-domain-management/v1/domain/",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "11.2.180.162", "port": 443, "type": "parallel", "credential_id": credential_id,
                              "credential_key": credential_key, "network_type": "direct"})
        assert client.jsonResponse["code"] == 400014205
        assert client.jsonResponse["message"] == "Linked failed"
        assert client.jsonResponse["cause"] == "Connection timed out"
        assert client.jsonResponse["detail"] == ['11.2.180.162']

    def test_NetGapNotVerifyPortHostValid(self):
        """
        网闸模式不验证host和port的联通性
        :return:
        """
        # token = get_token()
        client = Http_client(tagname="HTTPGWP")
        client.post(url="/api/document-domain-management/v1/domain/",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "10.2.180.162", "port": 8888, "type": "parallel", "network_type": "indirect"})
        print(client.jsonResponse)
        assert client.status_code == 201
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")

    @allure.step("初始化数据和清除数据")
    @pytest.fixture(scope="function")
    def setupAndteardown(self):
        CommonDocDomain().addRelationDomain(host="10.2.180.162")
        yield
        CommonDocDomain().clearRelationDomain(host=["10.2.176.245", "10.2.180.162"])

    def test_ChildDomainaddChildDomain409014204(self, setupAndteardown):
        """
        子域添加子域报错409014204
        message: "Add failed, the current domain has been added as a subdomain"
        cause: "Add failed, the current domain has been added as a subdomain by 10.2.176.245"
        :return:
        """
        token = get_token("10.2.180.162")
        client = Http_client(tagname="HTTP_child2")
        client.post(url="/api/document-domain-management/v1/domain/",
                    header={"Content-Type": "application/json", "Authorization": "Bearer " + token},
                    jsondata={"host": "10.2.176.208", "port": 443, "type": "child", "credential_id": "add",
                              "credential_key": "sinn"})
        assert client.status_code == 409
        assert client.jsonResponse["code"] == 409014204
        assert client.jsonResponse["message"] == "Add failed, the current domain has been added as a subdomain"
        assert client.jsonResponse[
                   "cause"] == "Add failed, the current domain has been added as a subdomain by 10.2.176.245"

    @pytest.fixture(scope="function")
    def clear_data(self):
        yield
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")

    def test_domain_child_direct(self, clear_data):
        """
        添加子域直链模式
        :return:
        """
        # token = get_token()
        client = Http_client(tagname="HTTPGWP")
        CommonDocDomain.del_invalid_credential(host="10.2.180.162", domain_type="child")
        credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(host="10.2.180.162",
                                                                                  credential_type="child")
        client.post(url="/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "10.2.180.162", "port": 443, "type": "child", "credential_id": credential_id,
                              "credential_key": credential_key,
                              "network_type": "direct"})
        assert client.status_code == 201
        db = DB_connect(dbname="db_domain_self")
        result = db.select_one("SELECT * from domain_mgnt.t_relationship_domain where "
                               "f_host='10.2.180.162';")
        assert result[1] == "10.2.180.162"
        assert result[2] == 443
        assert result[5] == "child"
        assert result[6] == "direct"
        assert result[7] == credential_id
        assert result[8] == credential_key

    def test_domain_child_indirect(self, clear_data):
        """
        添加子域非直链模式
        :param clear_data:
        :return:
        """
        # token = get_token()
        client = Http_client(tagname="HTTPGWP")
        CommonDocDomain.del_invalid_credential(host="10.2.180.162", domain_type="child")
        credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(host="10.2.180.162",
                                                                                  credential_type="child")
        client.post(url="/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "10.2.180.162", "port": 443, "type": "child", "credential_id": credential_id,
                              "credential_key": credential_key,
                              "network_type": "indirect"})
        assert client.status_code == 201
        db = DB_connect(dbname="db_domain_self")
        result = db.select_one("SELECT * from domain_mgnt.t_relationship_domain where "
                               "f_host='10.2.180.162';")
        assert result[1] == "10.2.180.162"
        assert result[2] == 443
        assert result[5] == "child"
        assert result[6] == "direct"
        assert result[7] == credential_id
        assert result[8] == credential_key

    def test_domain_parallel_direct(self, clear_data):
        """
        添加平级域直链模式
        :return:
        """
        # token = get_token()
        client = Http_client(tagname="HTTPGWP")
        CommonDocDomain.del_invalid_credential(host="10.2.180.162", domain_type="parallel")
        credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(host="10.2.180.162",
                                                                                  credential_type="parallel")
        client.post(url="/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "10.2.180.162", "port": 443, "type": "parallel", "credential_id": credential_id,
                              "credential_key": credential_key,
                              "network_type": "direct"})
        assert client.status_code == 201
        db = DB_connect(dbname="db_domain_self")
        result = db.select_one("SELECT * from domain_mgnt.t_relationship_domain where "
                               "f_host='10.2.180.162';")
        print(result)
        assert result[1] == "10.2.180.162"
        assert result[2] == 443
        assert result[5] == "parallel"
        assert result[6] == "direct"
        assert result[7] == credential_id
        assert result[8] == credential_key

    def test_domain_parallel_indirect(self, clear_data):
        """
        添加平级域非直链模式  BUG ASP-6135 indirect 模式下应不存appid,appkey,sercet
        :param clear_data:
        :return:
        """
        # token = get_token()
        client = Http_client(tagname="HTTPGWP")
        CommonDocDomain.del_invalid_credential(host="10.2.180.162", domain_type="parallel")
        credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(host="10.2.180.162",
                                                                                  credential_type="parallel")
        client.post(url="/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "10.2.180.162", "port": 443, "type": "parallel", "credential_id": credential_id,
                              "credential_key": credential_key, "secret": "sercret",
                              "network_type": "indirect"})
        assert client.status_code == 201
        db = DB_connect(dbname="db_domain_self")
        result = db.select_one("SELECT * from domain_mgnt.t_relationship_domain where "
                               "f_host='10.2.180.162';")
        print(result)
        assert result[1] == "10.2.180.162"
        assert result[2] == 443
        assert result[5] == "parallel"
        assert result[6] == "indirect"
        assert result[3] == "sercret"
        assert result[7] == ""
        assert result[8] == ""

    def test_required_network_type(self):
        """
        校验network_type必填network_type
        :return:
        """
        # token = get_token()
        client = Http_client(tagname="HTTPGWP")
        client.post(url="/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "10.2.180.162", "port": 443, "type": "parallel", "credential_id": "appid",
                              "credential_key": "appkey", "secret": "sercret"})
        assert client.jsonResponse["code"] == 400000000
        assert client.jsonResponse["cause"] == "'network_type' is a required property"

    def test_network_type_enum_error(self):
        """
        network_type枚举错误
        :return:
        """
        # token = get_token()
        client = Http_client(tagname="HTTPGWP")
        client.post(url="/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "10.2.180.162", "port": 443, "type": "parallel", "credential_id": "appid",
                              "credential_key": "appkey", "secret": "sercret", "network_type": "undirect"})
        assert client.jsonResponse["code"] == 400000000
        assert client.jsonResponse["cause"] == "'undirect' is not one of ['direct', 'indirect']"

    def test_verified_required_credential_id(self, metadata_host):
        """
        校验direct模式下，credential_id和credential_key 必填
        :return:
        """
        client = Http_client()
        client.post(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "10.2.180.162", "port": 443, "type": "child", "secret": "sercret",
                              "network_type": "direct"})
        assert client.status_code == 400
        assert client.jsonResponse["code"] == 400000000
        assert client.jsonResponse["message"] == "Invalid request."
        assert client.jsonResponse["cause"] == "'credential_id' is a required property"
        assert client.jsonResponse["detail"] == {'invalid_params': [
            {'host': '10.2.180.162', 'port': 443, 'type': 'child', 'secret': 'sercret', 'network_type': 'direct'}]}

        client.post(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "10.2.180.162", "port": 443, "type": "child", "credential_id": "credential_id",
                              "secret": "sercret", "network_type": "direct"})
        print(client.status_code)
        print(client.jsonResponse)
        assert client.status_code == 400
        assert client.jsonResponse["code"] == 400000000
        assert client.jsonResponse["message"] == "Invalid request."
        assert client.jsonResponse["cause"] == "'credential_key' is a required property"
        assert client.jsonResponse["detail"] == {'invalid_params':
                                                     [{'host': '10.2.180.162', 'port': 443, 'type': 'child',
                                                       'credential_id': 'credential_id',
                                                       'secret': 'sercret', 'network_type': 'direct'}]}

        client.post(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "10.2.180.162", "port": 443, "type": "parallel",
                              "secret": "sercret", "network_type": "direct"})
        print(client.status_code)
        print(client.jsonResponse)
        assert client.status_code == 400
        assert client.jsonResponse["code"] == 400000000
        assert client.jsonResponse["message"] == "Invalid request."
        assert client.jsonResponse["cause"] == "'credential_id' is a required property"
        assert client.jsonResponse["detail"] == {
            'invalid_params': [{'host': '10.2.180.162', 'port': 443, 'type': 'parallel', 'network_type': 'direct'}]}

        client.post(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "10.2.180.162", "port": 443, "type": "parallel", "credential_id": "credential_id",
                              "secret": "sercret", "network_type": "direct"})
        print(client.status_code)
        print(client.jsonResponse)
        assert client.status_code == 400
        assert client.jsonResponse["code"] == 400000000
        assert client.jsonResponse["message"] == "Invalid request."
        assert client.jsonResponse["cause"] == "'credential_key' is a required property"
        assert client.jsonResponse["detail"] == {'invalid_params': [{'host': '10.2.180.162', 'port': 443,
                                                                     'type': 'parallel',
                                                                     'credential_id': 'credential_id',
                                                                     'network_type': 'direct'}]}

    def test_not_exist_credential_id(self, metadata_host):
        """
        添加不存在的凭据
        :return:
        """
        client = Http_client()
        client.post(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "10.2.180.162", "port": 443, "type": "child", "secret": "sercret",
                              "credential_id": "f1605b13-6e3a-4b39-ae36-eb39f15c161b4",
                              "credential_key": "A8wIBuQSm9Rd",
                              "network_type": "direct"})
        print(client.jsonResponse)
        assert client.status_code == 401
        assert client.jsonResponse["code"] == 401014201
        assert client.jsonResponse["message"] == "Invalid client"
        assert client.jsonResponse["cause"] == "invalid_client"

        client.post(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "10.2.180.162", "port": 443, "type": "parallel", "secret": "sercret",
                              "credential_id": "f1605b13-6e3a-4b39-ae36-eb39f15c161b4",
                              "credential_key": "A8wIBuQSm9Rd",
                              "network_type": "direct"})
        print(client.jsonResponse)
        assert client.status_code == 401
        assert client.jsonResponse["code"] == 401014201
        assert client.jsonResponse["message"] == "Invalid client"
        assert client.jsonResponse["cause"] == "invalid_client"

    def test_is_del_credential_id(self, metadata_host):
        """
        使用已被删除的credential_id
        :param metadata_host:
        :return:
        """
        CommonDocDomain.del_invalid_credential(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                               domain_type="child")
        client = Http_client()
        credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(host="10.2.180.162",
                                                                                  credential_type="child")
        CommonAuthCredentialMgnt().del_credential(host="10.2.180.162", credential_id=credential_id)
        client.post(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "10.2.180.162", "port": 443, "type": "child", "secret": "sercret",
                              "credential_id": credential_id, "credential_key": credential_key,
                              "network_type": "direct"})
        print(client.jsonResponse)
        assert client.status_code == 403
        assert client.jsonResponse["code"] == 403014000
        assert client.jsonResponse["message"] == 'No permission to do this operation.'
        assert client.jsonResponse["cause"] == "client_id does not match"

        credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(host="10.2.180.162",
                                                                                  credential_type="parallel")
        CommonAuthCredentialMgnt().del_credential(host="10.2.180.162", credential_id=credential_id)
        client.post(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": "10.2.180.162", "port": 443, "type": "parallel", "secret": "sercret",
                              "credential_id": credential_id, "credential_key": credential_key,
                              "network_type": "direct"})
        print(client.jsonResponse)
        assert client.status_code == 403
        assert client.jsonResponse["code"] == 403014000
        assert client.jsonResponse["message"] == 'No permission to do this operation.'
        assert client.jsonResponse["cause"] == "client_id does not match"

    @pytest.mark.parametrize("domaintype", argvalues=["child", "parallel"])
    def test_invalid_credential_id(self, metadata_host, domaintype):
        """
        添加无效invalid的credential_id
        :return:
        """
        child_host = metadata_host["parallel.eisoo.com"].split("//")[-1]
        print(child_host)
        client = Http_client()
        credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(host=child_host,
                                                                                  credential_type=domaintype)
        UUID = CommonDocDomain().addRelationDomain(host=child_host, domaintype=domaintype,
                                                   httphost=metadata_host["self.eisoo.com"].split("//")[-1],
                                                   credential_id=credential_id, credential_key=credential_key)[0]
        CommonDocDomain().delRelationDomain(host=metadata_host["self.eisoo.com"].split("//")[-1], uuid=UUID)
        client.post(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": child_host, "port": 443, "type": domaintype, "secret": "sercret",
                              "credential_id": credential_id, "credential_key": credential_key,
                              "network_type": "direct"})

        assert client.status_code == 409
        assert client.jsonResponse["code"] == 409014206
        assert client.jsonResponse["message"] == "Credential type is not available"
        assert client.jsonResponse["cause"] == "Credential type is not available"
        assert client.jsonResponse["detail"] == [credential_id, credential_key]
        CommonAuthCredentialMgnt().del_credential(host=child_host, credential_id=credential_id)

    @pytest.mark.parametrize("domaintype", argvalues=["child", "parallel"])
    def test_me_used_credential_id(self, metadata_host, domaintype):
        """
        使用已使用的凭据
        :param metadata_host:
        :return:
        """
        CommonDocDomain().clearRelationDomain(host=metadata_host["self.eisoo.com"].split("//")[-1])
        domain_data = CommonDocDomain().addRelationDomain(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                                          domaintype=domaintype,
                                                          httphost=metadata_host["self.eisoo.com"].split("//")[-1])
        client = Http_client()
        client.post(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": metadata_host["parallel.eisoo.com"].split("//")[-1], "port": 443,
                              "type": domaintype, "secret": "sercret",
                              "credential_id": domain_data[1], "credential_key": domain_data[2],
                              "network_type": "direct"})

        print(client.jsonResponse)
        assert client.status_code == 409
        assert client.jsonResponse["code"] == 409014000
        assert client.jsonResponse["message"] == 'Conflict resource.'
        assert client.jsonResponse["cause"] == 'host already exist'
        assert client.jsonResponse["detail"] == {
            'conflict_resource': [metadata_host["parallel.eisoo.com"].split("//")[-1]]}

    @pytest.fixture(scope="function")
    def del_data(self, metadata_host):
        yield
        CommonDocDomain().clearRelationDomain(
            host=[metadata_host["self.eisoo.com"].split("//")[-1],
                  metadata_host["child.eisoo.com"].split("//")[-1]])

        CommonDocDomain.del_invalid_credential(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                               domain_type="parallel")

    @pytest.mark.parametrize("domaintype", argvalues=["child", "parallel"])
    def test_he_used_credential_id(self, metadata_host, domaintype, del_data):
        """
        使用已使用的凭据
        :param metadata_host:
        :return:
        """
        CommonDocDomain().clearRelationDomain(host=metadata_host["self.eisoo.com"].split("//")[-1])
        domain_data = CommonDocDomain().addRelationDomain(host=metadata_host["parallel.eisoo.com"].split("//")[-1],
                                                          domaintype=domaintype,
                                                          httphost=metadata_host["child.eisoo.com"].split("//")[-1])
        client = Http_client()
        client.post(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": metadata_host["parallel.eisoo.com"].split("//")[-1], "port": 443,
                              "type": domaintype, "secret": "sercret",
                              "credential_id": domain_data[1], "credential_key": domain_data[2],
                              "network_type": "direct"})
        print(client.jsonResponse)
        if domaintype == "child":
            assert client.status_code == 409
            assert client.jsonResponse["code"] == 409014203
            assert client.jsonResponse["message"] == 'The domain has be added'
            assert client.jsonResponse["cause"] == "The domain has be added by ['10.2.176.208']"
            assert client.jsonResponse["detail"] == ['10.2.176.208']
        elif domaintype == "parallel":
            assert client.status_code == 409
            assert client.jsonResponse["code"] == 409014206
            assert client.jsonResponse["message"] == 'Credential type is not available'
            assert client.jsonResponse["cause"] == "Credential type is not available"
            assert client.jsonResponse["detail"] == [domain_data[1], domain_data[2]]

    @pytest.mark.parametrize("domaintype,credential_type", argvalues=[("child", "parallel"), ("parallel", "child")])
    def test_add_Inconsistent_credentials(self, metadata_host, domaintype, credential_type):
        """
        添加类型不一致的凭据，状态为未使用的
        :return:
        """
        CommonDocDomain().clearRelationDomain(host=metadata_host["self.eisoo.com"].split("//")[-1])
        CommonDocDomain.del_invalid_credential(host=metadata_host["parallel.eisoo.com"].split("//")[-1])
        credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(
            host=metadata_host["parallel.eisoo.com"].split("//")[-1],
            credential_type=credential_type)
        client = Http_client()
        client.post(url=metadata_host["self.eisoo.com"] + "/api/document-domain-management/v1/domain",
                    header={"Content-Type": "application/json"},
                    jsondata={"host": metadata_host["parallel.eisoo.com"].split("//")[-1], "port": 443,
                              "type": domaintype, "secret": "sercret",
                              "credential_id": credential_id, "credential_key": credential_key,
                              "network_type": "direct"})
        print(client.jsonResponse)
        assert client.status_code == 409
        assert client.jsonResponse["code"] == 409014205
        assert client.jsonResponse["message"] == 'Credential type is not match'
        assert client.jsonResponse["cause"] == 'Credential type is not match'
        assert client.jsonResponse["detail"] == [credential_id, credential_key]
