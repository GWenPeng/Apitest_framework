# coding=utf-8
import pytest
import allure
from Common.readjson import JsonRead
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect


@pytest.mark.ASP_2371
@allure.feature("获取所有策略信息_查询白名单状态")
class Test_GetNetworkRestrictionStatus(object):
    """
    获取所有策略信息_查询白名单状态
    """

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

    @allure.testcase("4719, 访问者网段绑定功能状态查询-查询关闭状态")
    @pytest.mark.high
    def test_get_network_restriction_status_false(self, close_network_restriction):
        """

        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/policy-management/v1/general?mode=current&offset=0&limit=1000&name"
                       "=network_restriction",
                   params={"mode": "current", "start": 0, "limit": -1, "name": "network_restriction"},
                   header='{"Content-Type":"application/json"}',
                   )
        print(client.jsonResponse)
        assert client.jsonResponse["count"] == 1
        assert client.jsonResponse["data"][0]["name"] == "network_restriction"
        assert client.jsonResponse["data"][0]["value"]["is_enabled"] is False
        assert client.status_code == 200
        assert client.elapsed <= 20.0

    @allure.step("开启访问者网段开关")
    @pytest.fixture(scope="function")
    def enabled_network_restriction(self):
        client = Http_client(tagname="HTTPGWP")
        client.put(url="/api/policy-management/v1/general/network_restriction/value",
                   json=[{"name": "network_restriction", "value": {"is_enabled": True}}],
                   header='{"Content-Type":"application/json"}',
                   )
        print(client.jsonResponse)
        assert client.status_code == 200

    @allure.testcase("4718, 访问者网段绑定功能状态查询-查询启用状态")
    @pytest.mark.high
    def test_get_network_restriction_status_True(self, enabled_network_restriction):
        """

        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/policy-management/v1/general?mode=current&offset=0&limit=1000&name"
                       "=network_restriction",
                   params={"mode": "current", "start": 0, "limit": -1, "name": "network_restriction"},
                   header='{"Content-Type":"application/json"}',
                   )
        print(client.jsonResponse)
        assert client.jsonResponse["count"] == 1
        assert client.jsonResponse["data"][0]["name"] == "network_restriction"
        assert client.jsonResponse["data"][0]["value"]["is_enabled"] is True
        assert client.status_code == 200
        assert client.elapsed <= 20.0

    # @allure.step("设置访问者网段开关为null")
    # @pytest.fixture(scope="function")
    # def set_network_restriction_null(self):
    #     db = DB_connect(host="10.2.176.245")
    #     db.update('UPDATE policy_mgnt.t_policies set f_value = NULL where '
    #               'f_name="network_restriction";')
    #
    #     yield
    #     db.update('UPDATE policy_mgnt.t_policies set f_value = \'{"is_enabled":false}\' where '
    #               'f_name="network_restriction";')

    # @allure.testcase("4720, 访问者网段绑定功能状态查询-查询启用状态") # "Column 'f_value' cannot be null")
    # @pytest.mark.low
    # def test_get_network_restriction_status_null(self,set_network_restriction_null):
    #     """
    #
    #     :return:
    #     """
    #     client = Http_client(tagname="HTTPGWP")
    #     client.get(url="/api/policy-management/v1/general?mode=current&offset=0&limit=1000&name"
    #                    "=network_restriction",
    #                params={"mode": "current", "start": 0, "limit": -1, "name": "network_restriction"},
    #                header='{"Content-Type":"application/json"}',
    #                )
    #     print(client.jsonResponse)
    #     assert client.status_code == 500
    #     assert client.elapsed <= 5.0

