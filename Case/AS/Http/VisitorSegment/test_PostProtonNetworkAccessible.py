# coding=utf-8
from Common.http_request import Http_client
from .CommonVisitorSegment import CommonAccNetRestrictBoundPolicy
from Common.IpToInt import IpToInt, ipAndNetmaskToStartipEndip
from EThriftException.ttypes import ncTException
from flaky import flaky
import pytest
import allure
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
@allure.feature("OPA访问者网段获取决策结果")
@flaky(max_runs=3, min_passes=1)
class Test_GetOpaPolicyResult(object):
    """
    OPA访问者网段获取决策结果
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
        # ip_mask_uuid = CommonAccNetRestrictBoundPolicy().add_Network(host="10.2.176.245", name="zhangip_mask",
        #                                                              start_ip="10.2.181.1",
        #                                                              end_ip="10.2.181.255", ip_address="192.168.1.23"
        #                                                              , netmask="255.255.255.0", net_type="ip_mask")

        yield ip_segment_uuid
        CommonAccNetRestrictBoundPolicy().clear_Network_list(host="10.2.176.245")

    @allure.step("创建多个用户")
    @pytest.fixture(scope="function", params=["5"])
    def create_user(self, request):
        list_user_id = []
        for index in range(int(request.param)):
            user_id = CommonAccNetRestrictBoundPolicy().create_user(loginName="eisoo.com" + str(index))
            list_user_id.append(user_id)
        yield list_user_id
        for i in range(len(list_user_id)):
            CommonAccNetRestrictBoundPolicy().close_person_doc(user_id=list_user_id[i])
            CommonAccNetRestrictBoundPolicy().del_user(user_id=list_user_id[i])

    @allure.step("创建部门用户")
    @pytest.fixture(scope="function", params=[("3", "151bcb65-48ce-4b62-973f-0bb6685f9cb8")])
    def create_department_user(self, request):
        list_user_id = []
        for index in range(int(request.param[0])):
            user_id = CommonAccNetRestrictBoundPolicy().create_user(loginName="department.user" + str(index),
                                                                    departmentIds=[request.param[1]])
            list_user_id.append(user_id)
        yield list_user_id, request.param[1]
        for i in range(len(list_user_id)):
            CommonAccNetRestrictBoundPolicy().close_person_doc(user_id=list_user_id[i])
            CommonAccNetRestrictBoundPolicy().del_user(user_id=list_user_id[i])

    @allure.step("批量绑定访问者")
    @pytest.fixture(scope="function")
    def add_accessors(self, add_network, create_department_user, create_user):
        """
        批量绑定访问者，多用户测试1,50,200,500,1000
        :return:
        """
        jsonlist = []
        for index in range(len(create_user)):
            jsonlist.append({"accessor_id": create_user[index], "accessor_type": "user"})
        jsonlist.append({"accessor_id": create_department_user[1], "accessor_type": "department"})
        CommonAccNetRestrictBoundPolicy().add_accessor_network(network_id=add_network, jsondata=jsonlist)

        return create_user, create_department_user[0]

    @allure.step("OPA访问者网段策略决策结果")
    def test_opa_result(self, add_accessors):
        """

        :return:
        """
        time.sleep(10)
        client0 = Http_client(tagname="HTTPGWP")
        client0.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network/accessible",
                     jsondata={
                         "input": {"accessor_id": add_accessors[0][1], "ip": IpToInt("10.2.181.1")}},
                     header={"Content-Type": "application/json"})
        # print(client0.jsonResponse)
        assert client0.jsonResponse["result"] is True

        client1 = Http_client(tagname="HTTPGWP")
        client1.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network/accessible",
                     jsondata={
                         "input": {"accessor_id": add_accessors[0][1], "ip": IpToInt("10.2.181.2")}},
                     header={"Content-Type": "application/json"})
        # print(client1.jsonResponse)
        assert client1.jsonResponse["result"] is True

        client2 = Http_client(tagname="HTTPGWP")
        client2.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network/accessible",
                     jsondata={
                         "input": {"accessor_id": add_accessors[0][1], "ip": IpToInt("10.2.181.0")}},
                     header={"Content-Type": "application/json"})
        # print(client2.jsonResponse)
        assert client2.jsonResponse["result"] is False

        # 断言endip边界值10.2.181.255
        client_endip1 = Http_client(tagname="HTTPGWP")
        client_endip1.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network/accessible",
                           jsondata={
                               "input": {"accessor_id": add_accessors[0][1], "ip": IpToInt("10.2.181.255")}},
                           header={"Content-Type": "application/json"})
        # print(client_endip1.jsonResponse)
        assert client_endip1.jsonResponse["result"] is True

        client_endip2 = Http_client(tagname="HTTPGWP")
        client_endip2.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network/accessible",
                           jsondata={
                               "input": {"accessor_id": add_accessors[0][1], "ip": IpToInt("10.2.181.254")}},
                           header={"Content-Type": "application/json"})
        # print(client_endip2.jsonResponse)
        assert client_endip2.jsonResponse["result"] is True

        client_endip3 = Http_client(tagname="HTTPGWP")
        client_endip3.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network/accessible",
                           jsondata={
                               "input": {"accessor_id": add_accessors[0][1], "ip": IpToInt("10.2.182.0")}},
                           header={"Content-Type": "application/json"})
        # print(client_endip3.jsonResponse)
        assert client_endip3.jsonResponse["result"] is False

        # 断言部门用户startIP "10.2.181.1"
        client_department = Http_client(tagname="HTTPGWP")
        client_department.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network/accessible",
                               jsondata={
                                   "input": {"accessor_id": add_accessors[1][0], "ip": IpToInt("10.2.181.1")}},
                               header={"Content-Type": "application/json"})
        # print(client_department.jsonResponse)
        assert client_department.jsonResponse["result"] is True

        client_department1 = Http_client(tagname="HTTPGWP")
        client_department1.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network/accessible",
                                jsondata={
                                    "input": {"accessor_id": add_accessors[1][0], "ip": IpToInt("10.2.181.2")}},
                                header={"Content-Type": "application/json"})
        # print(client_department1.jsonResponse)
        assert client_department1.jsonResponse["result"] is True

        client_department2 = Http_client(tagname="HTTPGWP")
        client_department2.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network/accessible",
                                jsondata={
                                    "input": {"accessor_id": add_accessors[1][0], "ip": IpToInt("10.2.181.0")}},
                                header={"Content-Type": "application/json"})
        # print(client_department2.jsonResponse)
        assert client_department2.jsonResponse["result"] is False

        # 断言部门用户endip "10.2.181.255"
        client_department_endip = Http_client(tagname="HTTPGWP")
        client_department_endip.post(
            url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network/accessible",
            jsondata={
                "input": {"accessor_id": add_accessors[1][0], "ip": IpToInt("10.2.181.255")}},
            header={"Content-Type": "application/json"})
        # print(client_department_endip.jsonResponse)
        assert client_department_endip.jsonResponse["result"] is True

        client_department_endip1 = Http_client(tagname="HTTPGWP")
        client_department_endip1.post(
            url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network/accessible",
            jsondata={
                "input": {"accessor_id": add_accessors[1][0], "ip": IpToInt("10.2.181.254")}},
            header={"Content-Type": "application/json"})
        # print(client_department_endip1.jsonResponse)
        assert client_department_endip1.jsonResponse["result"] is True

        client_department_endip2 = Http_client(tagname="HTTPGWP")
        client_department_endip2.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network"
                                          "/accessible",
                                      jsondata={
                                          "input": {"accessor_id": add_accessors[1][0], "ip": IpToInt("10.2.182.0")}},
                                      header={"Content-Type": "application/json"})
        # print(client_department_endip2.jsonResponse)
        assert client_department_endip2.jsonResponse["result"] is False

    @allure.step("开关打开，未绑定的用户获取策略结果")
    def test_opa_result_not_bound_user(self):
        """

        :return:
        """
        time.sleep(3)
        client_no_bound_user = Http_client(tagname="HTTPGWP")
        client_no_bound_user.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network"
                                      "/accessible",
                                  jsondata={
                                      "input": {"accessor_id": "266c6a42-6131-4d62-8f39-853e7093701c",
                                                "ip": IpToInt("10.2.182.1")}},
                                  header={"Content-Type": "application/json"})
        print(client_no_bound_user.jsonResponse)
        assert client_no_bound_user.jsonResponse["result"] is False

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

    @allure.step("开关关闭，任何的用户获取策略结果")
    def test_opa_result_close_restriction_user(self, disabled_network_restriction):
        """

        :return:
        """
        time.sleep(3)
        client = Http_client(tagname="HTTPGWP")
        client.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network"
                        "/accessible",
                    jsondata={
                        "input": {"accessor_id": "266c6a42-6131-4d62-8f39-853e7093701c",
                                  "ip": IpToInt("10.2.182.1")}},
                    header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.jsonResponse["result"] is True

    @allure.step("不存在的用户获取策略结果")
    def test_opa_result_not_exist_user(self):
        """

        :return:
        """
        time.sleep(3)
        client = Http_client(tagname="HTTPGWP")
        client.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network"
                        "/accessible",
                    jsondata={
                        "input": {"accessor_id": "c27a33b4-a95e-11ea-aa13f-005056825c8b",
                                  "ip": IpToInt("10.2.182.1")}},
                    header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.jsonResponse["result"] is False

    @allure.step("网段绑定部门访问者")
    @pytest.fixture(scope="function")
    def net_bound_accessor_department(self, add_network):
        departmentID = CommonAccNetRestrictBoundPolicy.CreateDepartment()
        userID = CommonAccNetRestrictBoundPolicy().create_user(loginName="userUser", departmentIds=[departmentID])
        CommonAccNetRestrictBoundPolicy.add_accessor_network(network_id=add_network,
                                                             jsondata=[{"accessor_id": departmentID,
                                                                        "accessor_type": "department"}])
        yield userID, departmentID
        try:
            CommonAccNetRestrictBoundPolicy.close_person_doc(user_id=userID)
            CommonAccNetRestrictBoundPolicy().del_user(user_id=userID)
        except ncTException as e:
            print("用户已在用例中删除", e)
        try:
            CommonAccNetRestrictBoundPolicy().DeleteDepartment(depart_id=departmentID)
        except ncTException as e:
            print("部门已在用例中删除", e)

    @allure.testcase("10528,删除部门引擎用nsq同步数据至policy")
    def test_opa_result_del_department(self, net_bound_accessor_department):
        """

        :return:
        """
        time.sleep(5)
        client = Http_client(tagname="HTTPGWP")
        client.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network"
                        "/accessible",
                    jsondata={
                        "input": {"accessor_id": net_bound_accessor_department[0],
                                  "ip": IpToInt("10.2.181.1")}},
                    header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.jsonResponse["result"] is True

        client.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network"
                        "/accessible",
                    jsondata={
                        "input": {"accessor_id": net_bound_accessor_department[0],
                                  "ip": IpToInt("10.2.181.255")}},
                    header={"Content-Type": "application/json"})
        assert client.jsonResponse["result"] is True
        CommonAccNetRestrictBoundPolicy().DeleteDepartment(depart_id=net_bound_accessor_department[1])
        # 删除部门，断言决策结果为false

        time.sleep(3)
        client1 = Http_client(tagname="HTTPGWP")
        client1.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network"
                         "/accessible",
                     jsondata={
                         "input": {"accessor_id": net_bound_accessor_department[0],
                                   "ip": IpToInt("10.2.181.1")}},
                     header={"Content-Type": "application/json"})
        print(client1.jsonResponse)
        assert client1.jsonResponse["result"] is False

        client1.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network"
                         "/accessible",
                     jsondata={
                         "input": {"accessor_id": net_bound_accessor_department[0],
                                   "ip": IpToInt("10.2.181.255")}},
                     header={"Content-Type": "application/json"})
        assert client1.jsonResponse["result"] is False

    @allure.testcase("10529,删除用户引擎用nsq同步数据至policy")
    def test_opa_result_del_user(self, net_bound_accessor_department):
        """

        :return:
        """
        time.sleep(5)
        client = Http_client(tagname="HTTPGWP")
        client.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network"
                        "/accessible",
                    jsondata={
                        "input": {"accessor_id": net_bound_accessor_department[0],
                                  "ip": IpToInt("10.2.181.1")}},
                    header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.jsonResponse["result"] is True

        client.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network"
                        "/accessible",
                    jsondata={
                        "input": {"accessor_id": net_bound_accessor_department[0],
                                  "ip": IpToInt("10.2.181.255")}},
                    header={"Content-Type": "application/json"})
        assert client.jsonResponse["result"] is True
        allure.step("#关闭个人文档")
        CommonAccNetRestrictBoundPolicy().close_person_doc(user_id=net_bound_accessor_department[0])  # 关闭个人文档
        allure.step("#删除用户")
        CommonAccNetRestrictBoundPolicy().del_user(user_id=net_bound_accessor_department[0])  # 删除用户
        time.sleep(8)
        client1 = Http_client(tagname="HTTPGWP")
        client1.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network"
                         "/accessible",
                     jsondata={
                         "input": {"accessor_id": net_bound_accessor_department[0],
                                   "ip": IpToInt("10.2.181.1")}},
                     header={"Content-Type": "application/json"})
        print(client1.jsonResponse)
        assert client1.jsonResponse["result"] is False

        client1.post(url="http://10.2.176.245:9080/api/proton-policy-engine/v1/query/network"
                         "/accessible",
                     jsondata={
                         "input": {"accessor_id": net_bound_accessor_department[0],
                                   "ip": IpToInt("10.2.181.255")}},
                     header={"Content-Type": "application/json"})
        assert client1.jsonResponse["result"] is False
