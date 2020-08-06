import pytest
import allure
from Common.readjson import JsonRead
from Common.http_request import Http_client
from .CommonDocPolicyMgnt import CommonDocPolicyMgnt


@pytest.mark.ASP_344
@pytest.mark.high
@allure.severity('blocker')  # 优先级
@allure.feature("文档域策略管控")
class Test_EditStrategyState(object):
    StrategyName = ['client_restriction', 'multi_factor_auth', 'password_strength_meter']

    @allure.testcase("ID5600,用例名：设置策略状态--子域环境设置自己的策略，设置成功--返回200")
    @allure.testcase("ID5492,用例名：设置策略状态--非子域设置策略状态，设置成功--返回200")
    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_EditStrategyState200.json").dict_value_join())
    # 锁定单个策略状态
    def test_EditStrategyTrue200(self, url, jsondata, headers, checkpoint):
        """
        用例描述：test_EditStrategyState200方法用于设置策略状态接口
        json数据包含禅道上多条用例的校验，具体对body中不同功能的传参检查
        """
        edits = self.StrategyName[0] + "/state"
        client = Http_client()
        client.put(url=url + edits, json=jsondata, header=headers)
        # 获取修改后的策略状态
        comm = CommonDocPolicyMgnt()
        StrategyState = comm.selectStrategyState(self.StrategyName[0])
        assert client.status_code == checkpoint['status_code']
        assert StrategyState == 1
        assert client.elapsed <= 20.0

    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_EditStrategyState200.json").dict_value_join())
    # 锁定多个策略状态
    def test_EditStrategyTrues200(self, url, jsondata, headers, checkpoint):
        """
        用例描述：test_EditStrategyState200方法用于设置策略状态接口
        json数据包含禅道上多条用例的校验，具体对body中不同功能的传参检查
        """
        edits = self.StrategyName[1] + "," + self.StrategyName[2] + "/state"
        client = Http_client()
        client.put(url=url + edits, json=jsondata, header=headers)
        # 获取修改后的策略状态
        comm = CommonDocPolicyMgnt()
        StrategyState1 = comm.selectStrategyState(self.StrategyName[1])
        StrategyState2 = comm.selectStrategyState(self.StrategyName[2])
        assert client.status_code == checkpoint['status_code']
        assert StrategyState1 == 1
        assert StrategyState2 == 1
        assert client.elapsed <= 20.0

    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_EditStrategyState200.json").dict_value_join())
    # 解锁单个策略状态
    def test_EditStrategyFalse200(self, url, jsondata, headers, checkpoint):
        """
        用例描述：test_EditStrategyState200方法用于设置策略状态接口
        json数据包含禅道上多条用例的校验，具体对body中不同功能的传参检查
        """
        edits = self.StrategyName[0] + "/state"
        client = Http_client()
        client.put(url=url + edits, json={"locked": False}, header=headers)
        # 获取修改后的策略状态
        comm = CommonDocPolicyMgnt()
        StrategyState = comm.selectStrategyState(self.StrategyName[0])
        assert client.status_code == checkpoint['status_code']
        assert StrategyState == 0
        assert client.elapsed <= 20.0

    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_EditStrategyState200.json").dict_value_join())
    # 解锁多个策略状态
    def test_EditStrategyFalses200(self, url, jsondata, headers, checkpoint):
        """
        用例描述：test_EditStrategyState200方法用于设置策略状态接口
        json数据包含禅道上多条用例的校验，具体对body中不同功能的传参检查
        """
        edits = self.StrategyName[1] + "," + self.StrategyName[2] + "/state"
        client = Http_client()
        client.put(url=url + edits, json={"locked": False}, header=headers)
        # 获取修改后的策略状态
        comm = CommonDocPolicyMgnt()
        multistate = comm.selectStrategyState(self.StrategyName[1])
        psmstate = comm.selectStrategyState(self.StrategyName[2])
        assert client.status_code == checkpoint['status_code']
        assert multistate == 0
        assert psmstate == 0
        assert client.elapsed <= 20.0

    @allure.testcase("ID5599,用例名：设置策略状态--子域设置策略，参数错误，设置失败--返回404")
    @allure.testcase("ID5491,用例名：设置策略状态--非子域设置策略状态，参数错误，设置失败--返回404")
    def test_EditStrategyTrue404(self):
        """
        用例描述：test_EditStrategyState404方法用于设置策略状态接口
        """
        client = Http_client()

        # 缺少name参数，同时去除/符号
        url = "/api/policy-management/v1/general/" + "state"
        client.put(url=url, json={"locked": False}, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 404
        assert client.elapsed <= 20.0

        # 缺少name参数，保留/符号
        url = "/api/policy-management/v1/general/" + "/state"
        client.put(url=url, json={"locked": False}, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 404
        assert client.elapsed <= 20.0

        # name不存在
        url = "/api/policy-management/v1/general/%s" % "name" + "/state"
        client.put(url=url, json={"locked": False}, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 404
        assert client.jsonResponse['code'] == 404013000
        assert client.jsonResponse['message'] == 'Resource not found.'
        assert client.elapsed <= 20.0

    @allure.testcase("ID5799,用例名：设置策略状态--子域环境解锁已被锁定策略失败--返回400")
    def test_EditStrategyTrue400(self):
        """
        用例描述：test_EditStrategyState400方法用于设置策略状态接口
        """
        client = Http_client()

        # 缺少locked参数
        url = "/api/policy-management/v1/general/%s" % (self.StrategyName[1]) + "/state"
        client.put(url=url, json=None, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 400
        assert client.jsonResponse['code'] == 400000000
        assert client.jsonResponse['message'] == 'Invalid request.'
        assert client.elapsed <= 20.0

        # locked参数类型错误,locked为数字
        url = "/api/policy-management/v1/general/%s" % (self.StrategyName[1]) + "/state"
        client.put(url=url, json={"locked": 111}, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 400
        assert client.jsonResponse['code'] == 400000000
        assert client.jsonResponse['message'] == 'Invalid request.'
        assert client.elapsed <= 20.0

        # locked参数类型错误,locked为英文
        url = "/api/policy-management/v1/general/%s" % (self.StrategyName[1]) + "/state"
        client.put(url=url, json={"locked": "lock"}, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 400
        assert client.jsonResponse['code'] == 400000000
        assert client.jsonResponse['message'] == 'Invalid request.'
        assert client.elapsed <= 20.0

        # locked参数类型错误,locked为中文
        url = "/api/policy-management/v1/general/%s" % (self.StrategyName[1]) + "/state"
        client.put(url=url, json={"locked": "锁定"}, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 400
        assert client.jsonResponse['code'] == 400000000
        assert client.jsonResponse['message'] == 'Invalid request.'
        assert client.elapsed <= 20.0

        # locked参数类型错误,locked为符号
        url = "/api/policy-management/v1/general/%s" % (self.StrategyName[1]) + "/state"
        client.put(url=url, json={"locked": "**"}, header="{\"Content-Type\":\"application/json\"}")
        assert client.status_code == 400
        assert client.jsonResponse['code'] == 400000000
        assert client.jsonResponse['message'] == 'Invalid request.'
        assert client.elapsed <= 20.0


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_EditStrategyState.py'])
