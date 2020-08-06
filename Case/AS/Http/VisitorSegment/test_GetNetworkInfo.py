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
@allure.feature("获取网段信息接口")
class Test_GetNetworkInfo(object):
    """
    获取网段信息接口
    """

    @allure.testcase("6916,获取网段信息--网段id不存在")
    @pytest.mark.high
    def test_Get_Network_id_not_exist(self):
        """
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/policy-management/v1/user-login/network-restriction/network/35ca2311-a0e3"
                       "-4e58-894e-b3333724d93b", header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.status_code == 404
        assert client.jsonResponse["code"] == 404013000
        assert client.jsonResponse["message"] == "Resource not found."
        assert client.jsonResponse["detail"] == {"notfound_params": ["id"]}

    @allure.step("新增访问者网段数据")
    @pytest.fixture(scope="function")
    def add_network(self):
        """

        :return:
        """
        ip_segment_uuid = CommonAccNetRestrictBoundPolicy().add_Network(host="10.2.176.245", name="zhang",
                                                                        start_ip="10.2.181.1",
                                                                        end_ip="10.2.181.255", net_type="ip_segment")
        ip_mask_uuid = CommonAccNetRestrictBoundPolicy().add_Network(host="10.2.176.245", name="zhangip_mask",
                                                                     start_ip="10.2.181.1",
                                                                     end_ip="10.2.181.255", ip_address="192.168.1.23"
                                                                     , netmask="255.255.255.0", net_type="ip_mask")

        yield ip_segment_uuid, ip_mask_uuid
        CommonAccNetRestrictBoundPolicy().clear_Network_list(host="10.2.176.245")

    @allure.testcase("6917,获取网段信息--网段id存在")
    @pytest.mark.high
    def test_Get_Network_id_exist(self, add_network):
        """
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[0]
                   , header={"Content-Type": "application/json"})
        client1 = Http_client(tagname="HTTPGWP")
        client1.get(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[1]
            , header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        print(client1.jsonResponse)
        assert client.status_code == 200
        assert client.jsonResponse["end_ip"] == "10.2.181.255"
        assert client.jsonResponse["id"] == add_network[0]
        # assert client.jsonResponse["ip_address"] == ""
        assert client.jsonResponse["name"] == "zhang"
        assert client.jsonResponse["net_type"] == "ip_segment"
        # assert client.jsonResponse["netmask"] == ""
        assert client.jsonResponse["start_ip"] == "10.2.181.1"
        assert client1.status_code == 200
        # assert client1.jsonResponse["end_ip"] == ""
        assert client1.jsonResponse["id"] == add_network[1]
        assert client1.jsonResponse["ip_address"] == "192.168.1.23"
        assert client1.jsonResponse["name"] == "zhangip_mask"
        assert client1.jsonResponse["net_type"] == "ip_mask"
        assert client1.jsonResponse["netmask"] == "255.255.255.0"
        # assert client1.jsonResponse["start_ip"] == ""

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

    @allure.testcase("6918, 访问者网段绑定功能关闭")
    @pytest.mark.high
    def test_get_network_info_close_network_restriction(self, add_network, close_network_restriction):
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[0]
                   , header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.status_code == 200
        assert client.jsonResponse["end_ip"] == "10.2.181.255"
        assert client.jsonResponse["id"] == add_network[0]
        # assert client.jsonResponse["ip_address"] == ""
        assert client.jsonResponse["name"] == "zhang"
        assert client.jsonResponse["net_type"] == "ip_segment"
        # assert client.jsonResponse["netmask"] == ""
        assert client.jsonResponse["start_ip"] == "10.2.181.1"

    @allure.testcase("获取所有网段信息")
    @pytest.mark.high
    def test_get_network_info_public_net(self):
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/policy-management/v1/user-login/network-restriction/network/public-net"
                   , header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.status_code == 200
        # assert client.jsonResponse["end_ip"] == ""
        assert client.jsonResponse["id"] == "public-net"
        # assert client.jsonResponse["ip_address"] == ""
        # assert client.jsonResponse["name"] == ""
        assert client.jsonResponse["net_type"] == ""
        # assert client.jsonResponse["netmask"] == ""
        # assert client.jsonResponse["start_ip"] == ""
