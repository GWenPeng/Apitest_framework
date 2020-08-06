# coding=utf-8
import pytest
import allure
from Common.readjson import JsonRead
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect
from .CommonVisitorSegment import CommonAccNetRestrictBoundPolicy
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
@allure.feature("访问者新增接口")
class Test_PostAddAccessor(object):
    """
     访问者新增接口
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
        user_id = CommonAccNetRestrictBoundPolicy().create_user(loginName="eisoo.com")
        yield user_id
        CommonAccNetRestrictBoundPolicy().close_person_doc(user_id=user_id)
        CommonAccNetRestrictBoundPolicy().del_user(user_id=user_id)

    @allure.testcase("4796, 访问者新增接口-校验请求字段必填")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PostAddAccessorVerifyFiled.json").dict_value_join())
    def test_add_accessor_verify_field(self, url, header, jsondata, checkpoint, add_network, create_user):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :param add_network:
        :return:
        """
        if "accessor_id" in jsondata[0]:
            jsondata[0]["accessor_id"] = create_user
        client = Http_client(tagname="HTTPGWP")
        if "accessor" in url:
            client.post(url=url, jsondata=jsondata, header=header)
        else:
            client.post(url=url + add_network[0] + "/accessor", jsondata=jsondata, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 201 and client.status_code != 404:
            assert client.jsonResponse[0]["id"] == checkpoint["id"]
            assert client.jsonResponse[0]["status"] == checkpoint["status"]
            assert client.jsonResponse[0]["body"]["code"] == checkpoint["code"]
            assert client.jsonResponse[0]["body"]["message"] == checkpoint["message"]
            assert client.jsonResponse[0]["body"]["cause"] == checkpoint["cause"]
            assert client.jsonResponse[0]["body"]["detail"] == checkpoint["detail"]

    @allure.testcase("4797, 访问者新增接口-校验请求字段类型")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PostAddAccessorVerifyType.json").dict_value_join())
    def test_add_accessor_verify_type(self, url, header, jsondata, checkpoint, add_network, create_user):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        if jsondata[0]["accessor_id"] == "add":
            jsondata[0]["accessor_id"] = create_user
        if "accessor" in url:
            client.post(url=url, jsondata=jsondata, header=header)
        else:
            client.post(url=url + add_network[0] + "/accessor", jsondata=jsondata, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 201:
            assert client.jsonResponse[0]["id"] == checkpoint["id"]
            assert client.jsonResponse[0]["status"] == checkpoint["status"]
            assert client.jsonResponse[0]["body"]["code"] == checkpoint["code"]
            assert client.jsonResponse[0]["body"]["message"] == checkpoint["message"]
            assert client.jsonResponse[0]["body"]["cause"] == checkpoint["cause"]
            assert client.jsonResponse[0]["body"]["detail"] == checkpoint["detail"]

    @allure.testcase("4798,访问者新增接口-校验请求字段为空&null")
    @allure.testcase("4799,访问者新增接口-传入不符合要求的字段值")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PostAddAccessorEmptyNull.json").dict_value_join())
    def test_add_accessor_empty_null(self, url, header, jsondata, checkpoint, add_network, create_user):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :param add_network:
        :param create_user:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        if jsondata[0]["accessor_id"] == "add":
            jsondata[0]["accessor_id"] = create_user
        if "accessor" in url:
            client.post(url=url, jsondata=jsondata, header=header)
        else:
            client.post(url=url + add_network[0] + "/accessor", jsondata=jsondata, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        assert client.jsonResponse[0]["status"] == checkpoint["status"]
        assert client.jsonResponse[0]["body"]["code"] == checkpoint["body.code"]
        assert client.jsonResponse[0]["body"]["message"] == checkpoint["message"]
        assert client.jsonResponse[0]["body"]["cause"] == checkpoint["cause"]
        assert client.jsonResponse[0]["body"]["detail"] == checkpoint["detail"]

    @allure.testcase("4800,访问者新增接口-新增失败")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PostAddAccessorNotExist.json").dict_value_join())
    def test_add_accessor_not_exist(self, url, header, jsondata, checkpoint, add_network, create_user):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :param add_network:
        :param create_user:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        if jsondata[0]["accessor_id"] == "add":
            jsondata[0]["accessor_id"] = create_user
        if "accessor" in url:
            client.post(url=url, jsondata=jsondata, header=header)
        else:
            client.post(url=url + add_network[0] + "/accessor", jsondata=jsondata, header=header)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code != 207:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]
        else:
            assert client.jsonResponse[0]["status"] == checkpoint["status"]
            assert client.jsonResponse[0]["body"]["code"] == checkpoint["body.code"]
            assert client.jsonResponse[0]["body"]["message"] == checkpoint["message"]
            assert client.jsonResponse[0]["body"]["cause"] == checkpoint["cause"]
            assert client.jsonResponse[0]["body"]["detail"] == checkpoint["detail"]

    @allure.step("清空访问者网段")
    @pytest.fixture(scope="function")
    def clear_accessor_data(self):
        yield
        CommonAccNetRestrictBoundPolicy().clear_accessor_list()

    @allure.testcase("4801,访问者新增接口-新增成功")
    @pytest.mark.high
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/VisitorSegment/testdata/PostAddAccessorSuccess.json").dict_value_join())
    def test_add_accessor_success(self, url, header, jsondata, checkpoint, add_network, clear_accessor_data):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :param add_network:
        :param create_user:
        :return:
        """
        res = CommonAccNetRestrictBoundPolicy().add_accessor_network(network_id=add_network[0], jsondata=jsondata)
        print(res)
        for i in range(len(res)):
            assert res[i]["id"] == checkpoint["id." + str(i)]
            assert res[i]["status"] == checkpoint["status." + str(i)]
            assert res[i]["body"] == checkpoint["body." + str(i)]

    @allure.testcase("4801,访问者新增接口-新增成功")
    @pytest.mark.high
    def test_add_accessor_repeat(self, add_network):
        CommonAccNetRestrictBoundPolicy().add_accessor_network(network_id=add_network[0],
                                                               jsondata=[{
                                                                   "accessor_id": "266c6a42-6131-4d62-8f39-853e7093701c",
                                                                   "accessor_type": "user"}])
        db = DB_connect(host="10.2.176.245")
        result = db.select_all(
            "SELECT * from policy_mgnt.t_network_accessor_relation where f_network_id=\"" + add_network[0] + "\"")
        db.close()
        assert len(result) == 1
        CommonAccNetRestrictBoundPolicy().add_accessor_network(network_id=add_network[0],
                                                               jsondata=[{
                                                                   "accessor_id": "266c6a42-6131-4d62-8f39-853e7093701c",
                                                                   "accessor_type": "user"}])
        db1 = DB_connect(host="10.2.176.245")
        result1 = db1.select_all(
            "SELECT * from policy_mgnt.t_network_accessor_relation where f_network_id=\"" + add_network[0] + "\"")
        db1.close()
        assert len(result1) == 1

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

    @allure.testcase("4802,访问者新增接口-访问者网段绑定功能关闭")
    @pytest.mark.high
    def test_add_accessor_disabled_network_restriction(self, add_network, disabled_network_restriction):
        """

        :param add_network:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.post(
            url="/api/policy-management/v1/user-login/network-restriction/network/176d85ce-3f22-437a-80a1"
                "-0e018c22c3b2/accessor",
            jsondata=[{"accessor_id": "266c6a42-6131-4d62-8f39-8533e7093701c", "accessor_type": "department"}],
            header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.status_code == 207
        assert client.jsonResponse[0]["id"] == ""
        assert client.jsonResponse[0]["status"] == 403
        assert client.jsonResponse[0]["body"] == {'code': 403013000, 'message': 'No permission to do this operation.',
                                                  'cause': 'Network restriction function is not enabled.'}

    @allure.step("创建多个用户")
    @pytest.fixture(scope="function")
    def create_user_n_more(self):
        list_user_id = []
        for index in range(1000):
            user_id = CommonAccNetRestrictBoundPolicy().create_user(loginName="eisoo.com" + str(index))
            list_user_id.append(user_id)
        yield list_user_id
        for i in range(len(list_user_id)):
            CommonAccNetRestrictBoundPolicy().close_person_doc(user_id=list_user_id[i])
            CommonAccNetRestrictBoundPolicy().del_user(user_id=list_user_id[i])

    @allure.step("清空访问者")
    @pytest.fixture(scope="function")
    def clear_accessor(self, create_user):
        yield create_user
        CommonAccNetRestrictBoundPolicy().clear_accessor()

    @allure.testcase(" 访问者新增接口-所有网段绑定访问者")
    @pytest.mark.high
    def test_add_accessor_public_net(self, clear_accessor):
        res = CommonAccNetRestrictBoundPolicy().add_accessor_network(
            network_id="public-net",
            jsondata=[{"accessor_id": "266c6a42-6131-4d62-8f39-853e7093701c", "accessor_type": "user"},
                      {"accessor_id": "151bcb65-48ce-4b62-973f-0bb6685f9cb8", "accessor_type": "department"},
                      {"accessor_id": clear_accessor, "accessor_type": "user"}])
        print(res)
        assert len(res) == 3
        assert res[0]["id"] == "266c6a42-6131-4d62-8f39-853e7093701c"
        assert res[0]["status"] == 201
        assert res[0]["body"] == {'accessor_id': '266c6a42-6131-4d62-8f39-853e7093701c', 'accessor_name': 'admin',
                                  'accessor_type': 'user'}
        assert res[1]["id"] == "151bcb65-48ce-4b62-973f-0bb6685f9cb8"
        assert res[1]["status"] == 201
        assert res[1]["body"] == {'accessor_id': '151bcb65-48ce-4b62-973f-0bb6685f9cb8', 'accessor_name': '组织结构',
                                  'accessor_type': 'department'}
        assert res[2]["id"] == clear_accessor
        assert res[2]["status"] == 201
        assert res[2]["body"] == {'accessor_id': clear_accessor, 'accessor_name': 'eisoo.com', 'accessor_type': 'user'}

    # def test_add_accessor_time(self, add_network, create_user_n_more):
    #     """
    #     批量绑定访问者，多用户性能测试1,50,200,500,1000
    #     :return:
    #     """
    #     jsonlist = []
    #     for index in range(len(create_user_n_more)):
    #         jsonlist.append({"accessor_id": create_user_n_more[index], "accessor_type": "user"})
    #     starttime = time.time()
    #     res = CommonAccNetRestrictBoundPolicy().add_accessor_network(network_id=add_network[0], jsondata=jsonlist)
    #     endtime = time.time()
    #     print((endtime - starttime)*1000)
    #     print(res)
