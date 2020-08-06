import pytest
import allure
import sys
sys.path.append("../../../../")
from Common.readjson import JsonRead
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect


@pytest.mark.ASP_344
@pytest.mark.high
@allure.severity('blocker')  # 优先级
@allure.feature("文档域策略管控")
class Test_SetPolicyClientRestriction200(object):
    @allure.testcase("ID5482,用例名：设置策略内容--非子域客户端登录限制，配置成功--返回200 ")
    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_SetPolicyClientRestriction200.json").dict_value_join())
    def test_SetPolicyClientRestriction200(self, url, jsondata, headers, checkpoint):
        '''
        用例描述：该用例用于测试设置策略内容，设置客户端登录限制
        使用非子域环境设置，设置后调用thrift接口获取设置值验证设置成功
        '''
        setpolicy_client = Http_client()
        setpolicy_client.put(url=url, data=jsondata, header=headers)
        assert setpolicy_client.status_code == checkpoint['status_code']

        #调取数据库，验证设置成功
        db = DB_connect("sharemgnt_db")
        query_result = db.select_one("select f_value from t_sharemgnt_config where f_key = 'forbid_ostype'")
        assert int(query_result[0]) == checkpoint['number']

if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_SetPolicyClientRestriction200.py'])
