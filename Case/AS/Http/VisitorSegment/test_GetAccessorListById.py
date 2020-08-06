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
@allure.feature("通过访问者ID查询网段")
class Test_GetAccessorListById(object):
    """
     通过访问者ID查询网段
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
        for index in range(1):
            user_id = CommonAccNetRestrictBoundPolicy().create_user(loginName="eisoo.com" + str(index))
            list_user_id.append(user_id)
        yield list_user_id
        for i in range(len(list_user_id)):
            CommonAccNetRestrictBoundPolicy().close_person_doc(user_id=list_user_id[i])
            CommonAccNetRestrictBoundPolicy().del_user(user_id=list_user_id[i])

    @allure.testcase("通过访问者ID查询网段")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,split_url,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/GetAccessorListById200.json").dict_value_join())
    def test_get_accessor_List_by_user_department_id(self, url, header, split_url, jsondata, checkpoint, add_network,
                                                     create_user):
        """

        :param url:
        :param header:
        :param split_url:
        :param jsondata:
        :param checkpoint:
        :return:
        """
        jsonlist = []
        for index in range(len(create_user)):
            jsonlist.append({"accessor_id": create_user[index], "accessor_type": "user"})
            jsonlist.append({"accessor_id": "151bcb65-48ce-4b62-973f-0bb6685f9cb8", "accessor_type": "department"})
        CommonAccNetRestrictBoundPolicy().add_accessor_network(network_id=add_network[0], jsondata=jsonlist)
        client = Http_client(tagname="HTTPGWP")
        if split_url == "" or split_url is None:
            client.get(url=url, header=header)
        else:
            client.get(url=url + create_user[0] + split_url, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        assert client.jsonResponse["count"] == checkpoint["count"]
        assert len(client.jsonResponse["data"]) == checkpoint["len.data"]
        assert client.jsonResponse["data"][0]["end_ip"] == checkpoint["end_ip"]
        # assert client.jsonResponse["data"][0]["ip_address"] == checkpoint["ip_address"]
        assert client.jsonResponse["data"][0]["name"] == checkpoint["name"]
        assert client.jsonResponse["data"][0]["net_type"] == checkpoint["net_type"]
        # assert client.jsonResponse["data"][0]["netmask"] == checkpoint["netmask"]
        assert client.jsonResponse["data"][0]["start_ip"] == checkpoint["start_ip"]

    @allure.step("新增多个访问者网段数据")
    @pytest.fixture(scope="function")
    def add_network_more(self):
        """

        :return:
        """
        list_ip_mask_uuid = []
        for index in range(21):
            ip_mask_uuid = CommonAccNetRestrictBoundPolicy().add_Network(host="10.2.176.245", name="zhang" + str(index),
                                                                         start_ip="10.2.181." + str(index),
                                                                         end_ip="10.2.181." + str(50 + index),
                                                                         ip_address="192.168.1." + str(index)
                                                                         , netmask="255.255.255.0", net_type="ip_mask")
            list_ip_mask_uuid.append(ip_mask_uuid)

        yield list_ip_mask_uuid
        CommonAccNetRestrictBoundPolicy().clear_Network_list(host="10.2.176.245")

    @allure.testcase("查询访问者绑定的网段,绑定多个网段")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,split_url,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/GetAccessorListByIdMoreNetwork.json").dict_value_join())
    def test_get_accessor_List_by_id_more_network(self, url, header, split_url, jsondata, checkpoint, add_network_more,
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
        jsonlist.append({"accessor_id": "151bcb65-48ce-4b62-973f-0bb6685f9cb8", "accessor_type": "department"})
        for i in range(len(add_network_more)):
            CommonAccNetRestrictBoundPolicy().add_accessor_network(network_id=add_network_more[i], jsondata=jsonlist)

        client = Http_client(tagname="HTTPGWP")
        if split_url == "" or split_url is None:
            client.get(url=url, header=header)
        else:
            client.get(url=url + create_user[0] + split_url, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        assert client.jsonResponse["count"] == checkpoint["count"]
        assert len(client.jsonResponse["data"]) == checkpoint["len.data"]

    @allure.testcase("查询访问者绑定的网段,传入不存在的ID")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,split_url,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/GetAccessorListByIdNull.json").dict_value_join())
    def test_get_accessor_List_by_id_not_exist_id(self, url, header, split_url, jsondata, checkpoint):
        """
        ASP-7363  【访问者网段白名单策略绑定-AT】获取访问者已绑定的网段接口,查询不存在的accessor_id时返回200，应该返回404
        :param url:
        :param header:
        :param split_url:
        :param jsondata:
        :param checkpoint:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        if split_url == "" or split_url is None:
            client.get(url=url, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        assert client.jsonResponse == checkpoint["res"]

    @allure.step("清空访问者")
    @pytest.fixture(scope="function")
    def clear_accessor(self, create_user):
        yield create_user
        CommonAccNetRestrictBoundPolicy().clear_accessor()

    @allure.testcase("获取访问者绑定“所有网段”")
    @pytest.mark.high
    def test_get_accessor_List_by_id_public_net(self, clear_accessor):
        CommonAccNetRestrictBoundPolicy().add_accessor_network(
            network_id="public-net",
            jsondata=[{"accessor_id": "266c6a42-6131-4d62-8f39-853e7093701c", "accessor_type": "user"},
                      {"accessor_id": "151bcb65-48ce-4b62-973f-0bb6685f9cb8", "accessor_type": "department"}])
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/policy-management/v1/user-login/network-restriction/accessor/266c6a42-6131-4d62-8f39"
                       "-853e7093701c/network?offset=0&limit=1000",
                   header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.status_code == 200
        assert client.jsonResponse["count"] == 1
        assert client.jsonResponse["data"][0]["id"] == "public-net"
        # assert client.jsonResponse["data"][0]["end_ip"] == ""
        # assert client.jsonResponse["data"][0]["ip_address"] == ""
        # assert client.jsonResponse["data"][0]["name"] == ""
        assert client.jsonResponse["data"][0]["net_type"] == ""
        # assert client.jsonResponse["data"][0]["netmask"] == ""
        # assert client.jsonResponse["data"][0]["start_ip"] == ""

        client1 = Http_client(tagname="HTTPGWP")
        client1.get(url="/api/policy-management/v1/user-login/network-restriction/accessor/151bcb65-48ce-4b62-973f"
                        "-0bb6685f9cb8/network?offset=0&limit=1000",
                    header={"Content-Type": "application/json"})
        print(client1.jsonResponse)
        assert client1.status_code == 200
        assert client1.jsonResponse["count"] == 1
        assert client1.jsonResponse["data"][0]["id"] == "public-net"
        # assert client1.jsonResponse["data"][0]["end_ip"] == ""
        # assert client1.jsonResponse["data"][0]["ip_address"] == ""
        # assert client1.jsonResponse["data"][0]["name"] == ""
        assert client1.jsonResponse["data"][0]["net_type"] == ""
        # assert client1.jsonResponse["data"][0]["netmask"] == ""
        # assert client1.jsonResponse["data"][0]["start_ip"] == ""

    @allure.testcase("10358 获取访问者已绑定的网段列表接口-offset,limit默认值")
    @pytest.mark.high
    def test_get_network_List_by_accessor_default(self, add_network_more, create_user):
        """

        :return:
        """
        jsonlist = []
        for index in range(len(create_user)):
            jsonlist.append({"accessor_id": create_user[index], "accessor_type": "user"})
        jsonlist.append({"accessor_id": "151bcb65-48ce-4b62-973f-0bb6685f9cb8", "accessor_type": "department"})
        for i in range(len(add_network_more)):
            CommonAccNetRestrictBoundPolicy().add_accessor_network(network_id=add_network_more[i], jsondata=jsonlist)

        # offset字段不传
        client1 = Http_client(tagname="HTTPGWP")
        client1.get(
            url="/api/policy-management/v1/user-login/network-restriction/accessor/" + create_user[0] + "/network"
                                                                                                        "?limit=21",
            header={"Content-Type": "application/json"})
        print(client1.jsonResponse)
        assert client1.status_code == 200
        assert len(client1.jsonResponse["data"]) == 21
        assert client1.jsonResponse["count"] == 21
        assert client1.jsonResponse['data'][0]["name"] == "zhang20"

        # offset字段值为空
        client2 = Http_client(tagname="HTTPGWP")
        client2.get(
            url="/api/policy-management/v1/user-login/network-restriction/accessor/" + create_user[0] +
                "/network?limit=21&offset=",
            header={"Content-Type": "application/json"})
        print(client2.jsonResponse)
        assert client2.status_code == 200
        assert len(client2.jsonResponse["data"]) == 21
        assert client2.jsonResponse["count"] == 21
        assert client2.jsonResponse['data'][0]["name"] == "zhang20"

        # limit字段不传
        client3 = Http_client(tagname="HTTPGWP")
        client3.get(
            url="/api/policy-management/v1/user-login/network-restriction/accessor/" + create_user[0] +
                "/network?offset=0",
            header={"Content-Type": "application/json"})
        print(client3.jsonResponse)
        assert client3.status_code == 200
        assert len(client3.jsonResponse["data"]) == 20
        assert client3.jsonResponse["count"] == 21
        assert client3.jsonResponse['data'][0]["name"] == "zhang20"

        # limit字段值不传
        client4 = Http_client(tagname="HTTPGWP")
        client4.get(
            url="/api/policy-management/v1/user-login/network-restriction/accessor/" + create_user[0] +
                "/network?offset=0&limit=",
            header={"Content-Type": "application/json"})
        print(client4.jsonResponse)
        assert client4.status_code == 200
        assert len(client4.jsonResponse["data"]) == 20
        assert client4.jsonResponse["count"] == 21
        assert client4.jsonResponse['data'][0]["name"] == "zhang20"

        # offset和limit字段值不传
        client5 = Http_client(tagname="HTTPGWP")
        client5.get(
            url="/api/policy-management/v1/user-login/network-restriction/accessor/" + create_user[0] +
                "/network?offset=&limit=",
            header={"Content-Type": "application/json"})
        print(client5.jsonResponse)
        assert client5.status_code == 200
        assert len(client5.jsonResponse["data"]) == 20
        assert client5.jsonResponse["count"] == 21
        assert client5.jsonResponse['data'][0]["name"] == "zhang20"

        # offset和limit字段不传
        client6 = Http_client(tagname="HTTPGWP")
        client6.get(
            url="/api/policy-management/v1/user-login/network-restriction/accessor/" + create_user[0] +
                "/network",
            header={"Content-Type": "application/json"})
        print(client6.jsonResponse)
        assert client6.status_code == 200
        assert len(client6.jsonResponse["data"]) == 20
        assert client6.jsonResponse["count"] == 21
        assert client6.jsonResponse['data'][0]["name"] == "zhang20"

    @allure.testcase("10359 获取访问者已绑定的网段接口-limit边界值合法验证")
    @pytest.mark.high
    def test_get_network_List_by_accessor_verify_limit(self, add_network_more, create_user):
        """

        :param add_network_more:
        :param create_user:
        :return:
        """
        jsonlist = []
        for index in range(len(create_user)):
            jsonlist.append({"accessor_id": create_user[index], "accessor_type": "user"})
        jsonlist.append({"accessor_id": "151bcb65-48ce-4b62-973f-0bb6685f9cb8", "accessor_type": "department"})
        for i in range(len(add_network_more)):
            CommonAccNetRestrictBoundPolicy().add_accessor_network(network_id=add_network_more[i], jsondata=jsonlist)

        # limit输入0
        client0 = Http_client(tagname="HTTPGWP")
        client0.get(
            url="/api/policy-management/v1/user-login/network-restriction/accessor/" + create_user[0] +
                "/network?offset=0&limit=0",
            header={"Content-Type": "application/json"})
        print(client0.jsonResponse)
        assert client0.status_code == 400
        assert client0.jsonResponse["code"] == 400000000
        assert client0.jsonResponse["message"] == "Invalid request."
        assert client0.jsonResponse["cause"] == ""
        assert client0.jsonResponse["detail"] == {'invalid_params': ['limit']}

        # limit输入1
        client1 = Http_client(tagname="HTTPGWP")
        client1.get(
            url="/api/policy-management/v1/user-login/network-restriction/accessor/" + create_user[0] +
                "/network?offset=0&limit=1",
            header={"Content-Type": "application/json"})
        print(client1.jsonResponse)
        assert client1.status_code == 200
        assert len(client1.jsonResponse["data"]) == 1
        assert client1.jsonResponse["count"] == 21
        assert client1.jsonResponse['data'][0]["name"] == "zhang20"
        # limit输入1
        client2 = Http_client(tagname="HTTPGWP")
        client2.get(
            url="/api/policy-management/v1/user-login/network-restriction/accessor/" + create_user[0] +
                "/network?offset=0&limit=2",
            header={"Content-Type": "application/json"})
        print(client2.jsonResponse)
        assert client2.status_code == 200
        assert len(client2.jsonResponse["data"]) == 2
        assert client2.jsonResponse["count"] == 21
        assert client2.jsonResponse['data'][0]["name"] == "zhang20"

        # limit输入1000
        client3 = Http_client(tagname="HTTPGWP")
        client3.get(
            url="/api/policy-management/v1/user-login/network-restriction/accessor/" + create_user[0] +
                "/network?offset=0&limit=1000",
            header={"Content-Type": "application/json"})
        print(client3.jsonResponse)
        assert client3.status_code == 200
        assert len(client3.jsonResponse["data"]) == 21
        assert client3.jsonResponse["count"] == 21
        assert client3.jsonResponse['data'][0]["name"] == "zhang20"

        # limit输入999
        client4 = Http_client(tagname="HTTPGWP")
        client4.get(
            url="/api/policy-management/v1/user-login/network-restriction/accessor/" + create_user[0] +
                "/network?offset=0&limit=999",
            header={"Content-Type": "application/json"})
        print(client4.jsonResponse)
        assert client4.status_code == 200
        assert len(client4.jsonResponse["data"]) == 21
        assert client4.jsonResponse["count"] == 21
        assert client4.jsonResponse['data'][0]["name"] == "zhang20"

        # limit输入1001
        client5 = Http_client(tagname="HTTPGWP")
        client5.get(
            url="/api/policy-management/v1/user-login/network-restriction/accessor/" + create_user[0] +
                "/network?offset=0&limit=1001",
            header={"Content-Type": "application/json"})
        print(client5.jsonResponse)
        assert client5.status_code == 400
        assert client5.jsonResponse["code"] == 400000000
        assert client5.jsonResponse["message"] == "Invalid request."
        assert client5.jsonResponse["cause"] == ""
        assert client5.jsonResponse["detail"] == {'invalid_params': ['limit']}

        # offset=-1
        client6 = Http_client(tagname="HTTPGWP")
        client6.get(
            url="/api/policy-management/v1/user-login/network-restriction/accessor/" + create_user[0] +
                "/network?offset=-1&limit=999",
            header={"Content-Type": "application/json"})
        print(client6.jsonResponse)
        assert client6.status_code == 400
        assert client6.jsonResponse["code"] == 400000000
        assert client6.jsonResponse["message"] == "Invalid request."
        assert client6.jsonResponse["cause"] == ""
        assert client6.jsonResponse["detail"] == {'invalid_params': ['offset']}

        # offset=20
        client7 = Http_client(tagname="HTTPGWP")
        client7.get(
            url="/api/policy-management/v1/user-login/network-restriction/accessor/" + create_user[0] +
                "/network?offset=20&limit=999",
            header={"Content-Type": "application/json"})
        print(client7.jsonResponse)
        assert client7.status_code == 200
        assert len(client7.jsonResponse["data"]) == 1
        assert client7.jsonResponse["count"] == 21
        assert client7.jsonResponse['data'][0]["name"] == "zhang0"

        # offset=21
        client8 = Http_client(tagname="HTTPGWP")
        client8.get(
            url="/api/policy-management/v1/user-login/network-restriction/accessor/" + create_user[0] +
                "/network?offset=21&limit=999",
            header={"Content-Type": "application/json"})
        print(client8.jsonResponse)
        assert client8.status_code == 200
        assert len(client8.jsonResponse["data"]) == 0
        assert client8.jsonResponse["count"] == 21
