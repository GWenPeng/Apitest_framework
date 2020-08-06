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
@allure.feature("网段新增接口")
class Test_AddNetwork(object):
    """
     网段新增接口
    """

    @allure.testcase("4763,  网段新增接口-网段新增成功")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PostAddNetworkSuccess.json").dict_value_join())
    def test_Add_Network_Success(self, url, header, jsondata, checkpoint):
        """

        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.post(url=url, jsondata=jsondata, header=header)
        location = client.respheaders["Location"]
        print(location)
        assert client.status_code == checkpoint["status_code"]
        assert checkpoint["resp.headers.Location"] in client.respheaders["Location"]
        assert client.elapsed <= 5.0
        print(location.split("/")[-1])
        CommonAccNetRestrictBoundPolicy().del_Network(host="10.2.176.245", network_id=location.split("/")[-1])

    @allure.testcase("4763,  网段新增接口-网段新增失败")
    @allure.issue(url="https://jira.aishu.cn/browse/ASP-6659", name="【访问者网段白名单策略绑定-AT】网段新增接口name字段超出128字符时，新增报错400"
                                                                    "，未定义具体错误码")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PostAddNetworkFailed.json").dict_value_join())
    def test_Add_Network_Failed(self, url, header, jsondata, checkpoint):
        """
        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.post(url=url, jsondata=jsondata, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        assert client.jsonResponse["code"] == checkpoint["code"]
        assert client.jsonResponse["message"] == checkpoint["message"]
        assert client.jsonResponse["detail"] == checkpoint["detail"]

    @pytest.fixture(scope="function")
    def clear_data(self):
        yield
        CommonAccNetRestrictBoundPolicy().clear_Network_list(host="10.2.176.245")

    @allure.testcase("4729, 网段新增接口-校验请求字段必填 ")
    @pytest.mark.low
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PostAddNetworkVerifyField.json").dict_value_join())
    def test_Add_Network_verify_field(self, url, header, jsondata, checkpoint, clear_data):
        client = Http_client(tagname="HTTPGWP")
        client.post(url=url, jsondata=jsondata, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 201:
            assert client.jsonResponse["code"] == checkpoint["code"]

    @allure.testcase("4733,网段新增接口-校验请求字段为空&null ")
    @allure.testcase("4902, 网段新增接口-校验请求字段为空&null   ")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PostAddNetworkNull.json").dict_value_join())
    def test_Add_Network_Null(self, url, header, jsondata, checkpoint, clear_data):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :param clear_data:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.post(url=url, jsondata=jsondata, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 201:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]

    @allure.testcase("4734,网段新增接口-校验end_ip>start_ip ")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PostAddNetworkEndipBigStartip.json").dict_value_join())
    def test_Add_Network_End_ip_big_Start_ip(self, url, header, jsondata, checkpoint, clear_data):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :param clear_data:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.post(url=url, jsondata=jsondata, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 201:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]

    @pytest.fixture(scope="function")
    def add_network(self):
        CommonAccNetRestrictBoundPolicy().add_Network(name="张三专用", start_ip="192.168.1.1", end_ip="192.168.1.2",
                                                      host="10.2.176.245")
        CommonAccNetRestrictBoundPolicy().add_Network(name="lisi", ip_address="192.168.12.1", netmask="255.255.255.0",
                                                      net_type="ip_mask", host="10.2.176.245")

    @allure.testcase("4735, 网段新增接口-校验字段重复   ")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PostAddNetworkRepeat.json").dict_value_join())
    def test_Add_Network_repeat(self, url, header, jsondata, checkpoint, add_network, clear_data):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :param clear_data:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.post(url=url, jsondata=jsondata, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 201:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]

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

    @allure.testcase("4778, 网段新增接口-访问者网段绑定功能关闭 ")
    @pytest.mark.high
    def test_Add_Network_repeat(self, disabled_network_restriction):
        """

        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.post(url="/api/policy-management/v1/user-login/network-restriction/network",
                    jsondata={"name": "zhang", "start_ip": "10.2.189.56", "end_ip": "192.168.2.199", "ip_address": "",
                              "netmask": "255.255.252.0", "net_type": "ip_segment"},
                    header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.status_code == 403
        assert client.jsonResponse["code"] == 403013000
        assert client.jsonResponse["message"] == "No permission to do this operation."
        assert client.jsonResponse["cause"] == "Network restriction function is not enabled."

    @allure.testcase("4915, 网段新增接口-name不能为特殊字符")
    @pytest.mark.medium
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PostAddNetworkName_Special_Char.json").dict_value_join())
    def test_Add_Network_name_special_char(self, url, header, jsondata, checkpoint):
        """

        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.post(url=url, jsondata=jsondata, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 201:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]

    @allure.testcase("4916, 网段新增接口-校验字段start_ip不符合格式、范围 ")
    @pytest.mark.medium
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PostAddNetworkVerifyFormatRange.json").dict_value_join())
    def test_Add_Network_verify_format_range(self, url, header, jsondata, checkpoint, clear_data):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.post(url=url, jsondata=jsondata, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 201:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]

    @allure.issue(url="http://jira.aishu.cn/browse/ASP-7631", name="BUG ASP-7631, 【访问者网段白名单】保存相同网段时未报错")
    @pytest.mark.high
    def test_add_network_prefix_zero(self, add_network, clear_data):
        """
        测试添加前缀为零的用例
        :return:
        """
        res = CommonAccNetRestrictBoundPolicy().add_Network(name="cp张三专用", start_ip="192.168.01.01",
                                                            end_ip="192.168.01.02",
                                                            host="10.2.176.245")
        assert res[0] == 409
        assert res[1]["code"] == 409013000
        assert res[1]["message"] == "Conflict resource."
        assert res[1]["detail"] == {"conflict_params": ["start_ip", "end_ip"]}
        res2 = CommonAccNetRestrictBoundPolicy().add_Network(name="cplisi", ip_address="192.168.012.01",
                                                             netmask="255.255.255.0",
                                                             net_type="ip_mask", host="10.2.176.245")
        assert res2[0] == 409
        assert res2[1]["code"] == 409013000
        assert res2[1]["message"] == "Conflict resource."
        assert res2[1]["detail"] == {"conflict_params": ["ip_address", "netmask"]}
