import allure
from Common.http_request import Http_client
from Common.thrift_client import Thrift_client
from ShareMgnt import ttypes
from EFAST import ncTEFAST
from ShareMgnt import ncTShareMgnt
from DB_connect.mysqlconnect import DB_connect
import time


class CommonAccNetRestrictBoundPolicy(object):
    @allure.step("删除网段")
    def del_Network(self, network_id, host="10.2.176.245"):
        """

        :param network_id:
        :param host:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.delete(
            url="https://" + host + "/api/policy-management/v1/user-login/network-restriction/network/" + network_id,
            header='{"Content-Type":"application/json"}')
        assert client.status_code == 200

    @allure.step("新增网段")
    def add_Network(self, name=None, start_ip=None, end_ip=None, ip_address=None, netmask=None, net_type="ip_segment",
                    host="10.2.176.245"):
        client = Http_client(tagname="HTTPGWP")
        if net_type == "ip_segment":
            client.post(url="https://" + host + "/api/policy-management/v1/user-login/network-restriction/network",
                        jsondata={"name": name, "start_ip": start_ip, "end_ip": end_ip, "net_type": net_type},
                        header='{"Content-Type":"application/json"}')
        elif net_type == "ip_mask":
            client.post(url="https://" + host + "/api/policy-management/v1/user-login/network-restriction/network",
                        jsondata={"name": name, "ip_address": ip_address, "netmask": netmask, "net_type": net_type},
                        header='{"Content-Type":"application/json"}')
        print(client.status_code)
        print(client.jsonResponse)
        if client.status_code == 201:
            assert client.status_code == 201
            return client.respheaders["Location"].split("/")[-1]
        else:
            return client.status_code, client.jsonResponse

    @allure.step("网段列表查询")
    def get_Network_list(self, host="10.2.176.245", offset=0, limit=1000, key_word=""):
        """

        :param offset:
        :param host:
        :param limit:
        :param key_word:
        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(url="https://" + host + "/api/policy-management/v1/user-login/network-restriction/network",
                   params={"offset": offset, "limit": limit, "key_word": key_word},
                   header={"Content-Type": "application/json"})
        return client.jsonResponse

    @allure.step("清空网段列表")
    def clear_Network_list(self, host=None):
        """

        :param host:
        :return:
        """
        if host is None:
            host = ["10.2.176.245"]
        if isinstance(host, str):
            host = [host]
        for Host in host:
            L = self.get_Network_list(host=Host)
            if isinstance(L, int):
                print(L)
            elif L["data"] is not None and len(L["data"]) > 1:
                for index in range(len(L["data"]) - 1):
                    self.del_Network(host=Host, network_id=L["data"][index + 1]["id"])
        return None

    @allure.step("获取网段信息详情")
    def get_network_info(self, uuid, host="10.2.176.245"):
        """

        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.get(url="https://" + host + "/api/policy-management/v1/user-login/network-restriction/network/" + uuid,
                   header={"Content-Type": "application/json"})
        assert client.status_code == 200
        return client.jsonResponse

    @staticmethod
    @allure.step("新增访问者网段")
    def add_accessor_network(network_id=None, jsondata=None, host="10.2.176.245"):
        """

        :return:
        """
        if jsondata is None:
            jsondata = [{"accessor_id": "266c6a42-6131-4d62-8f39-8533e7093701c", "accessor_type": "user"}]
        client = Http_client(tagname="HTTPGWP")
        client.post(
            url="https://" + host + "/api/policy-management/v1/user-login/network-restriction/network/" + network_id + "/accessor",
            header={"Content-Type": "application/json"},
            jsondata=jsondata
        )
        print(client.status_code)
        assert client.status_code == 207
        return client.jsonResponse

    @allure.step("获取访问者列表")
    def get_accessor_list(self, network_id="public-net", host="10.2.176.245", offset=0, limit=1000, key_word=""):
        client = Http_client(tagname="HTTPGWP")
        client.get(
            url="https://" + host + "/api/policy-management/v1/user-login/network-restriction/network/" + network_id +
                "/accessor",
            params={"offset": offset, "limit": limit, "key_word": key_word},
            header={"Content-Type": "application/json"})
        assert client.status_code == 200
        return client.jsonResponse

    @allure.step("删除访问者网段")
    def del_accessor_network(self, network_id=None, accessor_id=None, host="10.2.176.245"):
        """

        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.delete(
            url="https://" + host + "/api/policy-management/v1/user-login/network-restriction/network/" + network_id + "/accessor/" + accessor_id,
            header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.status_code == 207
        return client.jsonResponse

    @allure.step("删除访问者通过访问者id删除")
    def del_accessor(self, accessor_id=None, host="10.2.176.245"):
        """

        :return:
        """
        client = Http_client(tagname="HTTPGWP")
        client.delete(
            url="https://" + host + "/api/policy-management/v1/user-login/network-restriction/network/public-net/accessor/" + accessor_id,
            header={"Content-Type": "application/json"})
        print(client.jsonResponse)
        assert client.status_code == 207
        return client.jsonResponse

    @allure.step("根据网段ID清空访问者")
    def clear_accessor(self, network_id="public-net", host="10.2.176.245"):
        """

        :param network_id:
        :param host:
        :return:
        """
        if host is None:
            host = ["10.2.176.245"]
        if isinstance(host, str):
            host = [host]
        for Host in host:
            L = self.get_accessor_list(network_id=network_id, host=Host)
            if isinstance(L, int):
                print(L)
            elif L["data"] is not None and len(L["data"]) > 0:
                for index in range(len(L["data"])):
                    self.del_accessor(host=Host, accessor_id=L["data"][index]["accessor_id"])
        return None

    @allure.step("清空访问者列表")
    def clear_accessor_list(self, host="10.2.176.245"):
        DB_connect(host=host).delete("DELETE from policy_mgnt.t_network_accessor_relation ")

    @allure.step("创建用户user")
    def create_user(self, responsiblePersonId="266c6a42-6131-4d62-8f39-853e7093701c", host="10.2.176.245",
                    loginName="user1",
                    departmentIds=None, pwdControl=False, password="eisoo.com"):
        """
        :param password:
        :param pwdControl:
        :param departmentIds:
        :param loginName:
        :param host:
        :param responsiblePersonId:
        :param n: 访问者个数
        :return:
        """
        if departmentIds is None:
            departmentIds = ["-1"]
        UserInfo = ttypes.ncTUsrmAddUserInfo(
            user=ttypes.ncTUsrmUserInfo(loginName=loginName, departmentIds=departmentIds, pwdControl=pwdControl),
            password=password)
        tc = Thrift_client(host=host)
        user_id = tc.client.Usrm_AddUser(user=UserInfo, responsiblePersonId=responsiblePersonId)
        tc.close()
        return user_id

    @allure.step("删除用户")
    def del_user(self, user_id, host="10.2.176.245"):
        """

        :param host:
        :param user_id:
        :return:
        """
        tc = Thrift_client(host=host)
        tc.client.Usrm_DelUser(userId=user_id)
        tc.close()

    @staticmethod
    @allure.step("关闭个人文档")
    def close_person_doc(user_id="0d7194e0-9035-11ea-b57b-00505682e19f", host="10.2.176.245"):
        """
        EACP_DeleteUserDoc
        :return:
        """
        tc = Thrift_client(host=host, service=ncTEFAST, port=9121)
        tc.client.EFAST_DeleteUserDoc(userId=user_id, deleterId=None)
        tc.close()

    @allure.step("创建部门")
    def create_department(self, host="10.2.176.245", department_name="部门名称",
                          parentId="151bcb65-48ce-4b62-973f-0bb6685f9cb8", siteId=None, priority=None, email=None, ):
        """

        :return:
        """
        addparam = ttypes.ncTAddDepartParam(departName=department_name, parentId=parentId, siteId=siteId,
                                            priority=priority, email=email, )
        tc = Thrift_client(host=host)
        department_id = tc.client.Usrm_AddDepartment(addParam=addparam)
        tc.close()
        return department_id

    @allure.step("创建子部门")
    def create_child_department(self, n=1, f_department_name="父部门", start_child_name="子部门名称", host="10.2.176.245"):
        parent_id = self.create_department(host=host, department_name=f_department_name)
        child_department_id_list = []
        for index in range(n):
            child_department_id = self.create_department(host=host, department_name=start_child_name + str(index),
                                                         parentId=parent_id)
            parent_id = child_department_id
            child_department_id_list.append(child_department_id)
        return child_department_id_list

    @allure.step("创建多子部门，多用户")
    def create_Users_departments(self, n=1, users_number=1, level=3, start_f_department_name="父部门",
                                 start_child_name="子部门名称",
                                 host="10.2.176.245", start_user="user",
                                 responsiblePersonId="266c6a42-6131-4d62-8f39-853e7093701c"):
        """

        :param responsiblePersonId:
        :param start_user: 起始用户名称
        :param level: 创建的子部门数
        :param users_number: 创建的用户数
        :param start_f_department_name:起始父部门名称
        :param n:创建的父部门数
        :param start_child_name:起始子部门名称
        :param host:
        :return:
        """
        for index in range(n):
            depids = self.create_child_department(f_department_name=start_f_department_name + str(index), n=level,
                                                  start_child_name="父" + str(index) + start_child_name, host=host)
            for number in range(users_number):
                print(depids[-1])
                self.create_user(responsiblePersonId=responsiblePersonId, host=host,
                                 loginName="father" + str(index) + start_user + str(number),
                                 departmentIds=[depids[-1]])
        return None

    @staticmethod
    def create_many_user(n=2000, host="10.2.176.245", departmentIds=None):
        if departmentIds is None:
            departmentIds = ["151bcb65-48ce-4b62-973f-0bb6685f9cb8"]
        for index in range(n):
            CommonAccNetRestrictBoundPolicy().create_user(responsiblePersonId="266c6a42-6131-4d62-8f39-853e7093701c",
                                                          host=host,
                                                          loginName="username" + str(index),
                                                          departmentIds=departmentIds, pwdControl=False,
                                                          password="eisoo.com")

    def Get_userinfo(self):
        tc = Thrift_client(host="10.2.176.245")
        info = tc.client.Usrm_GetUserInfo(userId="000f65ea-aafa-11ea-ac6b-005056825c8b")
        print(info)

    @staticmethod
    def Usrm_GetDepartmentofusers():  # 测试部门接口性能
        tc = Thrift_client(host="10.2.176.245")
        starttime1 = time.time()
        deplist1 = tc.client.Usrm_GetDepartmentOfUsers(departmentId="b0458cd4-b0a7-11ea-b68d-005056825c8b", start=0,
                                                       limit=-1)
        t1 = time.time() - starttime1
        print("policy部门耗时：" + str(t1))
        starttime2 = time.time()
        deplist2 = tc.client.Usrm_GetDepartmentOfUsers(departmentId="151bcb65-48ce-4b62-973f-0bb6685f9cb8", start=0,
                                                       limit=-1)
        t2 = time.time() - starttime2
        print("组织结构部门耗时：" + str(t2))

        starttime3 = time.time()
        deplist3 = tc.client.Usrm_GetDepartmentOfUsers(departmentId="3a33006c-aaee-11ea-aa3f-005056825c8b", start=0,
                                                       limit=-1)
        t3 = time.time() - starttime3
        print("10w用户部门耗时：" + str(t3))
        # print(deplist3)

    @staticmethod
    @allure.step("创建部门")
    def CreateDepartment(departName="depart", parentId="151bcb65-48ce-4b62-973f-0bb6685f9cb8"):
        """
        thrift接口:创建部门C
        :return: departmentId 部门iD
        """
        tc = Thrift_client(service=ncTShareMgnt, host="10.2.176.245")
        addParam = ttypes.ncTAddDepartParam(departName=departName, parentId=parentId,
                                            ossId=None, priority=None, email=None)
        departmentId = tc.client.Usrm_AddDepartment(addParam=addParam)
        tc.close()
        return departmentId

    @staticmethod
    @allure.step("删除部门")
    def DeleteDepartment(depart_id=None, manager_id="266c6a42-6131-4d62-8f39-853e7093701c"):
        tc = Thrift_client(service=ncTShareMgnt, host="10.2.176.245")
        tc.client.Usrm_DeleteDepartment(depart_id=depart_id, manager_id=manager_id)
        tc.close()


if __name__ == '__main__':
    # # CommonAccNetRestrictBoundPolicy().create_user(loginName="djakja")
    # CommonAccNetRestrictBoundPolicy().close_person_doc(user_id="33dd3b4e-abb9-11ea-9de1-005056825c8b")
    # CommonAccNetRestrictBoundPolicy().del_user(user_id="33dd3b4e-abb9-11ea-9de1-005056825c8b")
    # depid = CommonAccNetRestrictBoundPolicy().create_Users_departments(n=3, users_number=3, level=3)
    # # print(depid)
    CommonAccNetRestrictBoundPolicy.create_many_user()
    # CommonAccNetRestrictBoundPolicy.Usrm_GetDepartmentofusers()

    # 创建网段
    # for index in range(255):
    #     for j in range(10,20):
    #         try:
    #             CommonAccNetRestrictBoundPolicy().add_Network(name="网段名称" + str((index+1)*j +1000),
    #                                                       start_ip="10.2." + str(j) + "." + str(index),
    #                                                       end_ip="192.168." + str(j) + "." + str(index),
    #                                                       ip_address="", netmask="", net_type="ip_segment",
    #                                                       host="10.2.176.94")
    #         except Exception as e :
    #             break
