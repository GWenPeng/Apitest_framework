import pytest
import allure
import json
from Common.readjson import JsonRead
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect
from Common.thrift_client import Thrift_client
from ShareMgnt import ncTShareMgnt


@pytest.mark.ASP_4581
@allure.feature("文档域策略管控")
class Test_SetPolicyMgnt_PolicyContent200or400(object):
    @pytest.mark.medium
    @allure.testcase("10732 设置策略管理服务策略内容--非子域客户端登录限制，配置参数错误--返回400")
    @allure.testcase("10734 设置策略管理服务策略内容--非子域双因子认证，配置参数错误--返回400")
    @allure.testcase("10736 设置策略管理服务策略内容--非子域密码强度，配置参数错误--返回400")
    @pytest.mark.parametrize(argnames="name,jsondata,remark",
                             argvalues=JsonRead("AS\\Http\\ForwardedPolicyMgntInter\\testdata"
                                                "\\test_SetPolicyMgnt_Policy400.json").dict_value_join())
    def test_SetPolicyMgnt_Policy400(self, name, jsondata, remark):
        put_client = Http_client()
        put_url = "/api/document-domain-management/v1/policy/general/{name}/value".format(name=name)
        put_client.put(url=put_url, json=jsondata, header={"Content-Type": "application/json"})
        print(put_client.jsonResponse)
        assert put_client.status_code == 400
        assert put_client.jsonResponse["code"] == 400000000
        assert put_client.jsonResponse["message"] == "Invalid request."

    @pytest.mark.high
    @allure.testcase("10733 设置策略管理服务策略内容--非子域客户端登录限制，配置成功--返回200")
    @pytest.mark.parametrize(argnames="jsondata,number,remark",
                             argvalues=JsonRead("AS\\Http\\ForwardedPolicyMgntInter\\testdata"
                                                "\\test_SetPolicyMgnt_Client_Restriction200.json").dict_value_join())
    def test_SetPolicyMgnt_client_restriction200(self, jsondata, number, remark):
        put_client = Http_client()
        put_url = "/api/document-domain-management/v1/policy/general/client_restriction/value"
        put_client.put(url=put_url, json=jsondata, header={"Content-Type": "application/json"})
        db = DB_connect("sharemgnt_db")
        # 验证客户端登陆限制
        query_result = db.select_one("select f_value from t_sharemgnt_config where f_key = 'forbid_ostype'")
        assert int(query_result[0]) == number

    @pytest.mark.high
    @allure.testcase("10735 设置策略管理服务策略内容--非子域双因子认证，配置参数成功--返回200--图形验证码")
    @pytest.mark.parametrize(argnames="jsondata,number,remark",
                             argvalues=JsonRead("AS\\Http\\ForwardedPolicyMgntInter\\testdata"
                                                "\\test_SetPolicyMgnt_Multi_Factor200.json").dict_value_join())
    def test_SetPolicyMgnt_Multi_Factor200(self, jsondata, number, remark):
        put_client = Http_client()
        put_url = "/api/document-domain-management/v1/policy/general/multi_factor_auth/value"
        put_client.put(url=put_url, json=jsondata, header={"Content-Type": "application/json"})
        db = DB_connect("sharemgnt_db")
        # 验证双因子认证
        query_result = db.select_one("select f_value from t_sharemgnt_config where f_key = 'vcode_login_config'")
        assert query_result[0] == number

    @pytest.mark.high
    @allure.testcase("10735 设置策略管理服务策略内容--非子域双因子认证，配置参数成功--返回200--短信/动态密码")
    @pytest.mark.parametrize(argnames="jsondata,mark,remark",
                             argvalues=JsonRead("AS\\Http\\ForwardedPolicyMgntInter\\testdata"
                                                "\\test_SetPolicyMgnt_SMSorOTP200.json").dict_value_join())
    def test_SetPolicyMgnt_SMSorOTP200(self, jsondata, mark, remark):
        put_client = Http_client()
        put_url = "/api/document-domain-management/v1/policy/general/multi_factor_auth/value"
        put_client.put(url=put_url, json=jsondata, header={"Content-Type": "application/json"})
        print(put_client.jsonResponse)
        tc = Thrift_client(ncTShareMgnt)
        response = tc.client.GetCustomConfigOfString("dualfactor_auth_server_status")
        response_dict = json.loads(response)
        if mark == "otp":
            assert response_dict['auth_by_OTP'] == True
        else:
            assert response_dict['auth_by_sms'] == True

    @pytest.mark.high
    @allure.testcase("10737 设置策略管理服务策略内容--非子域密码强度，配置参数成功--返回200")
    @pytest.mark.parametrize(argnames="jsondata,strong_pwd_length,remark",
                             argvalues=JsonRead("AS\\Http\\ForwardedPolicyMgntInter\\testdata"
                                                "\\test_SetPolicyMgnt_Password200.json").dict_value_join())
    def test_SetPolicyMgnt_Password200(self, jsondata, strong_pwd_length, remark):
        put_client = Http_client()
        put_url = "/api/document-domain-management/v1/policy/general/password_strength_meter/value"
        put_client.put(url=put_url, json=jsondata, header={"Content-Type": "application/json"})
        print(put_client.jsonResponse)
        # 调取数据库，验证设置成功
        db = DB_connect("sharemgnt_db")
        query_length = db.select_one("select f_value from t_sharemgnt_config where f_key = 'strong_pwd_length'")
        query_status = db.select_one("select f_value from t_sharemgnt_config where f_key = 'strong_pwd_status'")
        assert int(query_length[0]) == int(strong_pwd_length)
        assert int(query_status[0]) == 1



