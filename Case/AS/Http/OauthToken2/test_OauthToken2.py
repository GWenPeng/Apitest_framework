# coding=utf-8
import pytest
import allure
import requests
import json
from Common.readjson import JsonRead
from Common.readConfig import readconfigs
from Common.http_request import Http_client


@pytest.mark.ASP_4668
@pytest.mark.medium
@allure.severity('normal')  # 优先级
@allure.feature("服务间增加oauth认证")
class Test_OauthToken2(object):
    # 读取config文件信息
    readconfig = readconfigs()
    host = readconfig.get_http(tagname="HTTP", name='baseUrl')

    @allure.testcase("该用例覆盖：header不包含token；header包含无效token；header包含有效但超时token")
    @pytest.mark.parametrize(argnames="url,header,method,params,data,json,remark",
                             argvalues=JsonRead("AS/Http/OauthToken2/"
                                                "testdata/OauthToken2_domain.json").dict_value_join())
    def test_domain_oauth2_token401(self, url, header, method, params, data, json, remark):
        # header不包含token
        if "跳过" in remark:
            pytest.skip(msg=remark.split(",")[-1])
        if "http" in url:
            url = url
        else:
            url = self.host + url
        res_notoken = requests.request(method=method, url=url, headers=header, params=params, data=data,
                                       json=json,
                                       verify=False)
        assert res_notoken.json()["code"] == 401014000
        assert res_notoken.json()["message"] == "Unauthorization."
        assert res_notoken.json()["cause"] == "access_token empty"

        # header包含无效token
        header_oauth = {"Content-Type": "application/json", "Authorization": "Bearer 11"}
        res_invalidtoken = requests.request(method=method, url=url, headers=header_oauth, params=params,
                                            data=data,
                                            json=json, verify=False)
        assert res_invalidtoken.json()["code"] == 401014000
        assert res_invalidtoken.json()["message"] == "Unauthorization."
        assert res_invalidtoken.json()["cause"] == "access_token does not active"

        # header包含有效但超时token
        header_oauth_1 = {"Content-Type": "application/json",
                          "Authorization": "Bearer MzQAS0KuqrAjXxPYyEakUms-yisdXLsnblqf_rkJinY.-Z"
                                           "-ZHsECEwKqmbTYjqpRy2g9Z-I9yfHggMrQNZoIrn4"}
        res_auth2 = requests.request(method=method, url=url, headers=header_oauth_1, params=params,
                                     data=data, json=json, verify=False)

        assert res_auth2.json()["code"] == 401014000
        assert res_auth2.json()["message"] == "Unauthorization."
        assert res_auth2.json()["cause"] == "access_token does not active"

    @pytest.mark.parametrize("url,header,method,params,data,json,remark",
                             argvalues=JsonRead(
                                 "AS/Http/OauthToken2/testdata/OauthToken2_policy.json").dict_value_join())
    def test_policy_oauth2_token401(self, url, header, method, params, data, json, remark):
        # header不包含token
        if "跳过" in remark:
            pytest.skip(msg=remark.split(",")[-1])
        if "http" in url:
            url = url
        else:
            url = self.host + url
        res_notoken = requests.request(method=method, url=url, headers=header, params=params, data=data,
                                       json=json,
                                       verify=False)
        assert res_notoken.json()["code"] == 401013000
        assert res_notoken.json()["message"] == "Unauthorization."
        assert res_notoken.json()["cause"] == "access_token empty"

        # header包含无效token
        header_oauth = {"Content-Type": "application/json", "Authorization": "Bearer 11"}
        res_invalidtoken = requests.request(method=method, url=url, headers=header_oauth, params=params,
                                            data=data,
                                            json=json, verify=False)
        assert res_invalidtoken.json()["code"] == 401013000
        assert res_invalidtoken.json()["message"] == "Unauthorization."
        assert res_invalidtoken.json()["cause"] == "access_token does not active"

        # header包含有效但超时token
        header_oauth_1 = {"Content-Type": "application/json",
                          "Authorization": "Bearer 06xzzIBHg4OaJR1drP6rG3K1JmEebDBSqcPigsQVykk."
                                           "hIomct7lQd2BvaUsXZGjdeUCtuCezrh3Fm01U-vxOzE"}
        res_auth2 = requests.request(method=method, url=url, headers=header_oauth_1, params=params,
                                     data=data, json=json, verify=False)

        assert res_auth2.json()["code"] == 401013000
        assert res_auth2.json()["message"] == "Unauthorization."
        assert res_auth2.json()["cause"] == "access_token does not active"

    @pytest.mark.parametrize("url,header,method,params,data,json,remark",
                             argvalues=JsonRead(
                                 "AS/Http/OauthToken2/testdata/OauthToken2_domain.json").dict_value_join())
    def test_domain_oauth2_token403(self, url, header, method, params, data, json, remark):
        # 获取token
        token_url = "/oauth2/token"
        data = {"grant_type": "client_credentials"}
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        auth = ("1b699d07-c495-49a1-a167-0f27592d6b32", "-f5SpjenQ1zV")
        r = requests.request(method='POST', url=self.host + token_url, data=data, headers=header, auth=auth, verify=False)
        token = (eval(r.content.decode()))["access_token"]
        header_oauth = {"Content_Type": "application/json",
                        "Authorization": "Bearer " + token}
        res = requests.request(method=method, url=self.host + url, headers=header_oauth, params=params,
                               data=data, json=json, verify=False)
        assert res.json()["code"] == 403014000
        assert res.json()["message"] == "No permission to do this operation."
        assert res.json()["cause"] == "client_id does not match"

    @pytest.mark.parametrize("url,header,method,params,data,json,remark",
                             argvalues=JsonRead(
                                 "AS/Http/OauthToken2/testdata/OauthToken2_policy.json").dict_value_join())
    def test_policy_oauth2_token403(self, url, header, method, params, data, json, remark):
        # 获取token
        token_url = "/oauth2/token"
        data = {"grant_type": "client_credentials"}
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        auth = ("1b699d07-c495-49a1-a167-0f27592d6b32", "-f5SpjenQ1zV")
        r = requests.request(method='POST', url=self.host + token_url, data=data, headers=header, auth=auth,
                             verify=False)
        token = (eval(r.content.decode()))["access_token"]
        header_oauth = {"Content_Type": "application/json",
                        "Authorization": "Bearer " + token}
        res = requests.request(method=method, url=self.host + url, headers=header_oauth, params=params,
                               data=data, json=json, verify=False)
        assert res.json()["code"] == 403013000
        assert res.json()["message"] == "No permission to do this operation."
        assert res.json()["cause"] == "client_id does not match"
