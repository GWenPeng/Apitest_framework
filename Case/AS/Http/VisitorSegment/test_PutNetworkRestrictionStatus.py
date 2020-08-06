# coding=utf-8
import pytest
import allure
from Common.readjson import JsonRead
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect


@pytest.mark.ASP_2371
@allure.feature("设置策略内容_修改白名单状态")
class Test_PutNetworkRestrictionStatus(object):
    """
     设置策略内容_修改白名单状态
    """

    @allure.step("设置访问者网段开关字段为True")
    @pytest.fixture(scope="function")
    def set_network_restriction_True(self):
        db = DB_connect(host="10.2.176.245")
        db.update('UPDATE policy_mgnt.t_policies set f_value = \'{"is_enabled":true}\' where '
                  'f_name="network_restriction";')

        yield db
        db.update('UPDATE policy_mgnt.t_policies set f_value = \'{"is_enabled":false}\' where '
                  'f_name="network_restriction";')
        db.close()

    @allure.testcase("4723, 访问者网段绑定白名单功能启用和关闭接口-启用关闭 ")
    @pytest.mark.high
    def test_put_network_restriction_status_close_enabled(self, set_network_restriction_True):
        """

        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.put(url="/api/policy-management/v1/general/network_restriction/value",
                   json=[{"name": "network_restriction", "value": {"is_enabled": True}}],
                   header='{"Content-Type":"application/json"}',
                   )
        assert client.status_code == 200
        assert client.elapsed <= 5.0
        result = set_network_restriction_True.select_one("SELECT f_value from policy_mgnt.t_policies where "
                                                         "f_name=\"network_restriction\";")
        assert result[0] == '{"is_enabled":true}'
        client2 = Http_client(tagname="HTTPGWP")
        client2.put(url="/api/policy-management/v1/general/network_restriction/value",
                    json=[{"name": "network_restriction", "value": {"is_enabled": False}}],
                    header='{"Content-Type":"application/json"}',
                    )
        assert client2.status_code == 200
        db = DB_connect(host="10.2.176.245")
        result1 = db.select_one("SELECT f_value from policy_mgnt.t_policies where "
                                "f_name=\"network_restriction\";")
        assert result1[0] == '{"is_enabled":false}'
        db.close()
        client3 = Http_client(tagname="HTTPGWP")
        client3.put(url="/api/policy-management/v1/general/network_restriction/value",
                    json=[{"name": "network_restriction", "value": {"is_enabled": False}}],
                    header='{"Content-Type":"application/json"}',
                    )
        db1 = DB_connect(host="10.2.176.245")
        result2 = db1.select_one("SELECT f_value from policy_mgnt.t_policies where "
                                 "f_name=\"network_restriction\";")
        assert result2[0] == '{"is_enabled":false}'
        db1.close()
        client3 = Http_client(tagname="HTTPGWP")
        client3.put(url="/api/policy-management/v1/general/network_restriction/value",
                    json=[{"name": "network_restriction", "value": {"is_enabled": True}}],
                    header='{"Content-Type":"application/json"}',
                    )
        db2 = DB_connect(host="10.2.176.245")
        result3 = db2.select_one("SELECT f_value from policy_mgnt.t_policies where "
                                 "f_name=\"network_restriction\";")
        assert result3[0] == '{"is_enabled":true}'
        db2.close()

    @allure.testcase("4722, 访问者网段绑定白名单功能启用和关闭接口-字段必填校验 ")
    @pytest.mark.low
    def test_put_net_restrict_status_verify_required(self, set_network_restriction_True):
        """
        BUG；ASP-6650 【策略同步-AT】设置策略内容body未包含name参数，未报错400
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.put(url="/api/policy-management/v1/general/network_restriction/value",
                   json=None,
                   header='{"Content-Type":"application/json"}',
                   )
        print(client.jsonResponse)
        assert client.status_code == 400
        assert client.jsonResponse["code"] == 400000000
        assert client.jsonResponse["message"] == "Invalid request."

        client2 = Http_client(tagname="HTTPGWP")
        client2.put(url="/api/policy-management/v1/general/network_restriction/value",
                    json=[],
                    header='{"Content-Type":"application/json"}',
                    )
        print(client2.jsonResponse)
        assert client2.status_code == 400

    @allure.testcase("4721, 访问者网段绑定白名单功能启用和关闭接口-字段值类型检查 ")
    @pytest.mark.low
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PutNetRestrictionStatusVerifyType.json").dict_value_join())
    def test_put_net_restrict_status_verify_type(self, url, header, jsondata, checkpoint):
        client = Http_client(tagname="HTTPGWP")
        client.put(url=url, json=jsondata, header=header, )
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        assert client.jsonResponse["code"] == checkpoint["code"]
        assert client.jsonResponse["message"] == checkpoint["message"]
        assert client.jsonResponse["detail"] == {"invalid_params": ['0', '0.value.is_enabled']}
