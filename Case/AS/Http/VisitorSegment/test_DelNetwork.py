# coding=utf-8
import pytest
import allure
from Common.readjson import JsonRead
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect
from .CommonVisitorSegment import CommonAccNetRestrictBoundPolicy


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
@allure.feature("删除网段接口")
class Test_DelNetwork(object):
    """
     删除网段接口
    """

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

    @allure.testcase("4764,网段删除接口-校验请求字段必填")
    @pytest.mark.high
    def test_Del_network_info_verify_field(self):
        """

        :param add_network:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.delete(url="/api/policy-management/v1/user-login/network-restriction/network/",
                      header='{"Content-Type":"application/json"}')
        print(client.jsonResponse)
        assert client.status_code == 404

    @allure.testcase("4764,网段删除接口-校验请求字段必填")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/DelNetworkVerifyFieldType.json").dict_value_join())
    def test_Del_network_info_verify_field(self, url, header, jsondata, checkpoint):
        """

        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.delete(url=url, header='{"Content-Type":"application/json"}')
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 200:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]

    @allure.testcase("4781,网段删除接口-网段删除失败")
    @pytest.mark.high
    def test_Del_network_info_failed(self, add_network):
        client = Http_client(tagname="HTTPGWP")
        client.delete(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[
                0] + "f",
            header='{"Content-Type":"application/json"}')
        print(client.jsonResponse)
        assert client.status_code == 404
        assert client.jsonResponse["code"] == 404013000
        assert client.jsonResponse["cause"] == ""
        assert client.jsonResponse["message"] == "Resource not found."
        assert client.jsonResponse["detail"] == {"notfound_params": ["id"]}

    @allure.testcase("4782,网段删除接口-网段删除成功 ")
    @pytest.mark.high
    def test_Del_network_success(self, add_network):
        res0 = CommonAccNetRestrictBoundPolicy().get_Network_list()
        print(res0)
        assert len(res0["data"]) == 3
        client = Http_client(tagname="HTTPGWP")
        client.delete(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[0],
            header='{"Content-Type":"application/json"}')
        print(client.jsonResponse)
        assert client.status_code == 200
        res1 = CommonAccNetRestrictBoundPolicy().get_Network_list()
        print(res1)
        assert len(res1["data"]) == 2
        client.delete(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[1],
            header='{"Content-Type":"application/json"}')
        assert client.status_code == 200

        res2 = CommonAccNetRestrictBoundPolicy().get_Network_list()
        print(res2)
        assert res2["data"] is None or len(res2["data"]) == 1

    @allure.step("关闭访问者网段绑定功能开关")
    @pytest.fixture(scope="function")
    def disabled_network_restriction(self):
        client = Http_client(tagname="HTTPGWP")
        client.put(url="/api/policy-management/v1/general/network_restriction/value",
                   json=[{"name": "network_restriction", "value": {"is_enabled": False}}],
                   header='{"Content-Type":"application/json"}',
                   )
        assert client.status_code == 200
        yield
        client = Http_client(tagname="HTTPGWP")
        client.put(url="/api/policy-management/v1/general/network_restriction/value",
                   json=[{"name": "network_restriction", "value": {"is_enabled": True}}],
                   header='{"Content-Type":"application/json"}',
                   )
        assert client.status_code == 200

    @allure.testcase("4782,网段删除接口-网段删除成功 ")
    @pytest.mark.high
    def test_Del_network_close_network_restrict(self, add_network, disabled_network_restriction):
        """

        :param add_network:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.delete(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[0],
            header='{"Content-Type":"application/json"}')
        print(client.jsonResponse)
        assert client.status_code == 403
        assert client.jsonResponse["code"] == 403013000
        assert client.jsonResponse["message"] == "No permission to do this operation."
        assert client.jsonResponse["cause"] == "Network restriction function is not enabled."

    @allure.step("添加访问者")
    @pytest.fixture(scope="function")
    def add_accessor(self):
        accessor_user_id = "266c6a42-6131-4d62-8f39-853e7093701c"
        accessor_department_id = "151bcb65-48ce-4b62-973f-0bb6685f9cb8"
        CommonAccNetRestrictBoundPolicy().add_accessor_network(
            network_id="public-net",
            jsondata=[{"accessor_id": accessor_user_id, "accessor_type": "user"},
                      {"accessor_id": accessor_department_id, "accessor_type": "department"}])
        return accessor_user_id, accessor_department_id

    @allure.testcase("网段删除接口-删除所有网段 ")
    @pytest.mark.high
    def test_Del_network_public_net(self, add_accessor):
        client = Http_client(tagname="HTTPGWP")
        client.delete(
            url="/api/policy-management/v1/user-login/network-restriction/network/public-net/accessor/" + add_accessor[
                0] + ',' + add_accessor[1],
            header='{"Content-Type":"application/json"}')
        # print(client.jsonResponse)
        assert client.status_code == 207
        for i in range(len(client.jsonResponse)):
            assert client.jsonResponse[i]["id"] == add_accessor[i]
            assert client.jsonResponse[i]["status"] == 200
            assert client.jsonResponse[i]["body"] == {'accessor_id': add_accessor[i], 'accessor_name': '',
                                                      'accessor_type': ''}
