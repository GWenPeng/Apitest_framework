import pytest
import allure
from Common.readjson import JsonRead
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect


@pytest.mark.ASP_4581
@allure.feature("文档域策略管控")
class Test_SetPolicyMgnt_PolicyState200or404(object):
    @pytest.mark.medium
    @allure.testcase("10742 设置策略管理服务策略状态--非子域设置策略管理服务策略状态，参数错误--返回404")
    @pytest.mark.parametrize(argnames="url,jsondata,mark,remark",
                             argvalues=JsonRead("AS\\Http\\ForwardedPolicyMgntInter\\testdata"
                                                "\\test_SetPolicyMgnt_PolicyState404.json").dict_value_join())
    def test_SetPolicyMgnt_Policy404(self, url, jsondata, mark, remark):
        put_client = Http_client()
        put_client.put(url=url, json=jsondata, header={"Content-Type": "application/json"})
        if put_client != 200:
            print(put_client.jsonResponse)
        if mark == 0:
            assert put_client.status_code == 404
        else:
            assert put_client.status_code == 404
            assert put_client.jsonResponse["code"] == 404013000
            assert put_client.jsonResponse["message"] == "Resource not found."

    @pytest.mark.high
    @allure.testcase("10743 设置策略管理服务策略状态--非子域设置策略管理服务策略状态，设置成功--返回200")
    @pytest.mark.parametrize(argnames="url,jsondata,name,locked,remark",
                             argvalues=JsonRead("AS\\Http\\ForwardedPolicyMgntInter\\testdata"
                                                "\\test_SetPolicyMgnt_PolicyState200.json").dict_value_join())
    def test_SetPolicyMgnt_Policy200(self, url, jsondata, name, locked, remark):
        put_client = Http_client()
        put_client.put(url=url, json=jsondata, header={"Content-Type": "application/json"})
        # 分割name
        name_list = name.split(",")
        print(name_list)
        for i in name_list:
            # 调取数据库，验证设置成功和访问者部分被忽略
            db = DB_connect("sharemgnt_db")
            select_sql = "select f_locked from  policy_mgnt.t_policies where f_name = '{name}'".format(name=i)
            query = db.select_one(select_sql)
            assert query[0] == locked

    @pytest.mark.medium
    @allure.testcase("10744 设置策略管理服务策略状态--非子域设置策略管理服务策略状态，参数错误--返回400")
    @pytest.mark.parametrize(argnames="url,jsondata,remark",
                             argvalues=JsonRead("AS\\Http\\ForwardedPolicyMgntInter\\testdata"
                                                "\\test_SetPolicyMgnt_PolicyState400.json").dict_value_join())
    def test_SetPolicyMgnt_Policy400(self, url, jsondata, remark):
        put_client = Http_client()
        put_client.put(url=url, json=jsondata, header={"Content-Type": "application/json"})
        if put_client != 200:
            print(put_client.jsonResponse)
        assert put_client.status_code == 400
        assert put_client.jsonResponse["code"] == 400000000
        assert put_client.jsonResponse["message"] == "Invalid request."
