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
@allure.feature("访问者列表查询接口")
class Test_GetAccessorList(object):
    """
     访问者列表查询接口
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

    @allure.step("创建用户")
    @pytest.fixture(scope="function")
    def create_user(self):
        list_user_id = []
        for index in range(21):
            user_id = CommonAccNetRestrictBoundPolicy().create_user(loginName="eisoo.com" + str(index))
            list_user_id.append(user_id)
        yield list_user_id
        for i in range(len(list_user_id)):
            CommonAccNetRestrictBoundPolicy().close_person_doc(user_id=list_user_id[i])
            CommonAccNetRestrictBoundPolicy().del_user(user_id=list_user_id[i])

    @allure.testcase("4784, 访问者列表查询接口-校验请求字段必填 ")
    @allure.testcase("4868, 访问者列表查询接口-校验请求字段必填")
    @allure.testcase("4785, 访问者列表查询接口-校验请求字段类型")
    @allure.testcase("4786, 访问者列表查询接口-校验请求字段为空&null")
    @allure.testcase("4788, 访问者列表查询接口-查询不存在的网段")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,split_url,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/GetAccessorListVerifyFiled.json").dict_value_join())
    def test_Get_accessor_List_verify_field(self, url, header, split_url, jsondata, checkpoint, add_network):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :param add_network:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        if split_url == "" or split_url is None:
            client.get(url=url, header=header)
        else:
            client.get(url=url + add_network[0] + split_url, header=header)

        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if checkpoint["status_code"] != 200:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]
        else:
            assert client.jsonResponse["count"] == checkpoint["count"]
            assert client.jsonResponse["data"] == checkpoint["data"]

    @allure.testcase("4787,访问者列表查询接口-校验请求字段边界值")
    @allure.testcase("4867,访问者列表查询接口-校验请求字段非法边界值")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,split_url,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/GetAccessorListByPage.json").dict_value_join())
    def test_Get_accessor_List_by_page(self, url, header, split_url, jsondata, checkpoint, add_network, create_user):
        """

        :param url:
        :param header:
        :param split_url:
        :param jsondata:
        :param checkpoint:
        :param add_network:
        :return:
        """
        jsonlist = []
        for index in range(len(create_user)):
            jsonlist.append({"accessor_id": create_user[index], "accessor_type": "user"})

        CommonAccNetRestrictBoundPolicy().add_accessor_network(network_id=add_network[0], jsondata=jsonlist)
        client = Http_client(tagname="HTTPGWP")
        if split_url == "" or split_url is None:
            client.get(url=url, header=header)
        else:
            client.get(url=url + add_network[0] + split_url, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if checkpoint["status_code"] != 200:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]
        else:
            assert client.jsonResponse["count"] == checkpoint["count"]
            assert len(client.jsonResponse["data"]) == checkpoint["len.data"]
        # if len(client.jsonResponse["data"]) > 0:
        #     accessor_name_list = []
        #     for i in range(len(client.jsonResponse["data"])):
        #         accessor_name_list.append(client.jsonResponse["data"][i]["accessor_name"])
        #     for index in range(len(client.jsonResponse["data"])):
        #         assert "eisoo.com" + str(20 - checkpoint["start"] - index) in accessor_name_list

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

    @allure.testcase("4867,访问者列表查询接口-查询成功")
    @pytest.mark.high
    def test_Get_accessor_disabled_network_restriction(self, add_network, disabled_network_restriction):
        """
        :param add_network:
        :param create_user:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[0] +
                "/accessor?key_word=&offset=0&limit=1000",
            header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.status_code == 200
        assert client.jsonResponse["count"] == 0

    @allure.testcase("keyword关键字搜索")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,split_url,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/GetAccessorListByKeyWord.json").dict_value_join())
    def test_Get_accessor_List_by_key_word(self, url, header, split_url, jsondata, checkpoint, add_network,
                                           create_user):
        """

        :param url:
        :param header:
        :param split_url:
        :param jsondata:
        :param checkpoint:
        :param add_network:
        :param create_user:
        :return:
        """
        jsonlist = []
        for index in range(len(create_user)):
            jsonlist.append({"accessor_id": create_user[index], "accessor_type": "user"})
        CommonAccNetRestrictBoundPolicy().add_accessor_network(network_id=add_network[0], jsondata=jsonlist)
        client = Http_client(tagname="HTTPGWP")
        if split_url == "" or split_url is None:
            client.get(url=url, header=header)
        else:
            client.get(url=url + add_network[0] + split_url, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        assert client.jsonResponse["count"] == checkpoint["count"]
        assert len(client.jsonResponse["data"]) == checkpoint["len.data"]

    @allure.testcase("访问者列表查询——所有网段,默认为空数组")
    @pytest.mark.high
    def test_Get_accessor_List_public_net(self):
        client = Http_client(tagname="HTTPGWP")
        client.get(
            url="/api/policy-management/v1/user-login/network-restriction/network/public-net/accessor?key_word"
                "=&offset=0&limit=1000",
            header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.status_code == 200
        assert client.jsonResponse["count"] == 0
        assert client.jsonResponse["data"] == []

    @allure.testcase("访问者列表查询——所有网段,绑定用户访问者")
    @pytest.mark.high
    def test_Get_accessor_List_public_net_bound_user(self, create_user):
        for user_id in create_user:
            CommonAccNetRestrictBoundPolicy.add_accessor_network(network_id="public-net",
                                                                 jsondata=[{"accessor_id": user_id,
                                                                            "accessor_type": "user"}])
        client = Http_client(tagname="HTTPGWP")
        client.get(
            url="/api/policy-management/v1/user-login/network-restriction/network/public-net/accessor?key_word"
                "=&offset=0&limit=20", header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.status_code == 200
        assert client.jsonResponse["count"] == 21
        assert len(client.jsonResponse["data"]) == 20
        assert "eisoo.com" in client.jsonResponse["data"][0]["accessor_name"]
        assert "eisoo.com" in client.jsonResponse["data"][19]["accessor_name"]

    @allure.testcase("10328,访问者列表查询接口-offset,limit默认值")
    @pytest.mark.high
    def test_Get_accessor_list_default(self, add_network, create_user):
        jsonlist = []
        for index in range(len(create_user)):
            jsonlist.append({"accessor_id": create_user[index], "accessor_type": "user"})
        CommonAccNetRestrictBoundPolicy().add_accessor_network(network_id=add_network[0], jsondata=jsonlist)
        # offset字段不传
        client = Http_client(tagname="HTTPGWP")
        client.get(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[0] +
                "/accessor?key_word=&limit=21",
            header={"Content-Type": "application/json"})
        assert client.status_code == 200
        assert len(client.jsonResponse["data"]) == 21
        assert client.jsonResponse["count"] == 21
        # print(client.jsonResponse)
        # limit字段不传
        client1 = Http_client(tagname="HTTPGWP")
        client1.get(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[0] +
                "/accessor?key_word=&offset=0",
            header={"Content-Type": "application/json"})
        assert client1.status_code == 200
        assert len(client1.jsonResponse["data"]) == 20
        assert client1.jsonResponse["count"] == 21
        # print(client1.jsonResponse)

        # offset和limit值不传
        client2 = Http_client(tagname="HTTPGWP")
        client2.get(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[0] +
                "/accessor?key_word=",
            header={"Content-Type": "application/json"})
        assert client2.status_code == 200
        assert len(client2.jsonResponse["data"]) == 20
        assert client2.jsonResponse["count"] == 21
        assert client2.jsonResponse["data"][0]["accessor_id"] == client.jsonResponse["data"][0]["accessor_id"]
        print(client2.jsonResponse)

    @allure.testcase("10327,访问者列表查询接口-limit边界值合法验证 ")
    @pytest.mark.high
    def test_Get_accessor_list_verify_limit(self, add_network, create_user):
        """

        :param add_network:
        :return:
        """
        jsonlist = []
        for index in range(len(create_user)):
            jsonlist.append({"accessor_id": create_user[index], "accessor_type": "user"})
        CommonAccNetRestrictBoundPolicy().add_accessor_network(network_id=add_network[0], jsondata=jsonlist)

        # limit输入0
        client0 = Http_client(tagname="HTTPGWP")
        client0.get(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[0] +
                "/accessor?key_word=&offset=0&limit==0",
            header={"Content-Type": "application/json"})
        assert client0.status_code == 400
        assert client0.jsonResponse["code"] == 400000000
        assert client0.jsonResponse["message"] == "Invalid request."
        assert client0.jsonResponse["cause"] == ""
        assert client0.jsonResponse["detail"] == {"invalid_params": ["limit"]}

        # limit输入1
        client1 = Http_client(tagname="HTTPGWP")
        client1.get(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[0] +
                "/accessor?key_word=&offset=0&limit=1",
            header={"Content-Type": "application/json"})
        assert client1.status_code == 200
        assert len(client1.jsonResponse["data"]) == 1
        assert client1.jsonResponse["count"] == 21
        # limit输入2
        client1_1 = Http_client(tagname="HTTPGWP")
        client1_1.get(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[0] +
                "/accessor?key_word=&offset=0&limit=2",
            header={"Content-Type": "application/json"})
        assert client1_1.status_code == 200
        assert len(client1_1.jsonResponse["data"]) == 2
        assert client1_1.jsonResponse["count"] == 21
        # limit输入-1
        client2 = Http_client(tagname="HTTPGWP")
        client2.get(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[0] +
                "/accessor?key_word=&offset=0&limit=-1",
            header={"Content-Type": "application/json"})
        assert client2.status_code == 400
        assert client2.jsonResponse["code"] == 400000000
        assert client2.jsonResponse["message"] == "Invalid request."
        assert client2.jsonResponse["cause"] == ""
        assert client2.jsonResponse["detail"] == {"invalid_params": ["limit"]}

        # limit输入1001
        client3 = Http_client(tagname="HTTPGWP")
        client3.get(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[0] +
                "/accessor?key_word=&offset=0&limit=1001",
            header={"Content-Type": "application/json"})
        assert client3.status_code == 400
        assert client3.jsonResponse["code"] == 400000000
        assert client3.jsonResponse["message"] == "Invalid request."
        assert client3.jsonResponse["cause"] == ""
        assert client3.jsonResponse["detail"] == {"invalid_params": ["limit"]}

        # limit输入1000
        client3 = Http_client(tagname="HTTPGWP")
        client3.get(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[0] +
                "/accessor?key_word=&offset=0&limit=1000",
            header={"Content-Type": "application/json"})
        assert client3.status_code == 200
        assert len(client3.jsonResponse["data"]) == 21
        assert client3.jsonResponse["count"] == 21

        # limit输入999 offset>20
        client3 = Http_client(tagname="HTTPGWP")
        client3.get(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[0] +
                "/accessor?key_word=&offset=21&limit=999",
            header={"Content-Type": "application/json"})
        assert client3.status_code == 200
        assert len(client3.jsonResponse["data"]) == 0
        assert client3.jsonResponse["count"] == 21

        # offset 输入-1
        client3 = Http_client(tagname="HTTPGWP")
        client3.get(
            url="/api/policy-management/v1/user-login/network-restriction/network/" + add_network[0] +
                "/accessor?key_word=&offset=-1&limit=999",
            header={"Content-Type": "application/json"})
        assert client3.status_code == 400
        assert client3.jsonResponse["code"] == 400000000
        assert client3.jsonResponse["message"] == "Invalid request."
        assert client3.jsonResponse["cause"] == ""
        assert client3.jsonResponse["detail"] == {"invalid_params": ["offset"]}
