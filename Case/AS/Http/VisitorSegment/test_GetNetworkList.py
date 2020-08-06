# coding=utf-8
from Common.readjson import JsonRead
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect
from .CommonVisitorSegment import CommonAccNetRestrictBoundPolicy
import pytest
import allure
import time


@allure.step("开启访问者网段开关")
@pytest.fixture(scope="class", autouse=True)
def enabled_network_restriction():
    client = Http_client(tagname="HTTPGWP")
    client.put(url="/api/policy-management/v1/general/network_restriction/value",
               json=[{"name": "network_restriction", "value": {"is_enabled": True}}],
               header='{"Content-Type":"application/json"}',
               )
    assert client.status_code == 200


@pytest.mark.ASP_2371
@allure.feature("网段列表查询接口")
class Test_GetNetworkList(object):
    """
    网段列表查询接口
    """

    @allure.testcase("4905,网段列表查询接口-校验请求字段必填")
    @allure.testcase("4724,网段列表查询接口-校验请求字段必填")
    @pytest.mark.low
    @pytest.mark.parametrize("url,header,param,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/GetNetworkListVerifyField.json").dict_value_join())
    def test_Get_Network_Verify_field(self, url, header, param, checkpoint):
        """

        :param url:
        :param header:
        :param param:
        :param checkpoint:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(url=url, params=param, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code == 400:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]
        else:
            assert "count" in client.jsonResponse
            assert "data" in client.jsonResponse

    @allure.step("新增访问者网段数据")
    @pytest.fixture(scope="function")
    def add_network(self):
        """

        :return:
        """
        CommonAccNetRestrictBoundPolicy().add_Network(host="10.2.176.245", name="zhang", start_ip="10.2.181.1",
                                                      end_ip="10.2.181.255", net_type="ip_segment")
        CommonAccNetRestrictBoundPolicy().add_Network(host="10.2.176.245", name="zhang11", start_ip="10.2.182.1",
                                                      end_ip="10.2.182.255", net_type="ip_segment")
        CommonAccNetRestrictBoundPolicy().add_Network(host="10.2.176.245", name="网段3", start_ip="10.2.183.1",
                                                      end_ip="10.2.183.255", net_type="ip_segment")
        yield
        CommonAccNetRestrictBoundPolicy().clear_Network_list(host="10.2.176.245")

    @allure.testcase("4904,网段列表查询接口-校验请求字段边界值")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,param,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/GetNetworkListPage.json").dict_value_join())
    def test_Get_Network_Page(self, url, header, param, checkpoint, add_network):
        """

        :param url:
        :param header:
        :param param:
        :param checkpoint:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(url=url, params=param, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code == 400:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]
        else:
            assert client.jsonResponse["count"] == checkpoint["count"]
            assert len(client.jsonResponse["data"]) == checkpoint["data.index"]

    @allure.testcase("4903,网段列表查询接口-校验字段为空为null")
    @pytest.mark.low
    @pytest.mark.parametrize("url,header,param,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/GetNetworkListNull.json").dict_value_join())
    def test_get_network_list_null(self, url, header, param, checkpoint):
        """

        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(url=url, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 200:
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]

    @allure.step("关闭访问者网段开关")
    @pytest.fixture(scope="function")
    def close_network_restriction(self):
        client = Http_client(tagname="HTTPGWP")
        client.put(url="/api/policy-management/v1/general/network_restriction/value",
                   json=[{"name": "network_restriction", "value": {"is_enabled": False}}],
                   header='{"Content-Type":"application/json"}',
                   )
        print(client.jsonResponse)
        assert client.status_code == 200
        yield
        client = Http_client(tagname="HTTPGWP")
        client.put(url="/api/policy-management/v1/general/network_restriction/value",
                   json=[{"name": "network_restriction", "value": {"is_enabled": True}}],
                   header='{"Content-Type":"application/json"}',
                   )
        print(client.jsonResponse)
        assert client.status_code == 200

    @allure.testcase("4728, 网段列表查询接口-访问者网段绑定功能关闭 ")
    @pytest.mark.medium
    def test_get_network_list_close_network_restriction(self, close_network_restriction):
        client = Http_client(tagname="HTTPGWP")
        client.get(
            url="/api/policy-management/v1/user-login/network-restriction/network?key_word=\"\"&offset=0"
                "&limit=1000",
            header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.status_code == 200

    @allure.step("新增访问者网段数据")
    @pytest.fixture(scope="function")
    def add_Network(self):
        """

        :return:
        """
        CommonAccNetRestrictBoundPolicy().add_Network(host="10.2.176.245", name="zhang", start_ip="10.2.181.1",
                                                      end_ip="10.2.181.255", net_type="ip_segment")
        time.sleep(1)
        CommonAccNetRestrictBoundPolicy().add_Network(host="10.2.176.245", name="zhang11", start_ip="10.2.182.1",
                                                      end_ip="10.2.182.255", net_type="ip_segment")
        time.sleep(1)
        CommonAccNetRestrictBoundPolicy().add_Network(host="10.2.176.245", name="1000", start_ip="13.2.183.1",
                                                      end_ip="13.2.183.255", net_type="ip_segment")
        yield
        CommonAccNetRestrictBoundPolicy().clear_Network_list(host="10.2.176.245")

    @allure.testcase("4727,  网段列表查询接口-key_word关键字搜索")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,param,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/GetNetworkListKeywordSearch.json").dict_value_join())
    def test_get_network_list_search(self, url, header, param, checkpoint, add_Network):
        """

        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(url=url, params=param, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        assert client.jsonResponse["count"] == checkpoint["count"]
        assert len(client.jsonResponse["data"]) == checkpoint["data.len"]
        if checkpoint["count"] > 0:
            for index in range(checkpoint["count"]):
                assert client.jsonResponse["data"][index]["start_ip"] == checkpoint["data." + str(index) + ".start_ip"]

    @allure.step("新增200条网段数据")
    @pytest.fixture(scope="function")
    def add_200Network(self):
        """

        :return:
        """
        for index in range(200):
            CommonAccNetRestrictBoundPolicy().add_Network(host="10.2.176.245", name="zhang" + str(index),
                                                          start_ip="10.2.181." + str(1 + index), end_ip="10.2.181.255",
                                                          net_type="ip_segment")

        yield
        CommonAccNetRestrictBoundPolicy().clear_Network_list(host="10.2.176.245")

    @allure.testcase("4726, 网段列表查询接口-校验请求字段边界值")
    @pytest.mark.medium
    @pytest.mark.parametrize("url,header,param,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/GetNetworkListOutOfIndex.json").dict_value_join())
    def test_get_network_list_out_of_index(self, url, header, param, checkpoint, add_200Network):
        """

        :param url:
        :param header:
        :param param:
        :param checkpoint:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(url=url, params=param, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code == 400:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]
        else:
            assert client.jsonResponse["count"] == checkpoint["count"]
            assert len(client.jsonResponse["data"]) == checkpoint["data.len"]

    @allure.testcase("4725, 网段列表查询接口-校验请求字段类型")
    @pytest.mark.low
    @pytest.mark.parametrize("url,header,param,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/GetNetworkListTypeError.json").dict_value_join())
    def test_get_network_list_type_error(self, url, header, param, checkpoint):
        """

        :param url:
        :param header:
        :param param:
        :param checkpoint:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(url=url, params=param, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code == 400:
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]

    @allure.testcase("获取默认值——所有网段")
    @pytest.mark.high
    def test_get_network_list_default(self):
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/policy-management/v1/user-login/network-restriction/network?limit=1&offset=0&key_word=",
                   header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.status_code == 200
        assert client.jsonResponse["count"] == 1
        assert len(client.jsonResponse["data"]) == 1
        assert client.jsonResponse["data"][0]["id"] == "public-net"
        assert client.jsonResponse["data"][0]["net_type"] == ""

    @allure.testcase("10324 网段列表查询接口-offset,limit默认值")
    @allure.testcase("10326 网段列表查询接口-limit边界值合法验证")
    @pytest.mark.high
    def test_get_network_list_offset_limit_default(self, add_200Network):
        # offset字段不传
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/policy-management/v1/user-login/network-restriction/network?limit=200&key_word=",
                   header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.status_code == 200
        assert client.jsonResponse["count"] == 201
        assert len(client.jsonResponse["data"]) == 200
        assert client.jsonResponse["data"][0]["id"] == "public-net"

        # limit字段不传
        client1 = Http_client(tagname="HTTPGWP")
        client1.get(url="/api/policy-management/v1/user-login/network-restriction/network?offset=0&key_word=",
                    header={"Content-Type": "application/json"})
        print(client1.jsonResponse)
        assert client1.status_code == 200
        assert client1.jsonResponse["count"] == 201
        assert len(client1.jsonResponse["data"]) == 20
        assert client1.jsonResponse["data"][0]["id"] == "public-net"

        # offset和limit值不传
        client2 = Http_client(tagname="HTTPGWP")
        client2.get(url="/api/policy-management/v1/user-login/network-restriction/network?offset=&limit=200&key_word=",
                    header={"Content-Type": "application/json"})
        print(client2.jsonResponse)
        assert client2.status_code == 200
        assert client2.jsonResponse["count"] == 201
        assert len(client2.jsonResponse["data"]) == 200
        assert client2.jsonResponse["data"][0]["id"] == "public-net"

        # offset和limit值不传
        client3 = Http_client(tagname="HTTPGWP")
        client3.get(url="/api/policy-management/v1/user-login/network-restriction/network?offset=0&limit=&key_word=",
                    header={"Content-Type": "application/json"})
        print(client3.jsonResponse)
        assert client3.status_code == 200
        assert client3.jsonResponse["count"] == 201
        assert len(client3.jsonResponse["data"]) == 20
        assert client3.jsonResponse["data"][0]["id"] == "public-net"

        # limit输入1
        client4 = Http_client(tagname="HTTPGWP")
        client4.get(url="/api/policy-management/v1/user-login/network-restriction/network?offset=0&limit=1&key_word=",
                    header={"Content-Type": "application/json"})
        print(client4.jsonResponse)
        assert client4.status_code == 200
        assert client4.jsonResponse["count"] == 201
        assert len(client4.jsonResponse["data"]) == 1
        assert client4.jsonResponse["data"][0]["id"] == "public-net"

        # limit输入2
        client5 = Http_client(tagname="HTTPGWP")
        client5.get(url="/api/policy-management/v1/user-login/network-restriction/network?offset=0&limit=2&key_word=",
                    header={"Content-Type": "application/json"})
        print(client5.jsonResponse)
        assert client5.status_code == 200
        assert client5.jsonResponse["count"] == 201
        assert len(client5.jsonResponse["data"]) == 2
        assert client5.jsonResponse["data"][0]["id"] == "public-net"

        # limit输入1000
        client6 = Http_client(tagname="HTTPGWP")
        client6.get(
            url="/api/policy-management/v1/user-login/network-restriction/network?offset=0&limit=1000&key_word=",
            header={"Content-Type": "application/json"})
        print(client6.jsonResponse)
        assert client6.status_code == 200
        assert client6.jsonResponse["count"] == 201
        assert len(client6.jsonResponse["data"]) == 201
        assert client6.jsonResponse["data"][0]["id"] == "public-net"

        # limit输入999
        client7 = Http_client(tagname="HTTPGWP")
        client7.get(
            url="/api/policy-management/v1/user-login/network-restriction/network?offset=0&limit=999&key_word=",
            header={"Content-Type": "application/json"})
        print(client7.jsonResponse)
        assert client7.status_code == 200
        assert client7.jsonResponse["count"] == 201
        assert len(client7.jsonResponse["data"]) == 201
        assert client7.jsonResponse["data"][0]["id"] == "public-net"

        # offset 输入1
        client7 = Http_client(tagname="HTTPGWP")
        client7.get(
            url="/api/policy-management/v1/user-login/network-restriction/network?offset=1&limit=1000&key_word=",
            header={"Content-Type": "application/json"})
        print(client7.jsonResponse)
        assert client7.status_code == 200
        assert client7.jsonResponse["count"] == 201
        assert len(client7.jsonResponse["data"]) == 200
        assert client7.jsonResponse["data"][0]["name"] == "zhang199"
        assert client7.jsonResponse["data"][0]["start_ip"] == "10.2.181.200"
        assert client7.jsonResponse["data"][0]["end_ip"] == "10.2.181.255"
        assert client7.jsonResponse["data"][0]["net_type"] == "ip_segment"

    @allure.testcase("10326 网段列表查询接口-limit边界值合法验证")
    @pytest.mark.high
    def test_get_network_list_verify_offset_limit(self):
        # limit输入0
        client7 = Http_client(tagname="HTTPGWP")
        client7.get(
            url="/api/policy-management/v1/user-login/network-restriction/network?offset=0&limit=0&key_word=",
            header={"Content-Type": "application/json"})
        print(client7.jsonResponse)
        assert client7.status_code == 400
        assert client7.jsonResponse["code"] == 400000000
        assert client7.jsonResponse["message"] == "Invalid request."
        assert client7.jsonResponse["cause"] == ""
        assert client7.jsonResponse["detail"] == {'invalid_params': ['limit']}

        # limit输入-1
        client6 = Http_client(tagname="HTTPGWP")
        client6.get(
            url="/api/policy-management/v1/user-login/network-restriction/network?offset=0&limit=-1&key_word=",
            header={"Content-Type": "application/json"})
        print(client6.jsonResponse)
        assert client6.status_code == 400
        assert client6.jsonResponse["code"] == 400000000
        assert client6.jsonResponse["message"] == "Invalid request."
        assert client6.jsonResponse["cause"] == ""
        assert client6.jsonResponse["detail"] == {'invalid_params': ['limit']}

        # limit输入1001
        client5 = Http_client(tagname="HTTPGWP")
        client5.get(
            url="/api/policy-management/v1/user-login/network-restriction/network?offset=0&limit=1001&key_word=",
            header={"Content-Type": "application/json"})
        print(client5.jsonResponse)
        assert client5.status_code == 400
        assert client5.jsonResponse["code"] == 400000000
        assert client5.jsonResponse["message"] == "Invalid request."
        assert client5.jsonResponse["cause"] == ""
        assert client5.jsonResponse["detail"] == {'invalid_params': ['limit']}

        # offset输入-1
        client4 = Http_client(tagname="HTTPGWP")
        client4.get(
            url="/api/policy-management/v1/user-login/network-restriction/network?offset=-1&limit=1000&key_word=",
            header={"Content-Type": "application/json"})
        print(client4.jsonResponse)
        assert client4.status_code == 400
        assert client4.jsonResponse["code"] == 400000000
        assert client4.jsonResponse["message"] == "Invalid request."
        assert client4.jsonResponse["cause"] == ""
        assert client4.jsonResponse["detail"] == {'invalid_params': ['offset']}

        # offset输入-2
        client3 = Http_client(tagname="HTTPGWP")
        client3.get(
            url="/api/policy-management/v1/user-login/network-restriction/network?offset=-1&limit=1000&key_word=",
            header={"Content-Type": "application/json"})
        print(client3.jsonResponse)
        assert client3.status_code == 400
        assert client3.jsonResponse["code"] == 400000000
        assert client3.jsonResponse["message"] == "Invalid request."
        assert client3.jsonResponse["cause"] == ""
        assert client3.jsonResponse["detail"] == {'invalid_params': ['offset']}
