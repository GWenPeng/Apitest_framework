import pytest
import allure
from Common.readjson import JsonRead
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect
from .CommonDocPolicyMgnt import CommonDocPolicyMgnt


@pytest.mark.ASP_344
@pytest.mark.high
@allure.severity('blocker')  # 优先级
@allure.feature("文档域策略管控")
class Test_GetChildDomain(object):

    @allure.testcase("ID5390,用例名：获取已绑定子文档域--非子域start参数正向检查--返回200")
    @allure.testcase("ID5392,用例名：获取已绑定子文档域--非子域limit参数正向检查--返回200")
    @allure.testcase("ID5396,用例名：获取已绑定子文档域--子域start参数正向检查--返回200")
    @allure.testcase("ID5398,用例名：获取已绑定子文档域--子域limit参数正向检查--返回200")
    @pytest.fixture(scope="function")
    def create_policy(self, metadata_host):
        father_host = metadata_host["replace.eisoo.com"]
        child_host1 = metadata_host["child.eisoo.com"]
        child_host2 = metadata_host["self.eisoo.com"]
        father_host = (father_host.split(":")[1]).strip("/")
        child_host1 = (child_host1.split(":")[1]).strip("/")
        child_host2 = (child_host2.split(":")[1]).strip("/")
        # 获取策略id
        strategyId = CommonDocPolicyMgnt().AddPolicy('{"content":[{"name":"password_strength_meter",'
                                                     '"value":{"enable":True,"length":22}}],"name":"policy1"}')
        yield strategyId, father_host, child_host1, child_host2
        # 删除策略配置
        dbclose = DB_connect()
        dbclose.delete('delete from domain_mgnt.t_policy_tpls')
        dbclose.delete('delete from domain_mgnt.t_policy_tpl_domains')
        dbclose.delete('delete from domain_mgnt.t_relationship_domain')
        dbclose.close()

    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_GetChildDomain200.json").dict_value_join())
    def test_GetChildDomain200(self, url, jsondata, headers, checkpoint, create_policy):
        strategyId = create_policy[0]
        father_host = create_policy[1]
        child_host1 = create_policy[2]
        child_host2 = create_policy[3]
        doc = CommonDocPolicyMgnt()
        ids = strategyId + "/bound-domain"
        doc.addDocDoamin(strategyId=strategyId, father_host=father_host, child_host1=child_host1, child_host2=child_host2)
        client = Http_client()
        client.get(url=url + ids, params=jsondata, header=headers)
        assert client.status_code == checkpoint['status_code']
        assert len(client.jsonResponse["data"]) == checkpoint["data"]
        assert client.elapsed <= 20.0
    

    @allure.testcase("ID5388,用例名：获取已绑定子文档域--非子域key_word参数检查--返回200")
    @allure.testcase("ID5394,用例名：获取已绑定子文档域--子域key_word参数检查--返回200")
    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_GetChildDomain_Keyword200.json").dict_value_join())
    def test_GetChildDomain_keyword200(self, url, jsondata, headers, checkpoint, create_policy):
        strategyId = create_policy[0]
        father_host = create_policy[1]
        child_host1 = create_policy[2]
        child_host2 = create_policy[3]
        doc = CommonDocPolicyMgnt()
        ids = strategyId + "/bound-domain"
        doc.addDocDoamin(strategyId=strategyId, father_host=father_host, child_host1=child_host1, child_host2=child_host2)
        client = Http_client()
        client.get(url=url + ids, params=jsondata, header=headers)
        assert client.status_code == checkpoint['status_code']
        assert client.elapsed <= 20.0

    @allure.testcase("ID5388,用例名：获取已绑定子文档域--非子域key_word参数检查--返回200")
    @allure.testcase("ID5394,用例名：获取已绑定子文档域--子域key_word参数检查--返回200")
    def test_GetChildDomainCount(self, create_policy):
        strategyId = create_policy[0]
        father_host = create_policy[1]
        child_host1 = create_policy[2]
        child_host2 = create_policy[3]
        doc = CommonDocPolicyMgnt()
        ids = strategyId + "/bound-domain"
        doc.addDocDoamin(strategyId=strategyId, father_host=father_host, child_host1=child_host1, child_host2=child_host2)
        client = Http_client()
        url = "/api/document-domain-management/v1/policy-tpl/" + ids
        data = {'start': 0, 'limit': 1, 'key_word': '爱数'}
        client.get(url=url, params=data, header="{\"Content-Type\":\"application/json\"}")
        dataInfos = client.jsonResponse['data']
        for dataInfo in dataInfos:
            host = dataInfo['host']
        assert client.status_code == 200
        assert host == '爱数'
        assert client.jsonResponse['count'] == 1
        assert client.elapsed <= 20.0

    @allure.testcase("ID5387,用例名：获取已绑定子文档域--非子域策略ID参数异常检查--返回404")
    def test_GetChildDomain404(self, create_policy):
        strategyId = create_policy[0]
        father_host = create_policy[1]
        child_host1 = create_policy[2]
        child_host2 = create_policy[3]
        doc = CommonDocPolicyMgnt()
        doc.addDocDoamin(strategyId=strategyId, father_host=father_host, child_host1=child_host1, child_host2=child_host2)
        client = Http_client()
        # 缺少策略ID参数，同时去除/符号
        url = "/api/document-domain-management/v1/policy-tpl/" + "bound-domain"
        client.get(url=url, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 404
        assert client.jsonResponse['message'] == "Resource not found."
        assert client.elapsed <= 20.0

        # 策略ID不存在
        url = "/api/document-domain-management/v1/policy-tpl/" + strategyId + "1/bound-domain"
        client.get(url=url, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 404
        assert client.jsonResponse['message'] == "Resource not found."
        assert client.elapsed <= 20.0

        # 多个有效策略ID
        url = "/api/document-domain-management/v1/policy-tpl/" + strategyId + ",0033b878-cf89-4ecd-8bdf-62da7d9f2efc/bound-domain"
        client.get(url=url, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 404
        assert client.jsonResponse['message'] == "Resource not found."
        assert client.elapsed <= 20.0

    @allure.testcase("ID5389,用例名： 获取已绑定子文档域--非子域start参数异常检查--返回400")
    @allure.testcase("ID5391,用例名： 获取已绑定子文档域--非子域limit参数异常检查--返回400")
    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_GetChildDomain400.json").dict_value_join())
    def test_GetChildDomain400(self, url, jsondata, headers, checkpoint, create_policy):
        strategyId = create_policy[0]
        father_host = create_policy[1]
        child_host1 = create_policy[2]
        child_host2 = create_policy[3]
        doc = CommonDocPolicyMgnt()
        doc.addDocDoamin(strategyId=strategyId, father_host=father_host, child_host1=child_host1, child_host2=child_host2)
        client = Http_client()
        ids = strategyId + "/bound-domain"
        client.get(url=url + ids, params=jsondata, header=headers)
        assert client.status_code == 400
        assert client.jsonResponse['code'] == checkpoint['code']
        assert client.jsonResponse['message'] == checkpoint['message']
        assert client.elapsed <= 20.0


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_GetChildDomain.py'])
