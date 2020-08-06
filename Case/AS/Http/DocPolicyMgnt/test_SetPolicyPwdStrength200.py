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
class Test_SetPolicyPwdStrength200(object):
    @allure.testcase("ID5486,用例名：设置策略内容--非子域密码强度，配置参数成功--返回200")
    @pytest.mark.parametrize("url, headers, jsondata, checkpoint", argvalues=JsonRead(
        "AS\\Http\\DocPolicyMgnt\\testdata\\test_SetPolicyPwdStrength200.json").dict_value_join())
    def test_SetPolicyPwdStrength200(self, url, jsondata, headers, checkpoint):
        '''
        用例描述：该用例用于测试设置策略内容，设置密码强度
        使用非子域环境设置，设置后对比数据库验证设置成功
        '''
        setpolicy_client = Http_client()
        setpolicy_client.put(url=url, data=jsondata, header=headers)
        print (setpolicy_client.jsonResponse)
        assert setpolicy_client.status_code == checkpoint['status_code']

        #调取数据库，验证设置成功
        db = DB_connect("sharemgnt_db")
        query_length = db.select_one("select f_value from t_sharemgnt_config where f_key = 'strong_pwd_length'")
        query_status = db.select_one("select f_value from t_sharemgnt_config where f_key = 'strong_pwd_status'")
        assert int(query_length[0]) == checkpoint['strong_pwd_length']
        assert int(query_status[0]) == checkpoint['strogh_pwd_status']

if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_SetPolicyPwdStrength200.py'])
