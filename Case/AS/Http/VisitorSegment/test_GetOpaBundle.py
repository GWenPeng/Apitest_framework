# coding=utf-8
from flaky import flaky

from Common.readjson import JsonRead
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect
from .CommonVisitorSegment import CommonAccNetRestrictBoundPolicy
from Common.untar import untar
from Common.readjson import JsonRead
from Common.IpToInt import IpToInt, ipAndNetmaskToStartipEndip
import os
import pytest
import allure
import time
import json


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
@allure.feature("获取所有网段白名单")
@flaky(max_runs=3, min_passes=1)
class Test_GetOpaBundle(object):
    """
    获取所有网段白名单
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

    @pytest.fixture(scope="function")
    def clear_network(self):
        CommonAccNetRestrictBoundPolicy().clear_Network_list(host="10.2.176.245")

    @allure.testcase("6974, 获取所有网段白名单--访问者和网段为空-开启白名单")
    @pytest.mark.high
    def test_getOpaEmptyList(self, clear_network):
        """

        :return:
        """
        father_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = "opa.tar.gz"
        filePath = os.path.join(father_path, "VisitorSegment/testdata/")
        print(filePath)
        client = Http_client(tagname="HTTPGWP")
        time.sleep(3)
        client.get(url="/api/policy-management/v1/policy-data/bundle.tar.gz",
                   header={"Content-Type": "application/json"})
        assert client.status_code == 200
        try:
            s = open(filePath + filename, "wb")
            s.write(client.content)
            s.close()
        except Exception:
            raise
        untar(filePath + filename, filePath)
        js = JsonRead(datafile="AS/Http/VisitorSegment/testdata/network/data.json")
        data = js.load_dirt
        print(data)
        assert data["is_enabled"] is True
        assert data["users"] == {}
        assert data["departments"] == {}

    @allure.step("关闭访问者网段绑定功能开关")
    @pytest.fixture(scope="function")
    def disabled_network_restriction(self):
        client = Http_client(tagname="HTTPGWP")
        client.put(url="/api/policy-management/v1/general/network_restriction/value",
                   json=[{"name": "network_restriction", "value": {"is_enabled": False}}],
                   header='{"Content-Type":"application/json"}',
                   )
        assert client.status_code == 200
        time.sleep(3)
        yield
        client = Http_client(tagname="HTTPGWP")
        client.put(url="/api/policy-management/v1/general/network_restriction/value",
                   json=[{"name": "network_restriction", "value": {"is_enabled": True}}],
                   header='{"Content-Type":"application/json"}',
                   )
        assert client.status_code == 200

    @allure.testcase("6974, 获取所有网段白名单--访问者和网段为空-关闭白名单")
    @pytest.mark.high
    def test_getOpaEmptyList_disabled_network_restriction(self, clear_network, disabled_network_restriction):
        """
        BUG ASP-6883修改白名单策略状态为false时,获取到的所有白名单网段接口返回的data.json文件中is_enable为false
        :return:
        """
        father_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = "opa.tar.gz"
        filePath = os.path.join(father_path, "VisitorSegment/testdata/")
        print(filePath)
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/policy-management/v1/policy-data/bundle.tar.gz",
                   header={"Content-Type": "application/json"})
        assert client.status_code == 200
        try:
            s = open(filePath + filename, "wb")
            s.write(client.content)
            s.close()
        except Exception:
            raise
        untar(filePath + filename, filePath)
        js = JsonRead(datafile="AS/Http/VisitorSegment/testdata/network/data.json")
        data = js.load_dirt
        print(data)
        assert data["is_enabled"] is False

    @allure.step("创建多个用户")
    @pytest.fixture(scope="function", params=["1", "10"])
    def create_user(self, request):
        list_user_id = []
        for index in range(int(request.param)):
            user_id = CommonAccNetRestrictBoundPolicy().create_user(loginName="eisoo.com" + str(index))
            list_user_id.append(user_id)
        yield list_user_id
        for i in range(len(list_user_id)):
            CommonAccNetRestrictBoundPolicy().close_person_doc(user_id=list_user_id[i])
            CommonAccNetRestrictBoundPolicy().del_user(user_id=list_user_id[i])

    @allure.step("批量绑定访问者")
    @pytest.fixture(scope="function")
    def add_accessors(self, add_network, create_user):
        """
        批量绑定访问者，多用户测试1,50,200,500,1000
        :return:
        """
        jsonlist = []
        for index in range(len(create_user)):
            jsonlist.append({"accessor_id": create_user[index], "accessor_type": "user"})
        starttime = time.time()
        res = CommonAccNetRestrictBoundPolicy().add_accessor_network(network_id=add_network[0], jsondata=jsonlist)
        endtime = time.time()
        print((endtime - starttime) * 1000)
        print(res)
        time.sleep(3)
        return create_user

    @allure.testcase("获取所有白名单 获取opa_bundle.tar.gz")
    @pytest.mark.high
    def test_getOpaOneUser(self, add_accessors):
        """

        :return:
        """
        father_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = "opa.tar.gz"
        filePath = os.path.join(father_path, "VisitorSegment/testdata/")
        print(filePath)
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/policy-management/v1/policy-data/bundle.tar.gz",
                   header={"Content-Type": "application/json"})
        assert client.status_code == 200
        try:
            s = open(filePath + filename, "wb")
            s.write(client.content)
            s.close()
        except Exception:
            raise
        untar(filePath + filename, filePath)
        js = JsonRead(datafile="AS/Http/VisitorSegment/testdata/network/data.json")
        data = js.load_dirt
        print(data)
        # accessor_idlist = []
        # for inde in range(len(add_accessors)):
        #     accessor_idlist.append(data["accessors"][inde]["accessor_id"])
        assert data["is_enabled"] is True
        for index in range(len(add_accessors)):
            # assert add_accessors[index] in accessor_idlist
            assert data["users"][add_accessors[index]]["nets"][0]["start_ip"] == IpToInt("10.2.181.1")
            assert data["users"][add_accessors[index]]["nets"][0]["end_ip"] == IpToInt("10.2.181.255")

    @allure.step("新增多个访问者网段数据 10个")
    @pytest.fixture(scope="function")
    def add_network_more(self):
        """

        :return:
        """
        ip_netmask_list = []
        for index in range(5):
            ip_segment_uuid = CommonAccNetRestrictBoundPolicy().add_Network(host="10.2.176.245",
                                                                            name="zhang" + str(1 + index),
                                                                            start_ip="10.2.181." + str(1 + index),
                                                                            end_ip="10.2.181.255",
                                                                            net_type="ip_segment")
            ip_mask_uuid = CommonAccNetRestrictBoundPolicy().add_Network(host="10.2.176.245",
                                                                         name="zhangip_mask" + str(1 + index),
                                                                         start_ip="10.2.181.1",
                                                                         end_ip="10.2.181.255",
                                                                         ip_address="192.168.1." + str(23 + index)
                                                                         , netmask="255.255.255.0", net_type="ip_mask")
            ip_netmask_list.append(ip_segment_uuid)
            ip_netmask_list.append(ip_mask_uuid)

        yield ip_netmask_list
        CommonAccNetRestrictBoundPolicy().clear_Network_list(host="10.2.176.245")

    @allure.step("创建多个用户")
    @pytest.fixture(scope="function", params=["10"])
    def create_user_more(self, request):
        list_user_id = []
        for index in range(int(request.param)):
            user_id = CommonAccNetRestrictBoundPolicy().create_user(loginName="eisoo.com" + str(index))
            list_user_id.append(user_id)
        yield list_user_id
        for i in range(len(list_user_id)):
            CommonAccNetRestrictBoundPolicy().close_person_doc(user_id=list_user_id[i])
            CommonAccNetRestrictBoundPolicy().del_user(user_id=list_user_id[i])

    @allure.step("批量绑定访问者")
    @pytest.fixture(scope="function")
    def add_accessors_more(self, add_network_more, create_user_more):
        """
        :return:
        """
        jsonlist = []
        for index in range(len(create_user_more)):
            jsonlist.append({"accessor_id": create_user_more[index], "accessor_type": "user"})
        for index in range(len(add_network_more)):
            res = CommonAccNetRestrictBoundPolicy().add_accessor_network(network_id=add_network_more[index],
                                                                         jsondata=jsonlist)
            print(res)
        time.sleep(3)
        return create_user_more

    @allure.testcase("获取所有白名单 获取opa_bundle.tar.gz")
    @pytest.mark.high
    def test_getOpaTenUsers(self, add_accessors_more):
        """

        :return:
        """
        father_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = "opa.tar.gz"
        filePath = os.path.join(father_path, "VisitorSegment/testdata/")
        print(filePath)
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/policy-management/v1/policy-data/bundle.tar.gz",
                   header={"Content-Type": "application/json"})
        assert client.status_code == 200
        try:
            s = open(filePath + filename, "wb")
            s.write(client.content)
            s.close()
        except Exception:
            raise
        untar(filePath + filename, filePath)
        js = JsonRead(datafile="AS/Http/VisitorSegment/testdata/network/data.json")
        data = js.load_dirt
        # print(data)
        # accessor_idlist = []
        # for inde in range(len(add_accessors_more)):
        #     accessor_idlist.append(data["users"][][inde]["accessor_id"])
        assert data["is_enabled"] is True
        assert data["departments"] == {}
        for index in range(len(add_accessors_more)):
            # assert data["users"][add_accessors_more[index]]["nets"][index]
            # assert add_accessors_more[index] in accessor_idlist
            start_ip_list = []
            end_ip_list = []
            for i in range(len(data["users"][add_accessors_more[index]]["nets"])):
                start_ip_list.append(data["users"][add_accessors_more[index]]["nets"][i]["start_ip"])
                end_ip_list.append(data["users"][add_accessors_more[index]]["nets"][i]["end_ip"])

            for j in range(5):
                assert IpToInt("10.2.181." + str(1 + j)) in start_ip_list
                assert IpToInt("10.2.181.255") == end_ip_list[start_ip_list.index(IpToInt("10.2.181." + str(1 + j)))]
                st_ed_ip = ipAndNetmaskToStartipEndip(ip="192.168.1." + str(23 + j), netmask="255.255.255.0")
                assert IpToInt(st_ed_ip[0]) in start_ip_list
                assert IpToInt(st_ed_ip[1]) == end_ip_list[start_ip_list.index(IpToInt(st_ed_ip[0]))]

    @allure.step("创建部门用户")
    @pytest.fixture(scope="function", params=["1"])
    def create_department_user_more(self, request):
        list_user_id = []
        for index in range(int(request.param)):
            user_id = CommonAccNetRestrictBoundPolicy().create_user(loginName="eisoo.com" + str(index),
                                                                    departmentIds=["151bcb65-48ce-4b62-973f"
                                                                                   "-0bb6685f9cb8"])
            list_user_id.append(user_id)
        yield list_user_id
        # for i in range(len(list_user_id)):
        #     CommonAccNetRestrictBoundPolicy().close_person_doc(user_id=list_user_id[i])
        #     CommonAccNetRestrictBoundPolicy().del_user(user_id=list_user_id[i])

    @allure.step("批量绑定访问者")
    @pytest.fixture(scope="function")
    def add_accessors_department(self, add_network):
        """
        :return:
        """
        jsonlist = [{"accessor_id": "151bcb65-48ce-4b62-973f-0bb6685f9cb8", "accessor_type": "department"}]
        res = CommonAccNetRestrictBoundPolicy().add_accessor_network(network_id=add_network[0], jsondata=jsonlist)
        time.sleep(5)
        print(res)
        return add_network

    @allure.testcase("获取所有白名单,网段已绑定没有用户的部门;获取opa_bundle.tar.gz")
    @pytest.mark.high
    def test_getOpa_department_no_user(self, add_accessors_department):
        """

        :return:
        """
        data = self.GetOpaData()
        print(data)
        assert data["is_enabled"] is True
        assert data["users"] == {}
        assert data["departments"]["151bcb65-48ce-4b62-973f-0bb6685f9cb8"] == [
            {'start_ip': 167949569, 'end_ip': 167949823}]
        # user_id = CommonAccNetRestrictBoundPolicy().create_user(loginName="aishu.cn111",
        #                                                         departmentIds=["151bcb65-48ce-4b62-973f"
        #                                                                        "-0bb6685f9cb8"])

        # time.sleep(5)  # 一分钟内定时推送数据至nsq
        # data1 = self.GetOpaData()
        # print(data1)
        # try:
        #     assert data1["is_enabled"] is True
        #     assert data1["departments"] is not None  # 新增完用户更访问者绑定数据，推送至OPA，待设计
        #     assert data1["departments"]["accessors"][0]["accessor_id"] == user_id
        #     assert {"start_ip": IpToInt("10.2.181.1"), "end_ip": IpToInt("10.2.181.255")} in \
        #            data1["networks"]["accessors"][0]["net_segments"]
        # finally:
        #     CommonAccNetRestrictBoundPolicy().close_person_doc(user_id=user_id)
        #     CommonAccNetRestrictBoundPolicy().del_user(user_id=user_id)

    def GetOpaData(self):
        father_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = "opa.tar.gz"
        filePath = os.path.join(father_path, "VisitorSegment/testdata/")
        print(filePath)
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/policy-management/v1/policy-data/bundle.tar.gz",
                   header={"Content-Type": "application/json"})
        assert client.status_code == 200
        try:
            s = open(filePath + filename, "wb")
            s.write(client.content)
            s.close()
        except Exception:
            raise
        untar(filePath + filename, filePath)
        js = JsonRead(datafile="AS/Http/VisitorSegment/testdata/network/data.json")
        data = js.load_dirt
        # print(data)
        return data

    @allure.testcase("获取所有白名单,网段已绑定存在用户的部门;获取opa_bundle.tar.gz")
    @pytest.mark.high
    def test_getOpa_department_exist_user(self, create_department_user_more, add_accessors_department):
        """

        :param add_accessors_department:
        :param create_department_user_more:
        :return:
        """
        data = self.GetOpaData()
        assert data["is_enabled"] is True
        assert data["departments"]["151bcb65-48ce-4b62-973f-0bb6685f9cb8"] == [
            {"start_ip": 167949569, "end_ip": 167949823}]
        assert data["users"][create_department_user_more[0]]["departments"] == ['151bcb65-48ce-4b62-973f-0bb6685f9cb8']
        # 删除用户后断言，data.users=={}
        CommonAccNetRestrictBoundPolicy().close_person_doc(user_id=create_department_user_more[0])
        CommonAccNetRestrictBoundPolicy().del_user(user_id=create_department_user_more[0])
        time.sleep(3)
        data2 = self.GetOpaData()
        assert data2["is_enabled"] is True
        assert data2["departments"]["151bcb65-48ce-4b62-973f-0bb6685f9cb8"] == [
            {"start_ip": 167949569, "end_ip": 167949823}]
        assert data2["users"] == {}
