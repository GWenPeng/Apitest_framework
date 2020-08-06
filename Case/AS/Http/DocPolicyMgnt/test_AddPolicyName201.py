import pytest
import allure
import sys

sys.path.append("../../../../")

from Common.readjson import JsonRead
from DB_connect.mysqlconnect import DB_connect
from Common.http_request import Http_client


@pytest.mark.ASP_344
@pytest.mark.high
@allure.severity('blocker')  # 优先级
@allure.feature("文档域策略管控")
class Test_Domain_AddPolicy_NameCheck201(object):
    @allure.testcase("ID5315,用例名：新增策略配置--非子域新增策略成功--返回201")
    # 每条用例执行完成后执行，清除环境
    @pytest.fixture(scope="function")
    def teardown(self):
        pass
        yield
        db = DB_connect()
        db.delete("delete from t_policy_tpls")

    @pytest.mark.parametrize("jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_AddPolicyName201.json").dict_value_join())
    def test_Domain_AddPolicy_NameCheck201(self, jsondata, checkpoint, teardown):
        '''
        用例描述：该用例用于测试新增策略接口中策略“名称的参数检查以及body中传递策略个数”的检查，详情可见禅道用例
        新增策略接口，只关注了策略的新增成功
        策略是否正常应用到子域以及子域功能的检验，在应用策略接口中覆盖
        '''
        # 新增策略
        add_client = Http_client()
        add_client.post(url="/api/document-domain-management/v1/policy-tpl",
                        jsondata=jsondata,
                        header="{\"Content-Type\":\"application/json\"}")
        # 接口响应状态断言
        assert add_client.status_code == checkpoint['status_code']
        # 获取t_policy_tpls表中策略id
        db = DB_connect()
        query_result = db.select_one("select f_id from t_policy_tpls")
        # sql查询结果为元组，获取元组第一个值，即策略id
        global policyid
        policyid = query_result[0]
        # 拼接location预期值
        location = "/api/document-domain-management/v1/policy-tpl/" + policyid
        assert location == add_client.respheaders['Location']
        assert add_client.elapsed <= 20.0


if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_AddPolicyName201.py'])
