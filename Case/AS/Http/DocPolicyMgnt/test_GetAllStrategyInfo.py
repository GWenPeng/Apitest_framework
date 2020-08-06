import pytest
import allure
from Common.readjson import JsonRead
from Common.http_request import Http_client


@pytest.mark.ASP_344
@pytest.mark.high
@allure.severity('blocker')  # 优先级
@allure.feature("文档域策略管控")
class Test_GetAllStrategyInfo(object):
    @allure.testcase("ID5471,用例名：获取所有策略信息--非子域mode参数正向检查--返回200")
    @allure.testcase("ID5477,用例名：获取所有策略信息--非子域name参数正向检查--返回200")
    @allure.testcase("ID5475,用例名：获取所有策略信息--非子域limit参数正向检查--返回200")
    @allure.testcase("ID5473,用例名：获取所有策略信息--非子域offset参数正向检查--返回200")
    @allure.testcase("ID5579,用例名：获取所有策略信息--子域mode参数正向检查--返回200")
    @allure.testcase("ID5581,用例名：获取所有策略信息--子域offset参数正向检查--返回200")
    @allure.testcase("ID5583,用例名：获取所有策略信息--子域limit参数正向检查--返回200")
    @allure.testcase("ID5585,用例名：获取所有策略信息--子域name参数正向检查--返回200")
    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_GetAllStrategyInfo200.json").dict_value_join())
    def test_GetAllStrategyInfo200(self, url, jsondata, headers, checkpoint):
        """
        用例描述：Test_GetAllStrategyInfo200方法用于获取所有策略信息接口
        json数据包含禅道上多条用例的校验，具体对body中不同功能的传参检查
        """
        client = Http_client()
        client.get(url=url, params=jsondata, header=headers)
        assert client.status_code == checkpoint['status_code']
        assert len(client.jsonResponse["data"]) == checkpoint["data"]
        assert client.elapsed <= 20.0

    @allure.testcase("ID5471,用例名：获取所有策略信息--非子域mode参数正向检查--返回200")
    @allure.testcase("ID5477,用例名：获取所有策略信息--非子域name参数正向检查--返回200")
    @allure.testcase("ID5579,用例名：获取所有策略信息--子域mode参数正向检查--返回200")
    @allure.testcase("ID5585,用例名：获取所有策略信息--子域name参数正向检查--返回200")
    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_GetAllStrategyInfo_name_mode200.json").dict_value_join())
    def test_GetAllStrategyInfo_name_mode200(self, url, jsondata, headers, checkpoint):
        """
        用例描述：Test_GetAllStrategyInfo200方法用于获取所有策略信息接口
        json数据包含禅道上多条用例的校验，具体对body中不同功能的传参检查
        """
        client = Http_client()
        client.get(url=url, params=eval(jsondata), header=headers)
        assert client.status_code == checkpoint['status_code']
        assert client.elapsed <= 20.0

    @allure.testcase("ID5477,用例名：获取所有策略信息--非子域name参数正向检查--返回200")
    @allure.testcase("ID5585,用例名：获取所有策略信息--子域name参数正向检查--返回200")
    def test_GetAllStrategyInfoCount(self):
        """
        用例描述：test_GetAllStrategyInfoCount方法用于判断查询返回接口总数
        """
        client = Http_client()
        url = "/api/policy-management/v1/general"
        data = {'mode':'current','offset': 0, 'limit': 20, 'name': 'client_restriction'}
        client.get(url=url, params=data, header="{\"Content-Type\":\"application/json\"}")
        dataInfos = client.jsonResponse['data']
        for dataInfo in dataInfos:
            name = dataInfo['name']
        assert client.status_code == 200
        assert name == 'client_restriction'
        assert client.jsonResponse['count'] == 1
        assert client.elapsed <= 20.0

    @allure.testcase("ID5470,用例名： 获取所有策略信息--非子域mode参数异常检查--返回400")
    @allure.testcase("ID5472,用例名： 获取所有策略信息--非子域offset参数异常检查--返回400")
    @allure.testcase("ID5474,用例名： 获取所有策略信息--非子域limit参数异常检查--返回400")
    @allure.testcase("ID5578,用例名： 获取所有策略信息--子域mode参数异常检查--返回400")
    @allure.testcase("ID5580,用例名： 获取所有策略信息--子域offset参数异常检查--返回400")
    @allure.testcase("ID5582,用例名： 获取所有策略信息--子域limit参数异常检查--返回400")
    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_GetAllStrategyInfo400.json").dict_value_join())
    def test_GetAllStrategyInfo400(self, url, jsondata, headers, checkpoint):
        """
        用例描述：Test_GetAllStrategyInfo400方法用于获取所有策略信息接口
        json数据包含禅道上多条用例的校验，具体对body中不同功能的传参检查
        """
        client = Http_client()
        client.get(url=url, params=jsondata, header=headers)
        assert client.status_code == checkpoint['status_code']
        assert client.jsonResponse['code'] == checkpoint['code']
        assert client.jsonResponse['message'] == checkpoint['message']
        assert client.elapsed <= 20.0


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_GetAllStrategyInfo.py'])
