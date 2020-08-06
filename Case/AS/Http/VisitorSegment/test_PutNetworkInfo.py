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
@allure.feature("网段修改接口")
class Test_PutNetworkInfo(object):
    """
     网段修改接口
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

    @allure.testcase("4765, 网段修改接口-校验请求字段必填   ")
    @allure.testcase("4870,网段修改接口-校验请求字段为空&null ")
    @allure.testcase("4770,网段修改接口-校验请求字段为空&null 正常返回")
    @pytest.mark.medium
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PutNetworkInfoVerifyField.json").dict_value_join())
    def test_put_network_info_verify_field(self, url, header, jsondata, checkpoint, add_network):
        """

       :return:
       """
        client = Http_client(tagname="HTTPGWP")
        client.put(url=url + add_network[0], header=header, json=jsondata)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 200:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]

    @allure.testcase("4870,网段修改接口-校验请求字段为空&null ")
    @allure.testcase("4767,网段修改接口-校验请求字段类型 ")
    @pytest.mark.medium
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PutNetworkInfoIdEmptyNull.json").dict_value_join())
    def test_put_network_info_id_empty_null(self, url, header, jsondata, checkpoint):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.put(url=url, header=header, json=jsondata)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.jsonResponse is not None and client.status_code != 200:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]

    @allure.testcase("4767,网段修改接口-校验请求字段类型")
    @pytest.mark.medium
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PutNetworkInfoVerifyFieldType.json").dict_value_join())
    def test_put_network_info_verify_field_type(self, url, header, jsondata, checkpoint, add_network):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.put(url=url + add_network[0], header=header, json=jsondata)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 200:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]

    @allure.testcase("4771,网段修改接口-校验end_ip>start_ip")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PutNetworkInfoStartIpBigEndIp.json").dict_value_join())
    def test_put_network_info_startIp_big_endIp(self, url, header, jsondata, checkpoint, add_network):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :param add_network:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.put(url=url + add_network[0], header=header, json=jsondata)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 200:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]

    @allure.testcase("4772,网段修改接口-校验数据库的数据重复")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PutNetworkInfoVerifyFieldRepeat.json").dict_value_join())
    def test_put_network_info_Verify_Field_Repeat(self, url, header, jsondata, checkpoint, add_network):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :param add_network:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.put(url=url + add_network[0], header=header, json=jsondata)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 200:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]

    @allure.testcase("4774,网段修改接口- id不存在时网段修改失败")
    @pytest.mark.high
    def test_put_network_info_id_not_exist(self, add_network):
        """
        :param add_network:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.put(url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[
            0] + "2", header={"Content-Type": "application/json"},
                   json={"name": "name", "start_ip": "10.2.181.1", "end_ip": "192.168.1.254",
                         "ip_address": "192.168.1.23", "netmask": "255.255.255.0", "net_type": "ip_mask"})
        print(client.jsonResponse)
        assert client.status_code == 404
        assert client.jsonResponse["code"] == 404013000
        assert client.jsonResponse["message"] == "Resource not found."
        assert client.jsonResponse["detail"] == {"notfound_params": ["id"]}

    @allure.testcase("4775, 网段修改接口-网段修改成功 ")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PutNetworkInfoEditSuccess.json").dict_value_join())
    def test_put_network_info_edit_success(self, url, header, jsondata, checkpoint, add_network):
        """

        :param add_network:
        :return:
        """
        res = CommonAccNetRestrictBoundPolicy().get_network_info(uuid=add_network[0])  # 修改之前
        assert res["end_ip"] == "10.2.181.255"
        # assert res["ip_address"] == ""
        assert res["name"] == "zhang"
        assert res["net_type"] == "ip_segment"
        # assert res["netmask"] == ""
        assert res["start_ip"] == "10.2.181.1"
        # print(res)
        client = Http_client(tagname="HTTPGWP")
        client.put(url=url + add_network[0], header=header, json=jsondata)
        # print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]

        res2 = CommonAccNetRestrictBoundPolicy().get_network_info(uuid=add_network[0])  # 修改之后
        print(res2)

        assert res2["id"] == add_network[0]
        assert res2["name"] == checkpoint["name"]
        assert res2["net_type"] == checkpoint["net_type"]
        if checkpoint["net_type"] == "ip_segment":
            assert res2["end_ip"] == checkpoint["end_ip"]
            assert res2["start_ip"] == checkpoint["start_ip"]
        else:
            assert res2["end_ip"] == checkpoint["end_ip"]
            assert res2["start_ip"] == checkpoint["start_ip"]
            assert res2["ip_address"] == checkpoint["ip_address"]
            assert res2["netmask"] == checkpoint["netmask"]

        res_net_type2 = CommonAccNetRestrictBoundPolicy().get_network_info(uuid=add_network[1])  # 修改之前
        # assert res_net_type2["end_ip"] == ""
        assert res_net_type2["ip_address"] == "192.168.1.23"
        assert res_net_type2["name"] == "zhangip_mask"
        assert res_net_type2["net_type"] == "ip_mask"
        assert res_net_type2["netmask"] == "255.255.255.0"
        # assert res_net_type2["start_ip"] == ""

        client2 = Http_client(tagname="HTTPGWP")
        jsondata["name"] = "name_repeat"
        client2.put(url=url + add_network[1], header=header, json=jsondata)
        print(client2.jsonResponse)
        assert client2.status_code == 409
        assert client2.jsonResponse["code"] == 409013000
        assert client2.jsonResponse["message"] == "Conflict resource."
        assert client2.jsonResponse["cause"] == ""
        assert client2.jsonResponse["detail"] == checkpoint["detail"]

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

    @allure.testcase("4776,网段修改接口-访问者网段绑定功能关闭")
    @pytest.mark.high
    def test_put_network_info_close_network_restrict(self, add_network, disabled_network_restriction):
        """

        :param add_network:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.put(url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[
            0], header={"Content-Type": "application/json"},
                   json={"name": "name", "start_ip": "10.2.181.1", "end_ip": "192.168.1.254",
                         "ip_address": "192.168.1.23", "netmask": "255.255.255.0", "net_type": "ip_mask"})
        # print(client.jsonResponse)
        assert client.status_code == 403
        assert client.jsonResponse["code"] == 403013000
        assert client.jsonResponse["message"] == "No permission to do this operation."
        assert client.jsonResponse["cause"] == "Network restriction function is not enabled."

    @allure.testcase("4918,网段修改接口-校验字段ip_address不符合格式、范围 ")
    @allure.testcase("4922,网段修改接口-校验字段end_ip不符合格式、范围 ")
    @allure.testcase("4920,网段修改接口-校验字段netmask不符合格式、范围  ")
    @allure.testcase("4923,网段修改接口-校验字段start_ip不符合格式、范围 ")
    @pytest.mark.medium
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PutNetworkInfoFormatError.json").dict_value_join())
    def test_put_network_info_format_error(self, url, header, jsondata, checkpoint, add_network):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :param add_network:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.put(url=url + add_network[0], header=header, json=jsondata)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 200:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]

    @allure.testcase("4924,网段修改接口-name不能为特殊字符")
    @pytest.mark.medium
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PutNetworkInfoNameSpecialChart.json").dict_value_join())
    def test_put_network_info_name_special_chart(self, url, header, jsondata, checkpoint, add_network):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :param add_network:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.put(url=url + add_network[0], header=header, json=jsondata)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 200:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]

    @allure.testcase("网段修改接口-修改“所有网段”信息")
    @pytest.mark.high
    def test_put_network_info_public_net(self):
        client = Http_client(tagname="HTTPGWP")
        client.put(url="/api/policy-management/v1/user-login/network-restriction/network/public-net",
                   header={"Content-Type": "application/json"},
                   json={"end_ip": "12.133.14.121", "ip_address": "10.2.54.11", "name": "namereat",
                         "net_type": "ip_mask", "netmask": "255.255.252.0", "start_ip": "11.113.12.171"})
        print(client.jsonResponse)
        assert client.status_code == 403
        assert client.jsonResponse["code"] == 403013000
        assert client.jsonResponse["message"] == "No permission to do this operation."
        assert client.jsonResponse["cause"] == "Public net can only be read."
