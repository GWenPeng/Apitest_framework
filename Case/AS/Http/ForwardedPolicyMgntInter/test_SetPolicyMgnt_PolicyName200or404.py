import pytest
import allure
from Common.readjson import JsonRead
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect


@pytest.mark.ASP_4581
@allure.feature("文档域策略管控")
class Test_SetPolicyMgnt_PolicyName200or404(object):
    @pytest.mark.high
    @allure.testcase("10731 设置策略管理服务策略内容--非子域name参数正向检查--返回200--设置单个策略")
    @pytest.fixture(scope="function")
    def tear_down_pass(self):
        pass
        yield
        # 消除脏数据,将策略设置为原值
        put_client = Http_client()
        put_url = "/api/document-domain-management/v1/policy/general/password_strength_meter/value"
        put_client.put(url=put_url,
                       json=[{"name": "password_strength_meter", "value": {"enable": False, "length": 8}}],
                       header={"Content-Type": "application/json"})
        if put_client.status_code != 200:
            print(put_client.jsonResponse)

    def test_SetPolicyMgnt_one200(self, tear_down_pass):
        put_client = Http_client()
        put_url = "/api/document-domain-management/v1/policy/general/password_strength_meter/value"
        put_client.put(url=put_url,
                       json=[{"name": "password_strength_meter", "value": {"enable": True, "length": 33}}],
                       header={"Content-Type": "application/json"})
        # 调取数据库，验证设置成功
        db = DB_connect("sharemgnt_db")
        query_length = db.select_one("select f_value from t_sharemgnt_config where f_key = 'strong_pwd_length'")
        query_status = db.select_one("select f_value from t_sharemgnt_config where f_key = 'strong_pwd_status'")
        assert int(query_length[0]) == 33
        assert int(query_status[0]) == 1

    @allure.testcase("10731 设置策略管理服务策略内容--非子域name参数正向检查--返回200--设置多个策略")
    @pytest.mark.high
    @pytest.fixture(scope="function")
    def tear_down_two(self):
        pass
        yield
        put_client = Http_client()
        put_url = "/api/document-domain-management/v1/policy/general/{name}/value".format(name="password_strength_meter"
                                                                                               ",multi_factor_anth")
        put_client.put(url=put_url,
                       json=[{"name": "password_strength_meter", "value": {"enable": False, "length": 8}},
                             {"name": "multi_factor_auth",
                              "value": {"enable": False, "image_vcode": False, "otp": False, "password_error_count": 0,
                                        "sms_vcode": False}}],
                       header={"Content-Type": "application/json"})
        if put_client.status_code != 200:
            print(put_client.jsonResponse)

    def test_SetPolicyMgnt_many200(self, tear_down_two):
        put_client = Http_client()
        put_url = "/api/document-domain-management/v1/policy/general/{name}/value".format(name="password_strength_meter"
                                                                                               ",multi_factor_auth")
        put_client.put(url=put_url,
                       json=[{"name": "password_strength_meter", "value": {"enable": True, "length": 11}},
                             {"name": "multi_factor_auth",
                              "value": {"enable": True, "image_vcode": True, "otp": False, "password_error_count": 5,
                                        "sms_vcode": False}}],
                       header={"Content-Type": "application/json"})
        print(put_client.jsonResponse)
        # 调取数据库，验证设置成功
        db = DB_connect("sharemgnt_db")
        query_length = db.select_one("select f_value from t_sharemgnt_config where f_key = 'strong_pwd_length'")
        query_status = db.select_one("select f_value from t_sharemgnt_config where f_key = 'strong_pwd_status'")
        query_result = db.select_one("select f_value from t_sharemgnt_config where f_key = 'vcode_login_config'")
        assert query_result[0] == "{\"passwdErrCnt\": 5, \"isEnable\": true}"
        assert int(query_length[0]) == 11
        assert int(query_status[0]) == 1

    @allure.testcase("10731 设置策略管理服务策略内容--非子域name参数正向检查--返回200--设置全部策略")
    @pytest.mark.high
    @pytest.fixture(scope="function")
    def tear_down_all(self):
        pass
        yield
        put_client = Http_client()
        put_url = "/api/document-domain-management/v1/policy/general/{name}/value". \
            format(name="password_strength_meter,multi_factor_auth,client_restriction,network_restriction")
        put_client.put(url=put_url,
                       json=[{"name": "network_restriction", "value": {"is_enabled": False}},
                             {"name": "password_strength_meter", "value": {"enable": False, "length": 8}},
                             {"name": "multi_factor_auth", "value": {"enable": False, "image_vcode": False, "otp": False,
                                                                     "password_error_count": 0, "sms_vcode": False}},
                             {"name": "client_restriction", "value": {"android": False, "ios": False, "mac": False,
                                                                      "mobile_web": False, "pc_web": False,
                                                                      "windows": False}}],
                       header={"Content-Type": "application/json"})
        if put_client.status_code != 200:
            print(put_client.jsonResponse)

    def test_SetPolicyMgnt_all200(self, tear_down_all):
        put_client = Http_client()
        put_url = "/api/document-domain-management/v1/policy/general/{name}/value". \
            format(name="password_strength_meter,multi_factor_auth,client_restriction,network_restriction")
        put_client.put(url=put_url,
                       json=[{"name": "network_restriction", "value": {"is_enabled": True}},
                             {"name": "password_strength_meter", "value": {"enable": True, "length": 22}},
                             {"name": "multi_factor_auth", "value": {"enable": True, "image_vcode": True, "otp": False,
                                                                     "password_error_count": 5, "sms_vcode": False}},
                             {"name": "client_restriction", "value": {"android": True, "ios": True, "mac": False,
                                                                      "mobile_web": False, "pc_web": False,
                                                                      "windows": False}}],
                       header={"Content-Type": "application/json"})
        print(put_client.jsonResponse)
        # 调取数据库，验证设置成功
        db = DB_connect("sharemgnt_db")
        query_length = db.select_one("select f_value from t_sharemgnt_config where f_key = 'strong_pwd_length'")
        query_status = db.select_one("select f_value from t_sharemgnt_config where f_key = 'strong_pwd_status'")
        query_result = db.select_one("select f_value from t_sharemgnt_config where f_key = 'vcode_login_config'")
        # 验证双因子认证
        assert query_result[0] == "{\"passwdErrCnt\": 5, \"isEnable\": true}"
        # 验证密码强度
        assert int(query_length[0]) == 22
        assert int(query_status[0]) == 1
        # 验证客户端登陆限制
        query_result = db.select_one("select f_value from t_sharemgnt_config where f_key = 'forbid_ostype'")
        assert int(query_result[0]) == 6
        # 验证访问者登陆限制
        result1 = db.select_one("select f_value from policy_mgnt.t_policies where f_name='network_restriction'")
        assert result1[0] == '{"is_enabled":true}'

    @allure.testcase("10731 设置策略管理服务策略内容--非子域name参数正向检查--返回200--url中没有但是body中有，忽略设置")
    @pytest.mark.high
    @pytest.fixture(scope="function")
    def tear_down_err(self):
        pass
        yield
        put_client = Http_client()
        put_url = "/api/document-domain-management/v1/policy/general/{name}/value".format(name="password_strength_meter")
        put_client.put(url=put_url,
                       json=[{"name": "password_strength_meter", "value": {"enable": False, "length": 8}}],
                       header={"Content-Type": "application/json"})
        if put_client.status_code != 200:
            print(put_client.jsonResponse)

    def test_SetPolicyMgnt_err200(self, tear_down_err):
        put_client = Http_client()
        put_url = "/api/document-domain-management/v1/policy/general/{name}/value".format(name="password_strength_meter")
        put_client.put(url=put_url,
                       json=[{"name": "network_restriction", "value": {"is_enabled": True}},
                             {"name": "password_strength_meter", "value": {"enable": True, "length": 55}}],
                       header={"Content-Type": "application/json"})
        print(put_client.jsonResponse)
        # 调取数据库，验证设置成功和访问者部分被忽略
        db = DB_connect("sharemgnt_db")
        query_length = db.select_one("select f_value from t_sharemgnt_config where f_key = 'strong_pwd_length'")
        query_status = db.select_one("select f_value from t_sharemgnt_config where f_key = 'strong_pwd_status'")
        # 验证密码强度
        assert int(query_length[0]) == 55
        assert int(query_status[0]) == 1
        # 验证访问者登陆限制
        result1 = db.select_one("select f_value from policy_mgnt.t_policies where f_name='network_restriction'")
        assert result1[0] == '{"is_enabled":false}'

    @pytest.mark.medium
    @allure.testcase("10730 设置策略管理服务策略内容--非子域name参数异常检查--返回404")
    @pytest.mark.parametrize(argnames="name,jsondata,remark",
                             argvalues=JsonRead("AS\\Http\\ForwardedPolicyMgntInter\\testdata"
                                                "\\test_SetPolicyMgnt_Name404.json").dict_value_join())
    def test_SetPolicyMgnt_404(self, name, jsondata, remark):
        put_client = Http_client()
        put_url = "/api/document-domain-management/v1/policy/general/{name}/value".format(name=name)
        put_client.put(url=put_url, json=jsondata, header={"Content-Type": "application/json"})
        print(put_client.jsonResponse)
        assert put_client.status_code == 404
        assert put_client.jsonResponse["code"] == 404013000
        assert put_client.jsonResponse["message"] == "Resource not found."
