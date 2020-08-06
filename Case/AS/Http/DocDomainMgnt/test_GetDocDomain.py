# coding=utf-8
import pytest
import allure

from Common.readjson import JsonRead
from .CommonDocDomain import CommonDocDomain
from Common.http_request import Http_client


@pytest.mark.ASP_317
@allure.feature("获取本域详情")
class Test_GetMgntV1DomainSelf(object):
    """
     Test_suites获取本域详情
    """

    @allure.testcase("5238,域详情查询-返回404 ")
    @pytest.mark.medium
    @pytest.mark.parametrize("url,header,params,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/GetMgntV1Domain404.json").dict_value_join())
    def test_GetMgntV1Domain404(self, url, header, params, checkpoint):
        """

        :param url:请求url
        :param header:请求的header
        :param params:请求的params参数
        :param checkpoint:断言，检查点
        :return:None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  #
        # header = eval(header)
        # token = get_token()
        # header["Authorization"] = "Bearer " + token
        client = Http_client(tagname="HTTPGWP")
        client.get(url=url, params=params, header=header)
        assert client.jsonResponse['code'] == checkpoint['code']
        assert client.jsonResponse['message'] == checkpoint['message']
        assert client.status_code == checkpoint['status_code']
        print(client.jsonResponse)
        assert client.jsonResponse['detail']['notfound_params'][0] == checkpoint['detail.notfound_resource']
        assert client.elapsed <= 20.0

    @allure.testcase("5242-1,域详情查询-查询本域详情，返回200")
    @pytest.mark.parametrize("url,header,params,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/GetMgntV1DomainSelf200.json").dict_value_join())
    def test_GetMgntV1DomainSelf200(self, url, header, params, checkpoint):
        """

        :param url: 请求url
        :param header:请求的header
        :param params:请求的params参数
        :param checkpoint:断言，检查点
        :return:None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空本域的关系域
        # header = eval(header)
        # token = get_token()
        # header["Authorization"] = "Bearer " + token
        client = Http_client(tagname="HTTPGWP")
        client.get(url=url, params=params, header=header)
        assert client.jsonResponse['type'] == checkpoint['type']
        assert client.jsonResponse['host'] is None
        assert client.status_code == checkpoint['status_code']
        assert client.jsonResponse['id'] is not None
        assert client.elapsed <= 20.0

    @pytest.mark.ASP_317
    @allure.testcase("5242-2,域详情查询-查询本域详情，返回200")
    @allure.testcase("5242-5,域详情查询-查询本域详情，返回200")
    @pytest.mark.parametrize("url,header,params,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/GetMgntV1DomainSelf200.json").dict_value_join(),
                             ids=["1"])
    def test_GetMgntV1DomainSelfParent(self, url, header, params, checkpoint):
        """
        # 添加子域查询本域详情为"type": "parent",
         :param url: 请求url
        :param header:请求的header
        :param params:请求的params参数
        :param checkpoint:断言，检查点
        :return:None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空本域的关系域
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")  # 添加子域

        selfclient = Http_client(tagname="HTTPGWP")
        # header=eval(header)
        # token = get_token()
        # header["Authorization"] = "Bearer " + token
        selfclient.get(url=url, params=params, header=header)
        assert selfclient.jsonResponse['type'] == "parent"
        assert selfclient.jsonResponse['host'] is None
        assert selfclient.status_code == 200
        assert selfclient.jsonResponse['id'] is not None
        assert selfclient.elapsed <= 20.0

        child = CommonDocDomain().getSelfDomain(host="10.2.176.208")  # 查询子域详情
        assert child['type'] == "child"
        assert child['host'] == "10.2.176.245" or child['host'] == "self.eisoo.com"
        assert child['id'] is not None

    @allure.testcase("5242-3,域详情查询-查询本域详情，返回200")
    @pytest.mark.parametrize("url,header,params,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/GetMgntV1DomainSelf200.json").dict_value_join(),
                             ids=["1"])
    def test_GetMgntV1DomainSelfParallelAddParallel(self, url, header, params, checkpoint):
        """
         # 平级域添加平级域
        :param url:
        :param header:
        :param params:
        :param checkpoint:
        :return:
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空本域的关系域
        CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="parallel")  # 添加一个平级域
        # header=eval(header)
        # token = get_token()
        # header["Authorization"] = "Bearer " + token
        client = Http_client(tagname="HTTPGWP")
        client.get(url=url, params=params, header=header)
        print(client.jsonResponse)
        assert client.jsonResponse['type'] == "parallel"
        assert client.jsonResponse['host'] is None or client.jsonResponse['host'] == ""
        assert client.status_code == 200
        assert client.jsonResponse['id'] is not None

    @allure.testcase("5242-4,域详情查询-查询本域详情，返回200")
    @pytest.mark.parametrize("url,header,params,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/GetMgntV1DomainSelf200.json").dict_value_join(),
                             ids=["1"])
    def test_GetMgntV1DomainSelfFatherAddparallel(self, url, header, params, checkpoint):
        """
        # 父域添加平级域
        :param url:
        :param header:
        :param params:
        :param checkpoint:
        :return:
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空本域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.180.162")  # 清空平级域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.208")  # 清空子域的关系域
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")  # 添加一个子域
        CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="parallel")  # 添加一个平级域
        # header=eval(header)
        # token = get_token()
        # header["Authorization"] = "Bearer " + token
        client = Http_client(tagname="HTTPGWP")
        client.get(url=url, params=params, header=header)
        print(client.jsonResponse)
        assert client.jsonResponse['type'] == "parent"
        assert client.jsonResponse['host'] is None
        assert client.status_code == 200
        assert client.jsonResponse['id'] is not None


@pytest.mark.ASP_317
@allure.feature("获取关系域详情")
class Test_GetMgntV1DomainRelationship(object):
    """
    Test_suites获取关系域详情
    """

    @allure.testcase("5243,域详情查询-查询关系域，返回200 ")
    def test_GetMgntV1DomainChildUUID(self):
        """
        # uuid为子域的主键，查询关系域为子域
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空本域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.208")  # 清空子域的关系域
        domain_data = CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")
        uuid = domain_data[0]
        res = CommonDocDomain().getRelationDomain(uuid=uuid)
        assert res['type'] == "child"
        assert res['host'] == '10.2.176.208'
        assert res['port'] == 443
        assert res['credential_id'] == domain_data[1]
        assert res['credential_key'] == domain_data[2]
        assert res['id'] == uuid

    @allure.testcase("5243,域详情查询-查询关系域，返回200 ")
    def test_GetMgntV1DomainarallelUUID(self, clear_domain_indirect):
        """
         # uuid为平级域的主键
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空本域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.180.162")  # 清空平级域的关系域
        result = CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="parallel")
        uuid = result[0]

        res = CommonDocDomain().getRelationDomain(uuid=uuid)
        assert res['type'] == "parallel"
        assert res['host'] == "10.2.180.162"
        assert res['port'] == 443
        assert res['credential_id'] == result[1]
        assert res['credential_key'] == result[2]
        assert res['id'] == uuid

    @pytest.fixture(scope="function")
    def clear_domain_indirect(self):
        yield
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")

    def test_GetMgntV1Domainarallel_child_direct(self, clear_domain_indirect):
        """
        查询子域直链模式，子域只有直链模式
        :param clear_domain_indirect:
        :return:
        """
        domain_data = CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="child",
                                                          network_type="direct")
        uuid = domain_data[0]
        res = CommonDocDomain().getRelationDomain(uuid=uuid)
        assert res["type"] == "child"
        assert res["host"] == "10.2.180.162"
        assert res["network_type"] == "direct"
        assert res["port"] == 443
        assert res['credential_id'] == domain_data[1]
        assert res['credential_key'] == domain_data[2]
        assert res['id'] == uuid

    def test_GetMgntV1Domainarallel_child_indirect(self, clear_domain_indirect):
        """
        添加子域非直链模式，查询结果，返回子域直链模式，子域只有直链模式
        :param clear_domain_indirect:
        :return:
        """
        domain_data = CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="child",
                                                          network_type="indirect")
        uuid = domain_data[0]
        res = CommonDocDomain().getRelationDomain(uuid=uuid)
        assert res["type"] == "child"
        assert res["host"] == "10.2.180.162"
        assert res["network_type"] == "direct"
        assert res["port"] == 443
        assert res['credential_id'] == domain_data[1]
        assert res['credential_key'] == domain_data[2]
        assert res['id'] == uuid

    def test_GetMgntV1Domainarallel_parallel_direct(self, clear_domain_indirect):
        """
        添加平级域直链模式，返回平级域直链模式
        :param clear_domain_indirect:
        :return:
        """
        domain_data = CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="parallel",
                                                          network_type="direct")
        uuid = domain_data[0]
        res = CommonDocDomain().getRelationDomain(uuid=uuid)
        assert res["type"] == "parallel"
        assert res["host"] == "10.2.180.162"
        assert res["network_type"] == "direct"
        assert res["port"] == 443
        assert res['credential_id'] == domain_data[1]
        assert res['credential_key'] == domain_data[2]
        assert res['id'] == uuid

    def test_GetMgntV1Domainarallel_parallel_indirect(self, clear_domain_indirect):
        """
        添加平级域非直链模式，返回平级域非直链模式  BUG ASP-6148
        :param clear_domain_indirect:
        :return:
        """
        domain_data = CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="parallel",
                                                          network_type="indirect")
        uuid = domain_data[0]
        res = CommonDocDomain().getRelationDomain(uuid=uuid)
        assert res["type"] == "parallel"
        assert res["host"] == "10.2.180.162"
        assert res["network_type"] == "indirect"
        assert res["port"] == 443
        assert res['id'] == uuid
        assert "credential_id" not in res
        assert "credential_key" not in res
        assert "secret" not in res
        assert "secret_type" not in res

