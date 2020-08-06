import pytest
import allure
import sys

sys.path.append("../../../../")
from Common.readjson import JsonRead
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect
from .CommonDocPolicyMgnt import CommonDocPolicyMgnt


@pytest.mark.ASP_344
@pytest.mark.medium
@allure.severity('normal')  # 优先级
@allure.feature("文档域策略管控")
class Test_Domain_AddPolicy_NameCheck400(object):
    @allure.testcase("ID5313,用例名：新增策略配置--非子域环境新增策略，策略名称非法检查--返回400")
    # 每条用例执行完成后执行，清除环境
    @pytest.fixture(scope="function")
    def teardown(self):
        # 设置重复名称
        CommonDocPolicyMgnt().AddPolicy(jsondata='{"content":[{"name":"password_strength_meter",'
                                                 '"value":{"enable":False,"length":12}}],"name":"重复的策略名称"}')
        CommonDocPolicyMgnt().AddPolicy(jsondata='{"content":[{"name":"password_strength_meter",'
                                                 '"value":{"enable":False,"length":12}}],"name":"repeat strategy"}')
        CommonDocPolicyMgnt().AddPolicy(jsondata='{"content":[{"name":"password_strength_meter",'
                                                 '"value":{"enable":False,"length":12}}],"name":"~!%#$@-_. "}')
        CommonDocPolicyMgnt().AddPolicy(jsondata='{"content":[{"name":"password_strength_meter",'
                                                 '"value":{"enable":False,"length":12}}],"name":"11111"}')
        CommonDocPolicyMgnt().AddPolicy(jsondata='{"content":[{"name":"password_strength_meter",'
                                                 '"value":{"enable":False,"length":12}}],"name":"哈哈11111ss@"}')
        CommonDocPolicyMgnt().AddPolicy(jsondata='{"content":[{"name":"password_strength_meter",'
                                                 '"value":{"enable":False,"length":12}}],"name":"A"}')
        yield
        db = DB_connect()
        db.delete("delete from t_policy_tpls")

    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_AddPolicyName400.json").dict_value_join())
    def test_Domain_AddPolicy_NameCheck400(self, url, jsondata, headers, checkpoint, teardown):
        '''
        用例描述：该用例用于测试新增策略接口中策略"名称的参数400检查"，详情可见禅道用例
        '''
        add_client = Http_client()
        add_client.post(url=url, jsondata=jsondata, header=headers)
        # print (client.text)
        # 接口响应状态断言
        assert add_client.status_code == checkpoint['status_code']
        assert add_client.jsonResponse["code"] == checkpoint["code"]
        assert add_client.jsonResponse["message"] == checkpoint["message"]


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_AddPolicyName400.py'])
