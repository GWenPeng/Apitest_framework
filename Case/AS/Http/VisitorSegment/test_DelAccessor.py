# coding=utf-8
import pytest
import allure
from flaky import flaky

from Common.readjson import JsonRead
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect
from .CommonVisitorSegment import CommonAccNetRestrictBoundPolicy


@allure.step("开启访问者网段开关")
@pytest.fixture(scope="function", autouse=True)
def enabled_network_restriction():
    client = Http_client(tagname="HTTPGWP")
    client.put(url="/api/policy-management/v1/general/network_restriction/value",
               json=[{"name": "network_restriction", "value": {"is_enabled": True}}],
               header='{"Content-Type":"application/json"}',
               )
    assert client.status_code == 200


@pytest.mark.ASP_2371
@allure.feature("访问者删除接口")
@flaky(max_runs=3, min_passes=1)
class Test_DelAccessor(object):
    """
     访问者删除接口
    """

    @allure.step("新增访问者网段数据")
    @pytest.fixture(scope="function")
    def add_network(self):
        """

        :return:
        """
        ip_segment_uuid = None
        ip_mask_uuid = None
        try:
            ip_segment_uuid = CommonAccNetRestrictBoundPolicy().add_Network(host="10.2.176.245", name="zhang",
                                                                            start_ip="10.2.181.1",
                                                                            end_ip="10.2.181.255",
                                                                            net_type="ip_segment")
            ip_mask_uuid = CommonAccNetRestrictBoundPolicy().add_Network(host="10.2.176.245", name="zhangip_mask",
                                                                         start_ip="10.2.181.1",
                                                                         end_ip="10.2.181.255",
                                                                         ip_address="192.168.1.23"
                                                                         , netmask="255.255.255.0", net_type="ip_mask")
        except AssertionError as e:
            print("添加网段断言失败，可能已存在数据", e)
        yield ip_segment_uuid, ip_mask_uuid
        CommonAccNetRestrictBoundPolicy().clear_Network_list(host="10.2.176.245")

    @allure.testcase("4790, 访问者删除接口-校验请求字段必填")
    @allure.testcase("4791,  访问者删除接口-校验请求字段类型")
    @allure.testcase("4793,  访问者删除接口-删除失败 ")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,url_accessor,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/DelAccessorVerifyFiled.json").dict_value_join())
    def test_del_accessor_verify_field(self, url, header, url_accessor, jsondata, checkpoint, add_network):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :param add_network:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        if "accessor" in url:
            client.delete(url=url, header=header)
        else:
            client.delete(url=url + add_network[0] + url_accessor, header=header)

        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if "accessor" in url and client.status_code != 207 and "no_body" not in checkpoint:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]
        elif client.status_code == 207:
            print(client.jsonResponse)
            assert client.jsonResponse[0]["id"] == checkpoint["id"]
            assert client.jsonResponse[0]["status"] == checkpoint["status"]
            # assert client.jsonResponse[0]["body"] == checkpoint["header"]
            assert client.jsonResponse[0]["body"]["code"] == checkpoint["code"]
            assert client.jsonResponse[0]["body"]["message"] == checkpoint["message"]
            assert client.jsonResponse[0]["body"]["cause"] == checkpoint["cause"]
            assert client.jsonResponse[0]["body"]["detail"] == checkpoint["detail"]

    @allure.step("新增访问者")
    def add_accessor(self):
        CommonAccNetRestrictBoundPolicy().add_accessor_network()

    @allure.testcase("4794, 访问者删除接口-删除成功 ")
    @pytest.mark.high
    @pytest.mark.parametrize("jsondata,accessor_id,accessor_name",
                             [([{"accessor_id": "266c6a42-6131-4d62-8f39-853e7093701c", "accessor_type": "user"}],
                               "266c6a42-6131-4d62-8f39-853e7093701c", ["admin"]),
                              ([{"accessor_id": "266c6a42-6131-4d62-8f39-853e7093701c", "accessor_type": "user"},
                                {"accessor_id": "151bcb65-48ce-4b62-973f-0bb6685f9cb8", "accessor_type": "department"},
                                {"accessor_id": "234562BE-88FF-4440-9BFF-447F139871A2", "accessor_type": "user"}],
                               "266c6a42-6131-4d62-8f39-853e7093701c,151bcb65-48ce-4b62-973f-0bb6685f9cb8,"
                               "234562BE-88FF-4440-9BFF-447F139871A2", ["admin", "组织结构", "system"])])
    def test_del_accessor_success_user(self, add_network, jsondata, accessor_id, accessor_name):
        """
        BUG ASP-6837【访问者网段白名单策略绑定-AT】删除访问者接口，当访问者删除成功后，返回参数header中accessor_name和accessor_type为空
        :param add_network:
        :param jsondata:
        :param accessor_id:
        :param accessor_name:
        :return:
        """
        sul = CommonAccNetRestrictBoundPolicy().add_accessor_network(
            network_id=add_network[0], jsondata=jsondata)
        print(sul)
        for index in range(len(jsondata)):
            assert sul[index]["status"] == 201
            assert sul[index]["id"] == jsondata[index]["accessor_id"]
            assert sul[index]["body"] == {"accessor_id": jsondata[index]["accessor_id"],
                                          "accessor_name": accessor_name[index],
                                          "accessor_type": jsondata[index]["accessor_type"]}
        res = CommonAccNetRestrictBoundPolicy().del_accessor_network(network_id=add_network[0], accessor_id=accessor_id)
        print(res)
        for index in range(len(jsondata)):
            assert res[index]["status"] == 200
            assert res[index]["id"] == jsondata[index]["accessor_id"]
            assert res[index]["body"] == {"accessor_id": jsondata[index]["accessor_id"],
                                          "accessor_name": "",
                                          "accessor_type": ""}

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
                   header={"Content-Type": "application/json"},
                   )
        assert client.status_code == 200

    @allure.testcase("4795, 访问者删除接口-访问者网段绑定功能关闭 ")
    @pytest.mark.high
    def test_del_accessor_disabled_network_restriction(self, add_network, disabled_network_restriction):
        """

        :param add_network:
        :param disabled_network_restriction:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.delete(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[
                0] + "/accessor/" + "266c6a42-6131-4d62-8f39-853e7093701c",
            header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.status_code == 207
        assert client.jsonResponse[0]["id"] == ""
        assert client.jsonResponse[0]["status"] == 403
        assert client.jsonResponse[0]["body"] == {'code': 403013000, 'message': 'No permission to do this operation.',
                                                  'cause': 'Network restriction function is not enabled.'}

    @allure.testcase("访问者删除接口-删除绑定所有网段的访问者 ")
    @pytest.mark.high
    def test_del_accessor_public_net(self):
        client = Http_client(tagname="HTTPGWP")
        client.delete(
            url="/api/policy-management/v1/user-login/network-restriction/network/public-net/accessor/"
                + "266c6a42-6131-4d62-8f39-853e7093701c",
            header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.status_code == 207
