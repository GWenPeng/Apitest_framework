import pytest
import allure
from Common.readjson import JsonRead
from Common.http_request import Http_client


@pytest.mark.ASP_4581
@allure.feature("文档域策略管控")
class Test_GetPolicyMgntAllInfo200or400(object):
    @pytest.mark.high
    @allure.severity('blocker')  # 优先级
    @allure.testcase("10724 获取策略管理服务所有策略信息--非子域mode参数正向检查--返回200")
    @allure.testcase("10726 获取策略管理服务所有策略信息--非子域offset参数正向检查--返回200 ")
    @allure.testcase("10728 获取策略管理服务所有策略信息--非子域limit参数正向检查--返回200 ")
    @pytest.mark.parametrize(argnames="params,checkpoint,remark",
                             argvalues=JsonRead("AS\\Http\\ForwardedPolicyMgntInter\\testdata"
                                                "\\test_GetPolicyMgntAllInfo200.json").dict_value_join())
    def test_GetPolicyMgntAllInfo200(self, params, checkpoint, remark):
        client = Http_client()
        client.get(url="/api/document-domain-management/v1/policy/general",
                   params=params,
                   header={"Content-Type": "application/json"})
        assert client.status_code == 200
        assert client.jsonResponse["count"] == checkpoint["count"]
        assert len(client.jsonResponse["data"]) == checkpoint["data"]

    @allure.testcase("10729 获取策略管理服务所有策略信息--非子域name参数正向检查--返回200 ")
    @pytest.mark.parametrize(argnames="params,checkpoint,remark",
                             argvalues=JsonRead("AS\\Http\\ForwardedPolicyMgntInter\\testdata"
                                                "\\test_GetPolicyMgntAllInfo_name200.json").dict_value_join())
    def test_GetPolicyMgntAllInfo_name200(self, params, checkpoint, remark):
        client = Http_client()
        client.get(url="/api/document-domain-management/v1/policy/general",
                   params=params,
                   header={"Content-Type": "application/json"})
        assert client.status_code == 200
        assert client.jsonResponse["count"] == checkpoint["count"]
        assert len(client.jsonResponse["data"]) == checkpoint["data"]
        if checkpoint["data"] == 2:
            name_list = []
            name_list.append(client.jsonResponse["data"][0]["name"])
            name_list.append(client.jsonResponse["data"][1]["name"])
            assert checkpoint["name1"] in name_list
            assert checkpoint["name2"] in name_list
        elif checkpoint["data"] == 6:
            name_list = []
            name_list.append(client.jsonResponse["data"][0]["name"])
            name_list.append(client.jsonResponse["data"][1]["name"])
            name_list.append(client.jsonResponse["data"][2]["name"])
            name_list.append(client.jsonResponse["data"][3]["name"])
            name_list.append(client.jsonResponse["data"][4]["name"])
            name_list.append(client.jsonResponse["data"][5]["name"])
            assert checkpoint["name1"] in name_list
            assert checkpoint["name2"] in name_list
            assert checkpoint["name3"] in name_list
            assert checkpoint["name4"] in name_list
            assert checkpoint["name5"] in name_list
            assert checkpoint["name6"] in name_list
        else:
            client.jsonResponse["data"][0]["name"] == checkpoint["name"]


    @pytest.mark.medium
    @allure.severity('normal')  # 优先级
    @allure.testcase("10723 获取策略管理服务所有策略信息--非子域mode参数异常检查--返回400")
    @pytest.mark.parametrize(argnames="params,remark",
                             argvalues=JsonRead("AS\\Http\\ForwardedPolicyMgntInter\\testdata"
                                                "\\test_GetPolicyMgntAllInfo400.json").dict_value_join())
    def test_GetPolicyMgntAllInfo400(self, params, remark):
        client = Http_client()
        client.get(url="/api/document-domain-management/v1/policy/general",
                   params=params,
                   header={"Content-Type": "application/json"})
        assert client.status_code == 400
        assert client.jsonResponse["code"] == 400000000
        assert client.jsonResponse["message"] == "Invalid request."
