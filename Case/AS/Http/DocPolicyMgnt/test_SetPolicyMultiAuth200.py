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
class Test_SetPolicyMultiAuth200(object):
    @allure.testcase("ID5484,用例名：设置策略内容--非子域双因子认证，配置参数成功--返回200")
    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_SetPolicyMultiAuth200.json").dict_value_join())
    def test_SetPolicyMultiAuth200(self, url, jsondata, headers, checkpoint):
        setpolicy_client = Http_client()
        setpolicy_client.put(url=url, data=jsondata, header=headers)
        assert setpolicy_client.status_code == checkpoint['status_code']

        #调取数据库，验证设置成功
        db = DB_connect("sharemgnt_db")
        query_result = db.select_one("select f_value from t_sharemgnt_config where f_key = 'vcode_login_config'")
        assert query_result[0] == checkpoint['number']

if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_SetPolicyMultiAuth200.py'])
