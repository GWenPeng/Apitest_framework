# coding=utf-8
import pytest
import allure

from .CommonDocDomain import CommonDocDomain
from DB_connect.mysqlconnect import DB_connect
from Common.readjson import JsonRead
from Common.http_request import Http_client


@pytest.mark.ASP_317
@pytest.mark.high
@allure.feature("删除文档域")
class Test_DelMgntV1Domain(object):
    """
     Test_suites删除文档域

    """

    @allure.testcase("5287,关系域删除--删除子域成功，更改子域域类型时网络连接成功，返回200")
    def test_delChildDocDomain200(self):
        """
        只有一个子域，删除子域
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.208")  # 清除子域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        domain_data=CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")
        uuid = domain_data[0]  # 添加一个子域
        SelfDomain = CommonDocDomain().getSelfDomain(host="10.2.176.245")  # 查询本域详情
        assert SelfDomain['type'] == "parent"  # 删除子域前断言本域为父域
        CommonDocDomain().delRelationDomain(uuid=uuid)  # 删除子域
        newSelfDomain = CommonDocDomain().getSelfDomain(host="10.2.176.245")  # 再次查询本域详情
        assert newSelfDomain['type'] == "parallel"  # 修改后断言本域为平级域

    @allure.testcase("5287,关系域删除--删除子域成功，更改子域域类型时网络连接成功，返回200")
    def test_delMoreChildDocDomain200(self):
        """
        存在多个子域，删除子域
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.208")  # 清除子域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.180.162")  # 清空另外一个子域
        domain_data=CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")
        uuid = domain_data[0]  # 添加子域1
        domain_data2=CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="child")
        uuid2 = domain_data2[0]  # 添加子域2
        SelfDomain = CommonDocDomain().getSelfDomain(host="10.2.176.245")  # 查询本域详情
        assert SelfDomain['type'] == "parent"  # 删除子域前断言本域为父域
        CommonDocDomain().delRelationDomain(uuid=uuid)  # 删除子域
        newSelfDomain = CommonDocDomain().getSelfDomain(host="10.2.176.245")  # 再次查询本域详情
        assert newSelfDomain['type'] == "parent"  # 修改后断言本域为平级域

        CommonDocDomain().delRelationDomain(uuid=uuid2)  # 再次删除子域2
        new2SelfDomain = CommonDocDomain().getSelfDomain(host="10.2.176.245")  # 再次查询本域2详情
        assert new2SelfDomain['type'] == "parallel"  # 删除后的本域为平级域

    @allure.testcase("5287,关系域删除--删除子域成功，更改子域域类型时网络连接成功，返回200")
    def test_delParallelDocDomain200(self):
        """
        # 删除平级域
        :return: 断言本域类型仍然为平级域
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.180.162")  # 清空一个平级域关系域
        uuid = CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="parallel")
        SelfDomain = CommonDocDomain().getSelfDomain(host="10.2.176.245")  # 查询本域详情
        assert SelfDomain['type'] == "parallel"  # 删除子域前断言本域为平级域
        newSelfDomain = CommonDocDomain().getSelfDomain(host="10.2.176.245")  # 再次查询本域详情
        assert newSelfDomain['type'] == "parallel"

    @allure.step("初始化父域添加子域并策略绑定")
    @pytest.fixture(scope="function")
    def setupaddPoliyBound(self, fatherdomain="10.2.176.245", childdomain="10.2.180.162"):
        """

        :param fatherdomain:
        :param childdomain:
        :return:
        """

        data = CommonDocDomain().getPolicyList(httphost=fatherdomain)
        if len(data["data"]) != 0:
            policyuuid = data["data"][0]["id"]
            CommonDocDomain().clearBoundPolicyChild(httphost=fatherdomain, policyuuid=policyuuid)  # 清空策略绑定
        else:
            policyuuid = CommonDocDomain().addPolicy(httphost=fatherdomain)  # 否则添加一条策略
        print("policyuuid:", policyuuid)
        CommonDocDomain().clearRelationDomain(host=fatherdomain)  # 清空父域的关系域
        CommonDocDomain().clearRelationDomain(host=childdomain)  # 清空一个子域域关系域
        domain_data=CommonDocDomain().addRelationDomain(host=childdomain, httphost=fatherdomain,
                                            domaintype="child")
        childuuid = domain_data[0]  # 添加子域

        res = CommonDocDomain().BoundPolicy(httphost=fatherdomain, PolicyUUID=policyuuid, ChildDomainUUID=childuuid)
        print("绑定策略结果：", res)
        yield fatherdomain, childuuid, policyuuid

        CommonDocDomain().delboundPolicy(httphost=fatherdomain, PolicyUUID=policyuuid,
                                         ChildDomainUUID=childuuid)

    @allure.testcase("5284,关系域删除--删除子域失败，返回409")
    def test_delDocDomainHavePolicy409(self, setupaddPoliyBound):
        """
        有策略绑定；调用删除接口，删除子域失败返回409
        :return:
        """
        status = CommonDocDomain().delRelationDomain(host=setupaddPoliyBound[0], uuid=setupaddPoliyBound[1])
        assert status == 409

    @allure.step("初始化父域添加子域并策略绑定")
    @pytest.fixture(scope="function", params=["child", "parallel"])
    def setupaddDoclibSynPlan(self, request, fatherdomain="10.2.176.245", childdomain="10.2.180.162"):
        db = DB_connect(dbname="db_domain_self")
        db.delete('DELETE from t_library_sync_plan where f_id="4516ca17-faa8-45e0-ae6c-583673b205fc"')
        CommonDocDomain().clearRelationDomain(host=fatherdomain)  # 清空父域的关系域
        CommonDocDomain().clearRelationDomain(host=childdomain)  # 清空一个子域域关系域
        domainuuid = CommonDocDomain().addRelationDomain(httphost=fatherdomain, domaintype=request.param,
                                                         host=childdomain)[0]
        db.insert('INSERT INTO t_library_sync_plan VALUES ( "4516ca17-faa8-45e0-ae6c-583673b205fc",'
                  '"gns://CC6939142843419CA2897B444B518FDA","文档库A","' + domainuuid + '",'
                                                                                     '"' + childdomain + '","文档库H","live","null","running",DATE_SUB(NOW(), INTERVAL 8 HOUR))')
        db.close()

        return fatherdomain, domainuuid

    # @allure.testcase("5284,关系域删除--删除子域失败，返回409")
    # @pytest.mark.skip(msg="文档库同步计划代码没上，在开发中")
    # def test_delDocDomainHaveDocLibSynPlan409(self, setupaddDoclibSynPlan):
    #     """
    #     有文档库同步计划；调用删除接口
    #     :return:
    #     """
    #     status = CommonDocDomain().delRelationDomain(host=setupaddDoclibSynPlan[0], uuid=setupaddDoclibSynPlan[1])
    #     assert status == 409
    #     db = DB_connect(dbname="db_domain_self")
    #     db.delete('DELETE from t_library_sync_plan where f_id="4516ca17-faa8-45e0-ae6c-583673b205fc"')
    #     db.close()

    # @allure.testcase("5286,关系域删除--删除子域失败，更改子域域类型时网络连接失败，返回400")
    # def test_deldomainLink400(self):
    #     """
    #
    #     :return:
    #     """

    @allure.testcase("5283, 关系域删除--不存在的Id，返回404或405")
    @pytest.mark.parametrize("url,header,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/DelRelationDomain400.json").dict_value_join())
    def test_delrelationdomain400(self, url, header, checkpoint):
        """

        :return:
        """

        client = Http_client(tagname="HTTPGWP")
        client.delete(url=url, header=header)
        assert client.status_code == checkpoint["status_code"]
        if checkpoint["status_code"] == 404:
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["detail"]["notfound_params"][0] == checkpoint["detail.notfound_params"]
        print(client.status_code)
        print(client.jsonResponse)
