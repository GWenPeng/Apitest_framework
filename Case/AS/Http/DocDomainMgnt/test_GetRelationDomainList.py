# coding=utf-8
import pytest
import allure

from .CommonDocDomain import CommonDocDomain
from Common.http_request import Http_client
from Common.readjson import JsonRead
from DB_connect.mysqlconnect import DB_connect


@pytest.mark.ASP_317
@allure.feature("查询关系域列表")
class Test_GetRelationDomainList(object):
    """
        Test_suite查询关系域列表
    """

    @allure.testcase("5298关系域列表查询--校验key_word字段不填，返回200")
    @allure.testcase("5299,关系域列表查询--校验key_word字段值为空，返回200")
    @allure.testcase("5300,关系域列表查询--校验key_word字段值为null，返回200 ")
    @pytest.mark.parametrize("params",
                             ({"offset": 0, "limit": 3}, {"key_word": "", "limit": 3}, {"key_word": None, "offset": 0},
                              {"key_word": "", "offset": 0, "limit": 3}, {"key_word": "10", "offset": None, "limit": 3},
                              {"key_word": "10", "offset": 0, "limit": None}))
    def test_GetRelationDomainList(self, params):
        """
        test_case查询关系域列表，校验字段是否必传
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域关系域
        CommonDocDomain().addRelationDomain(host="10.2.176.176", domaintype="parallel")
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")
        CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="child")
        # token = get_token()
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/document-domain-management/v1/domain",
                   header={"Content-Type": "application/json"},
                   params=params, )
        assert client.status_code == 200
        assert client.jsonResponse["count"] == 3
        assert len(client.jsonResponse["data"]) == 3

    @allure.testcase("5306,关系域列表查询--key_word 查询为空,返回200，data列表为空")
    @pytest.mark.parametrize("key_word", ("19.2.176", "anyshare"))
    def test_GetRelationDomainListNone(self, key_word):
        """
        test_case查询关系域列表查询返回为空
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域关系域
        CommonDocDomain().addRelationDomain(host="10.2.176.176", domaintype="parallel")
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")
        CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="child")
        # token = get_token()
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/document-domain-management/v1/domain",
                   header={"Content-Type": "application/json"},
                   params={"key_word": key_word, "offset": 0, "limit": 3}, )
        assert client.status_code == 200
        assert client.jsonResponse["count"] == 0
        assert len(client.jsonResponse["data"]) == 0

    @allure.testcase("5304,关系域列表查询--key_word 通过IP查询，返回200")
    @pytest.mark.parametrize("key_word", ("10.2.180", "10.2.180.162"))
    def test_GetRelationDomainListByKeyIP(self, key_word):
        """
        test_case查询关系域列表，通过IP精确查询and 模糊查询
        :keyword 搜索关键字
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域关系域
        CommonDocDomain().addRelationDomain(host="10.2.176.176", domaintype="parallel")
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")
        CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="child")
        # token = get_token()
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/document-domain-management/v1/domain",
                   header={"Content-Type": "application/json"},
                   params={"key_word": key_word, "offset": 0, "limit": 3}, )
        assert client.status_code == 200
        if key_word == "10.2.176":
            assert len(client.jsonResponse["data"]) == 2
            assert client.jsonResponse["count"] == 2
            for index in range(2):
                assert key_word in client.jsonResponse["data"][index]["host"]
        elif key_word == "10.2.180.162":
            assert len(client.jsonResponse["data"]) == 1
            assert client.jsonResponse["count"] == 1
            assert client.jsonResponse["data"][0]["host"] == key_word

    @allure.testcase("5305,关系域列表查询--key_word 通过域名查询，返回200")
    @pytest.mark.parametrize("key_word", ("eisoo", "child.eisoo.com"))
    def test_GetRelationDomainListByKeyName(self, key_word):
        """
        test_case查询关系域列表，通过域名name精确查询and 模糊查询
        :keyword 搜索关键字
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域关系域
        CommonDocDomain().addRelationDomain(host="10.2.176.176", domaintype="parallel")
        CommonDocDomain().addRelationDomain(host="child.eisoo.com", domaintype="child")
        CommonDocDomain().addRelationDomain(host="parallel.eisoo.com", domaintype="parallel")
        # token = get_token()
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/document-domain-management/v1/domain",
                   header={"Content-Type": "application/json"},
                   params={"key_word": key_word, "offset": 0, "limit": 3}, )
        assert client.status_code == 200
        if key_word == "eisoo":
            assert len(client.jsonResponse["data"]) == 2
            assert client.jsonResponse["count"] == 2
            for index in range(2):
                assert key_word in client.jsonResponse["data"][index]["host"]
        elif key_word == "child.eisoo.com":
            assert len(client.jsonResponse["data"]) == 1
            assert client.jsonResponse["count"] == 1
            assert client.jsonResponse["data"][0]["host"] == key_word

    @pytest.mark.high
    @allure.testcase("5307,关系域列表查询--校验请求字段边界值")
    @pytest.mark.parametrize("url,header,params,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/GetRelationDomainListPage.json").dict_value_join())
    def test_GetRelationDomainListPage(self, url, header, params, checkpoint):
        """
        # testcase测试查询关系域列表的分页功能;
        :param url:请求地址
        :param header:请求头
        :param params:请求params参数
        :param checkpoint:断言，检查点t
        :return: None
        """
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空父域关系域
        CommonDocDomain().addRelationDomain(host="10.2.176.176", domaintype="parallel")
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="child")
        CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="child")
        # header = eval(header)
        # token = get_token()
        # header["Authorization"] = "Bearer " + token
        client = Http_client(tagname="HTTPGWP")
        client.get(url=url, header=header, params=eval(params))
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code == 200:
            assert client.jsonResponse["count"] == checkpoint["count"]
            assert len(client.jsonResponse["data"]) == checkpoint["data"]
        else:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]

    @allure.testcase("5302,关系域列表查询--参数类型错误，返回400")
    @allure.testcase("5301,关系域列表查询--校验字段值为null，返回400")
    @pytest.mark.parametrize("url,header,params,checkpoint",
                             argvalues=JsonRead(
                                 "AS/Http/DocDomainMgnt/testdata/GetRelationDomainList400.json").dict_value_join())
    def test_GetRelationDomainList400(self, url, header, params, checkpoint):
        """

        :param url:
        :param header:
        :param params:
        :param checkpoint:
        :return:
        """
        # header = eval(header)
        # token = get_token()
        # header["Authorization"] = "Bearer " + token
        client = Http_client(tagname="HTTPGWP")
        client.get(url=url, header=header, params=params)
        print(client.jsonResponse)
        assert client.status_code == checkpoint["status_code"]
        if client.status_code == 400:
            assert client.jsonResponse["code"] == checkpoint["code"]
            assert client.jsonResponse["message"] == checkpoint["message"]
            assert client.jsonResponse["cause"] == checkpoint["cause"]
            assert client.jsonResponse["detail"] == checkpoint["detail"]
        # if "message" in checkpoint:
        #     assert client.jsonResponse["message"] == checkpoint["message"]
        #     assert client.jsonResponse["detail"]["invalid_params"][0] == checkpoint["detail.invalid_params"]

    @pytest.fixture(scope="function")
    def setup_AddDomain(self):
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")  # 清空关系域
        db = DB_connect(dbname="db_domain_self")
        db.insert("INSERT INTO `domain_mgnt`.`t_relationship_domain` (\n\t`f_id`,\n\t`f_host`,\n\t`f_port`,"
                  "\n\t`f_secret`,\n\t`f_secret_type`,\n\t`f_domain_type`,\n\t`f_credential_id`,\n\t`f_credential_key`,"
                  "\n\t`f_create_time`\n)\nVALUES\n\t(\n\t\t'05e4143a-73f1-4048-91c5-74e6d19133b1',\n\t\t'bf.ds.cn',"
                  "\n\t\t'443',\n\t\t'secrect',\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',"
                  "\n\t\t'2020-03-10 11:18:48'\n\t),\n\t(\n\t\t'07d991b9-dba6-411e-bb25-3618149f0ff1',"
                  "\n\t\t'9.2.180.99',\n\t\t'443',\n\t\t'secrect',\n\t\t'',\n\t\t'parallel',\n\t\t'admin',"
                  "\n\t\t'eisoo.com',\n\t\t'2020-03-10 11:16:32'\n\t),"
                  "\n\t(\n\t\t'09cf4cd9-182a-4223-bc4e-29d1661b92f5',\n\t\t'tt.aa.com',\n\t\t'443',\n\t\t'secrect',"
                  "\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',\n\t\t'2020-03-05 15:34:19'\n\t),"
                  "\n\t(\n\t\t'0a8da7c5-1ea9-474b-b828-de03efdc5bf8',\n\t\t'3.2.180.99',\n\t\t'443',\n\t\t'secrect',"
                  "\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',\n\t\t'2020-03-10 11:15:57'\n\t),"
                  "\n\t(\n\t\t'134de43f-41ab-430b-a542-7c5b0d622c61',\n\t\t'AA.aa.com',\n\t\t'443',\n\t\t'secrect',"
                  "\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',\n\t\t'2020-03-05 15:34:02'\n\t),"
                  "\n\t(\n\t\t'2d968f4e-0fc2-467f-9e4a-89fbadc223f6',\n\t\t'LOL.ds.cn',\n\t\t'443',\n\t\t'secrect',"
                  "\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',\n\t\t'2020-03-10 11:19:31'\n\t),"
                  "\n\t(\n\t\t'4d74b744-5e70-44ca-9371-65470582d010',\n\t\t'222.2.180.99',\n\t\t'443',"
                  "\n\t\t'secrect',\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',\n\t\t'2020-03-10 "
                  "11:15:47'\n\t),\n\t(\n\t\t'5332d5e5-08cb-4cf5-978d-a3449a732b8b',\n\t\t'aa.dsad.com',\n\t\t'443',"
                  "\n\t\t'',\n\t\t'',\n\t\t'parallel',\n\t\t'',\n\t\t'',\n\t\t'2020-03-09 13:49:59'\n\t),"
                  "\n\t(\n\t\t'65c0e9c4-0144-48f5-a12a-25bfa19f4c9c',\n\t\t'ac.sdsa.com',\n\t\t'443',\n\t\t'',"
                  "\n\t\t'',\n\t\t'parallel',\n\t\t'',\n\t\t'',\n\t\t'2020-03-09 13:50:11'\n\t),"
                  "\n\t(\n\t\t'6aa86dcb-086c-4f99-8aae-00747eece33d',\n\t\t'qidian.ds.cn',\n\t\t'443',"
                  "\n\t\t'secrect',\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',\n\t\t'2020-03-10 "
                  "11:19:18'\n\t),\n\t(\n\t\t'6eb9eb7d-1033-40cc-869f-080a06b5af29',\n\t\t'10.2.176.202',\n\t\t'443',"
                  "\n\t\t'secrect',\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',\n\t\t'2020-03-02 "
                  "11:27:00'\n\t),\n\t(\n\t\t'72401a89-6083-4279-ae4d-7ab77dabbd07',\n\t\t'Bu.sd.com',\n\t\t'443',"
                  "\n\t\t'',\n\t\t'',\n\t\t'parallel',\n\t\t'',\n\t\t'',\n\t\t'2020-03-09 13:50:26'\n\t),"
                  "\n\t(\n\t\t'73435100-f781-45b7-8a41-8cba03aa48b7',\n\t\t'aa.aaa.cn',\n\t\t'443',\n\t\t'secrect',"
                  "\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',\n\t\t'2020-03-10 11:20:21'\n\t),"
                  "\n\t(\n\t\t'7e597282-106b-4e9d-bda4-1c54305bf55e',\n\t\t'xinlang.ds.cn',\n\t\t'443',"
                  "\n\t\t'secrect',\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',\n\t\t'2020-03-10 "
                  "11:19:11'\n\t),\n\t(\n\t\t'8fc98da4-91ab-4b8d-aa80-52b4f18fd98d',\n\t\t'dnf.ds.cn',\n\t\t'443',"
                  "\n\t\t'secrect',\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',\n\t\t'2020-03-10 "
                  "11:19:27'\n\t),\n\t(\n\t\t'93308efa-a37a-4634-b78d-428e62d2d46a',\n\t\t'145.2.180.99',\n\t\t'443',"
                  "\n\t\t'secrect',\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',\n\t\t'2020-03-10 "
                  "11:15:53'\n\t),\n\t(\n\t\t'd6434476-fea5-48c9-b943-b4966548c502',\n\t\t'FF.aa.com',\n\t\t'443',"
                  "\n\t\t'secrect',\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',\n\t\t'2020-03-05 "
                  "15:34:10'\n\t),\n\t(\n\t\t'd7d792d0-ba24-4cb2-929c-c465f40dca85',\n\t\t'10.2.176.23',\n\t\t'554',"
                  "\n\t\t'secrect',\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',\n\t\t'2020-03-09 "
                  "14:01:35'\n\t),\n\t(\n\t\t'eefb5f0a-f632-4f57-8c77-07df1a02163e',\n\t\t'aa.aa.can',\n\t\t'443',"
                  "\n\t\t'secrect',\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',\n\t\t'2020-03-10 "
                  "11:20:48'\n\t),\n\t(\n\t\t'f7b54946-6c28-4369-9f38-a593d2f69607',\n\t\t'VF.aa.com',\n\t\t'443',"
                  "\n\t\t'secrect',\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',\n\t\t'2020-03-05 "
                  "15:34:15'\n\t),\n\t(\n\t\t'fd0367a5-f399-4dbd-927c-37520c63ad2e',\n\t\t'Ba.ds.cn',\n\t\t'443',"
                  "\n\t\t'secrect',\n\t\t'',\n\t\t'parallel',\n\t\t'admin',\n\t\t'eisoo.com',\n\t\t'2020-03-10 "
                  "11:19:04'\n\t);")
        yield db
        db.delete("DELETE from t_relationship_domain ;")
        db.close()

    def test_GetRelationDomainListSortHost(self, setup_AddDomain):
        """
        ASP-5498：关系域列表查询接口未按照名称排序
        验证排序规则正确
        :return:
        """
        Domainlist = ["10.2.176.202", "10.2.176.23", "145.2.180.99", "222.2.180.99", "3.2.180.99", "9.2.180.99",
                      "aa.aa.can", "AA.aa.com", "aa.aaa.cn", "aa.dsad.com", "ac.sdsa.com", "Ba.ds.cn", "bf.ds.cn",
                      "Bu.sd.com", "dnf.ds.cn", "FF.aa.com", "LOL.ds.cn", "qidian.ds.cn", "tt.aa.com", "VF.aa.com",
                      "xinlang.ds.cn"]
        res = CommonDocDomain().getRelationDomainList()
        for i in range(len(res["data"])):
            assert res["data"][i]["host"] == Domainlist[i]

    @pytest.fixture(scope='function')
    def add_direct_domain(self):
        CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="child", network_type="direct")
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="parallel", network_type="direct")
        yield
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")

    def test_GetRelationDomainList_direct(self, add_direct_domain):
        """
        查询关系域列表，获取直链模式子域、平级域
        :return:
        """
        res = CommonDocDomain().getRelationDomainList()
        print(res)
        assert res["data"][0]["host"] == "10.2.176.208"
        assert res["data"][0]["type"] == "parallel"
        assert res["data"][0]["network_type"] == "direct"
        assert res["data"][1]["host"] == "10.2.180.162"
        assert res["data"][1]["type"] == "child"
        assert res["data"][1]["network_type"] == "direct"

    @pytest.fixture(scope='function')
    def add_indirect_domain(self):
        CommonDocDomain().addRelationDomain(host="10.2.180.162", domaintype="child", network_type="indirect")
        CommonDocDomain().addRelationDomain(host="10.2.176.208", domaintype="parallel", network_type="indirect")
        yield
        CommonDocDomain().clearRelationDomain(host="10.2.176.245")

    def test_GetRelationDomainList_indirect(self, add_indirect_domain):
        """
        查询关系域列表，获取非直链模式子域或平级域
        :return:
        """
        res = CommonDocDomain().getRelationDomainList()
        print(res)
        assert res["data"][0]["host"] == "10.2.176.208"
        assert res["data"][0]["type"] == "parallel"
        assert res["data"][0]["network_type"] == "indirect"
        assert res["data"][1]["host"] == "10.2.180.162"
        assert res["data"][1]["type"] == "child"
        assert res["data"][1]["network_type"] == "direct"

    @pytest.fixture(scope="function")
    def setup_add_relation_domain(self):
        for i in range(5):
            for index in range(200):
                CommonDocDomain().addRelationDomain(host="101.12." + str(i) + "." + str(index), port=443,
                                                    domaintype="parallel",
                                                    credential_id="admin",
                                                    credential_key="eisoo.com", httphost="10.2.176.245",
                                                    network_type="indirect")
        CommonDocDomain().addRelationDomain(host="101.12.6.1", port=443, domaintype="parallel",
                                            credential_id="admin",
                                            credential_key="eisoo.com", httphost="10.2.176.245", network_type="indirect")
        yield
        # CommonDocDomain().clearRelationDomain(host="10.2.176.245")
        DB_connect(host="10.2.176.245").delete(sql='DELETE from domain_mgnt.t_relationship_domain where '
                                                   'f_domain_type="parallel";')

    @pytest.mark.high
    @allure.testcase("10276, 关系域列表查询-limit边界值合法验证")
    @allure.testcase("10275, 关系域列表查询-offset,limit默认值")
    def test_GetRelationDomainList_default(self, setup_add_relation_domain):
        """

        :return:
        """

        # limit输入0
        # token = get_token()
        client = Http_client(tagname="HTTPGWP")
        client.get(url="/api/document-domain-management/v1/domain?key_word=&offset=0&limit=0",
                   header={"Content-Type": "application/json"})
        assert client.status_code == 400
        assert client.jsonResponse["code"] == 400000000
        assert client.jsonResponse["message"] == "Invalid request."
        assert client.jsonResponse["cause"] == ""
        assert client.jsonResponse["detail"] == {"invalid_params": ["limit"]}

        # limit输入1
        client1 = Http_client(tagname="HTTPGWP")
        client1.get(url="/api/document-domain-management/v1/domain?key_word=&offset=0&limit=1",
                    header={"Content-Type": "application/json"})
        assert client1.status_code == 200
        assert len(client1.jsonResponse["data"]) == 1
        assert client1.jsonResponse["count"] == 1001
        assert client1.jsonResponse["data"][0]["host"] == "101.12.0.0"
        # print(client1.jsonResponse)

        # limit输入2
        client2 = Http_client(tagname="HTTPGWP")
        client2.get(url="/api/document-domain-management/v1/domain?key_word=&offset=0&limit=2",
                    header={"Content-Type": "application/json"})
        assert client2.status_code == 200
        assert len(client2.jsonResponse["data"]) == 2
        assert client2.jsonResponse["count"] == 1001
        assert client2.jsonResponse["data"][0]["host"] == "101.12.0.0"
        # print(client2.jsonResponse)

        # limit输入-1
        client3 = Http_client(tagname="HTTPGWP")
        client3.get(url="/api/document-domain-management/v1/domain?key_word=&offset=0&limit=-1",
                    header={"Content-Type": "application/json"})
        assert client3.status_code == 400
        assert client3.jsonResponse["code"] == 400000000
        assert client3.jsonResponse["message"] == "Invalid request."
        assert client3.jsonResponse["cause"] == ""
        assert client3.jsonResponse["detail"] == {"invalid_params": ["limit"]}
        # print(client3.jsonResponse)

        # limit输入1000
        client4 = Http_client(tagname="HTTPGWP")
        client4.get(url="/api/document-domain-management/v1/domain?key_word=&offset=0&limit=1000",
                    header={"Content-Type": "application/json"})
        assert client4.status_code == 200
        assert len(client4.jsonResponse["data"]) == 1000
        assert client4.jsonResponse["count"] == 1001
        assert client4.jsonResponse["data"][0]["host"] == "101.12.0.0"
        # print(client4.jsonResponse)
        # limit输入1001
        client5 = Http_client(tagname="HTTPGWP")
        client5.get(url="/api/document-domain-management/v1/domain?key_word=&offset=0&limit=1001",
                    header={"Content-Type": "application/json"})
        assert client5.status_code == 400
        assert client5.jsonResponse["code"] == 400000000
        assert client5.jsonResponse["message"] == "Invalid request."
        assert client5.jsonResponse["cause"] == ""
        assert client5.jsonResponse["detail"] == {"invalid_params": ["limit"]}
        # print(client5.jsonResponse)

        # limit输入999 offset输入0
        client6 = Http_client(tagname="HTTPGWP")
        client6.get(url="/api/document-domain-management/v1/domain?key_word=&offset=0&limit=999",
                    header={"Content-Type": "application/json"})
        assert client6.status_code == 200
        assert len(client6.jsonResponse["data"]) == 999
        assert client6.jsonResponse["count"] == 1001
        assert client6.jsonResponse["data"][0]["host"] == "101.12.0.0"
        # print(client6.jsonResponse)

        # offset输入-1
        client7 = Http_client(tagname="HTTPGWP")
        client7.get(url="/api/document-domain-management/v1/domain?key_word=&offset=-1&limit=999",
                    header={"Content-Type": "application/json"})
        assert client7.status_code == 400
        assert client7.jsonResponse["code"] == 400000000
        assert client7.jsonResponse["message"] == "Invalid request."
        assert client7.jsonResponse["cause"] == ""
        assert client7.jsonResponse["detail"] == {"invalid_params": ["offset"]}
        # print(client7.jsonResponse)

        # offset输入1
        client8 = Http_client(tagname="HTTPGWP")
        client8.get(url="/api/document-domain-management/v1/domain?key_word=&offset=1&limit=1000",
                    header={"Content-Type": "application/json"})
        assert client8.status_code == 200
        assert len(client8.jsonResponse["data"]) == 1000
        assert client8.jsonResponse["count"] == 1001
        assert client8.jsonResponse["data"][0]["host"] == "101.12.0.1"
        # print(client8.jsonResponse)

        # offset输入2
        client9 = Http_client(tagname="HTTPGWP")
        client9.get(url="/api/document-domain-management/v1/domain?key_word=&offset=2&limit=1000",
                    header={"Content-Type": "application/json"})
        assert client9.status_code == 200
        assert len(client9.jsonResponse["data"]) == 999
        assert client9.jsonResponse["count"] == 1001
        assert client9.jsonResponse["data"][0]["host"] == "101.12.0.10"
        # print(client9.jsonResponse)

        # offset字段不传
        client10 = Http_client(tagname="HTTPGWP")
        client10.get(url="/api/document-domain-management/v1/domain?key_word=&limit=1000",
                     header={"Content-Type": "application/json"})
        assert client10.status_code == 200
        assert len(client10.jsonResponse["data"]) == 1000
        assert client10.jsonResponse["count"] == 1001
        assert client10.jsonResponse["data"][0]["host"] == "101.12.0.0"
        # print(client10.jsonResponse)

        # limit字段不传
        client11 = Http_client(tagname="HTTPGWP")
        client11.get(url="/api/document-domain-management/v1/domain?key_word=&offset=0",
                     header={"Content-Type": "application/json"})
        assert client11.status_code == 200
        assert len(client11.jsonResponse["data"]) == 20
        assert client11.jsonResponse["count"] == 1001
        assert client11.jsonResponse["data"][0]["host"] == "101.12.0.0"
        # print(client11.jsonResponse)

        # offset和limit值不传
        client12 = Http_client(tagname="HTTPGWP")
        client12.get(url="/api/document-domain-management/v1/domain?key_word=&offset=&limit=",
                     header={"Content-Type": "application/json"})
        assert client12.status_code == 200
        assert len(client12.jsonResponse["data"]) == 20
        assert client12.jsonResponse["count"] == 1001
        assert client12.jsonResponse["data"][0]["host"] == "101.12.0.0"
        # print(client12.jsonResponse)
