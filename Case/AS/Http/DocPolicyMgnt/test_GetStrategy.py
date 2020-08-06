import pytest
import allure
from Common.readjson import JsonRead
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect


@pytest.mark.ASP_344
@pytest.mark.high
@allure.feature("文档域策略管控")
class Test_GetStrategy(object):
    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_AddStrategy.json").dict_value_join())
    # 添加测试数据-添加策略
    def test_addStrategy(self, url, jsondata, headers, checkpoint):
        client = Http_client()
        client.post(url=url, jsondata=eval(jsondata), header=headers)

    @allure.testcase("ID5379,用例名：搜索策略--非子域offset参数正向检查--返回200")
    @allure.testcase("ID5381,用例名：搜索策略--非子域limit参数正向检查--返回200")
    @allure.testcase("ID5384,用例名：搜索策略--子域offset参数正向检查--返回200")
    @allure.testcase("ID5386,用例名：搜索策略--子域limit参数正向检查--返回200")
    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_GetStrategy200.json").dict_value_join())
    def test_GetStrategy200(self, url, jsondata, headers, checkpoint):
        """
        用例描述：test_GetStrategy200方法用于测试搜索策略接口
        json数据包含禅道上多条用例的校验，具体对body中不同功能的传参检查
        """
        client = Http_client()
        client.get(url=url, params=jsondata, header=headers)
        assert client.status_code == checkpoint['status_code']
        print(client.jsonResponse)
        print(client.jsonResponse["data"])
        assert len(client.jsonResponse["data"]) == checkpoint["data"]
        assert client.elapsed <= 20.0

    @allure.testcase("ID5377,用例名：搜索策略--非子域keyword参数检查--返回200")
    @allure.testcase("ID5382,用例名：搜索策略--子域keyword参数检查--返回200")
    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_GetStrategy_keyword200.json").dict_value_join())
    def test_GetStrategy_keyword200(self, url, jsondata, headers, checkpoint):
        """
        用例描述：test_GetStrategy200方法用于测试搜索策略接口
        json数据包含禅道上多条用例的校验，具体对body中不同功能的传参检查
        """
        client = Http_client()
        client.get(url=url, params=jsondata, header=headers)
        assert client.status_code == checkpoint['status_code']
        assert client.elapsed <= 20.0

    @allure.testcase("ID5377,用例名：搜索策略--非子域keyword参数检查--返回200")
    @allure.testcase("ID5382,用例名：搜索策略--子域keyword参数检查--返回200")
    def test_GetStrategyCount(self):
        """
        用例描述：test_GetStrategyCount方法用于判断查询返回接口总数
        """
        client = Http_client()
        url = "/api/document-domain-management/v1/policy-tpl/"
        data = {'offset': 0, 'limit': 20, 'key_word': '爱数'}
        client.get(url=url, params=data, header="{\"Content-Type\":\"application/json\"}")
        dataInfos = client.jsonResponse['data']
        for dataInfo in dataInfos:
            name = dataInfo['name']
        assert client.status_code == 200
        assert '爱数' in name
        assert client.jsonResponse['count'] == 1
        assert client.elapsed <= 20.0

    @allure.testcase("ID5378,用例名：搜索策略--非子域搜索offset参数异常检查--返回400 ")
    @allure.testcase("ID5385,用例名：搜索策略--子域limit参数异常检查--返回400")
    @allure.testcase("ID5380,用例名：搜索策略--非子域limit参数正向检查--返回400")
    @allure.testcase("ID5383,用例名：搜索策略--子域offset参数异常检查--返回400")
    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_GetStrategy400.json").dict_value_join())
    def test_GetStrategy400(self, url, jsondata, headers, checkpoint):
        """
        用例描述：test_GetStrategy400方法用于测试搜索策略接口
        json数据包含禅道上多条用例的校验，具体对body中不同功能的传参检查
        """
        client = Http_client()
        client.get(url=url, params=jsondata, header=headers)
        assert client.status_code == checkpoint['status_code']
        assert client.jsonResponse['code'] == checkpoint['code']
        assert client.jsonResponse['message'] == checkpoint['message']
        assert client.elapsed <= 20.0

    def test_cleraDate(self):
        db = DB_connect(dbname='database')
        db.delete('delete from domain_mgnt.t_policy_tpls')
        db.close()


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_GetStrategy.py'])
