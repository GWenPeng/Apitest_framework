# coding=utf-8
import pytest
import allure
from functools import lru_cache
from Common.get_token import Token
from .CommonDocDomain import CommonDocDomain
from Common.http_request import Http_client
from Common.readjson import JsonRead
from DB_connect.mysqlconnect import DB_connect


@lru_cache()
def get_token(host="10.2.176.245"):
    access_token = Token(host=host).get_token()["access_token"]
    return access_token


@pytest.mark.ASP_317
@allure.feature("修改本域类型")
class Test_PutSelfDomainType(object):
    """
        Test_suite修改本域类型
    """

    @allure.testcase("5294,本域类型设置--本域为为子域，设置目标域为平级域,返回200")
    def test_PutSelfDomainTypeParallel(self):
        """
        test_case修改本域类型由子域改为平级域
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.208")  # 清除子域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")  # 添加子域
        domain = CommonDocDomain().getSelfDomain(host="10.2.176.208")

        CommonDocDomain().setSelfDomain(host="10.2.176.208", domaintype="parallel", fatherdomain=domain["host"])

        newDomain = CommonDocDomain().getSelfDomain(host="10.2.176.208")  # 获取本域详情
        assert newDomain["type"] == "parallel"
        CommonDocDomain().setSelfDomain(host="10.2.176.208", domaintype="child", fatherdomain=domain["host"])

    @allure.testcase("5296,本域类型设置--本域为平级域，设置目标域为子域,返回200")
    def test_PutSelfDomainTypeChild(self):
        """
        test_case修改本域类型为子域
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.208")  # 清除子域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        CommonDocDomain().getSelfDomain(host="10.2.176.208")
        CommonDocDomain().setSelfDomain(host="10.2.176.208", domaintype="child", fatherdomain="10.2.176.245")
        newDomain = CommonDocDomain().getSelfDomain(host="10.2.176.208")  # 获取本域详情
        assert newDomain["type"] == "child"
        CommonDocDomain().setSelfDomain(host="10.2.176.208", domaintype="parallel", fatherdomain="10.2.176.245")

    @allure.testcase("5297,本域为父域，设置目标域为平级域 ，返回409")
    def test_PutSelfDomainTypeFParallel409(self):
        """
        本域为父域 ，存在合法域名M
        设置目标域为平级域；
        :return:
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.208")  # 清除子域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")  # 添加子域，成为父域
        host = "10.2.176.245"
        domaintype = "parallel"
        fatherdomain = "10.2.176.245"
        # token = get_token(host)
        client = Http_client(tagname="HTTPGWP")
        client.put(url="https://" + host + ":443/api/document-domain-management/v1/domain/self/type",
                   header={"Content-Type": "application/json"},
                   json={"type": domaintype, "host": fatherdomain})
        assert client.status_code == 409

    @allure.testcase("5297,本域为父域，设置目标域为平级域 ，返回409")
    def test_PutSelfDomainTypeFChild409(self):
        """
        本域为父域 ，存在合法域名M
        设置目标域为子域；
        :return:
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.208")  # 清除子域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")  # 添加子域，成为父域
        host = "10.2.176.245"
        domaintype = "child"
        fatherdomain = "10.2.180.162"
        # token = get_token(host)
        client = Http_client(tagname="HTTPGWP")
        client.put(url="https://" + host + ":443/api/document-domain-management/v1/domain/self/type",
                   header={"Content-Type": "application/json"},
                   json={"type": domaintype, "host": fatherdomain})
        assert client.status_code == 409

    @allure.testcase("5295,本域类型设置--本域为平级域，设置目标域为平级域,返回409")
    def test_PutSelfDomainTypePParallel409(self):
        """
        本域为为平級域，设置目标域为平级域；
        :return:
        """
        CommonDocDomain().clearRelationDomain(host="10.2.180.162")  # 清除平級域的关系域
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域的关系域
        host = "10.2.180.162"
        domaintype = "parallel"
        fatherdomain = "10.2.176.245"
        token = get_token(host)
        client = Http_client(tagname="HTTPGWP")
        client.put(url="https://" + host + ":443/api/document-domain-management/v1/domain/self/type",
                   header={"Content-Type": "application/json", "Authorization": "Bearer " + token},
                   json={"type": domaintype, "host": fatherdomain})
        print(client.jsonResponse)
        assert client.status_code == 400

    @pytest.fixture(scope="function")
    def setupdb(self):
        """

        :return:
        """
        db = DB_connect(dbname="db_domain_self")
        domain = db.select_one("SELECT * from t_domain_self")
        # print(domain)
        db.update('UPDATE t_domain_self set f_type="parallel" ,f_parent_host=NULL;')
        yield
        if domain[2] is None:
            xstr = "null"
        else:
            xstr = domain[2]
        sql = 'UPDATE t_domain_self set f_type="' + domain[1] + '" ,f_parent_host=' + xstr
        print(sql)
        db.update(sql)
        db.close()

    @allure.testcase("5292,本域类型设置--type类型枚举不存在，返回400")
    @allure.testcase("5290,本域类型设置--校验字段值为空或null，返回400")
    @allure.testcase("5288,本域类型设置--校验字段是否必填，返回400")
    @pytest.mark.parametrize("url,header,jsondata,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/PutSelfDomainType400.json").dict_value_join())
    def test_PutSelfDomainType400(self, setupdb, url, header, jsondata, checkpoint):
        """

        :param url:
        :param header:
        :param jsondata:
        :param checkpoint:
        :return:
        """
        # token = get_token()
        # header["Authorization"] = "Bearer " + token
        client = Http_client(tagname="HTTPGWP")
        client.put(url=url, header=header, json=jsondata)
        assert client.status_code == checkpoint["status_code"]
