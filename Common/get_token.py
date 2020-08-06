from requests.auth import HTTPBasicAuth
from Common.readConfig import readconfigs
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from requests import request
from urllib import parse
from requests.exceptions import MissingSchema
import random
import string

disable_warnings(InsecureRequestWarning)


class Token(object):
    def __init__(self, host):
        self.rf = readconfigs(configName="token_config.ini")
        self.cookies = None
        self.host = host
        data = eval(self.rf.get_strValue(section="client_id", option=host))
        # print(data)
        self.client_id = data["client_id"]
        self.client_secret = data["client_secret"]
        self.client_secret = data["client_secret"]
        self.scope = data["scope"]
        self.redirect_uri = data["redirect_uris"][0]

    def registered_client(self):
        """
        注册客户端
        :return:
        """
        json = {
            "grant_types": [
                "authorization_code",
                "implicit",
                "refresh_token"
            ],
            "response_types": [
                "code",
                "token"
            ],
            "scope": "offline root_readonly manage_managed_users",
            "redirect_uris": [
                "https://127.0.0.1:8000/api_test/callback"
            ],
            "client_name": "api_test"
        }
        res = request(method="POST", url="https://" + self.host + "/oauth2/clients", json=json, verify=False,
                      allow_redirects=False)
        if res.status_code == 201:
            # rf = readconfigs(configName="token_config.ini")
            self.rf.set_option_value(section="client_id", option=self.host, value=str(res.json()))
            data = eval(self.rf.get_strValue(section="client_id", option=self.host))
            # print(data)
            self.client_id = data["client_id"]
            self.client_secret = data["client_secret"]
            self.client_secret = data["client_secret"]
            self.scope = data["scope"]
            self.redirect_uri = data["redirect_uris"][0]
        else:
            print(getattr(self.registered_client, "__name__"), res.status_code, res.content)

    def authorizing_users(self):
        """
        授权用户
        :return:
        """
        params = {"client_id": self.client_id,
                  "response_type": "code",
                  "scope": self.scope,
                  "redirect_uri": self.redirect_uri,
                  "state": ''.join(random.sample(string.ascii_letters, 24))}

        res = request(method="POST", url="https://" + self.host + "/oauth2/auth", params=params,
                      verify=False,
                      allow_redirects=False)
        if res.status_code == 302:
            # print(res.content)
            self.cookies = res.cookies
            return res.headers["Location"].split("=")[-1]
        else:
            print(getattr(self.authorizing_users, "__name__"), res.status_code, res.content)

    def request_login(self):
        """
        获取登录请求
        :return:
        """
        login_challenge = self.authorizing_users()
        params = {"login_challenge": login_challenge}
        res = request(method="GET", url="http://" + self.host + ":9080/oauth2/auth/requests/login", params=params,
                      verify=False, cookies=self.cookies,
                      allow_redirects=False)
        if res.status_code == 200:
            # print(res.content)
            return login_challenge
        else:
            print(getattr(self.request_login, "__name__"), res.status_code, res.content)

    def accept_login_request(self):
        """
        #接受登陆请求
        :return:
        """
        login_challenge = self.request_login()
        params = {"login_challenge": login_challenge}
        json = {
            "acr": "string",
            "context": {
                "udid": "",
                "visitor_type": "realname",
                "client_type": "web",
                "account_type": "other",
                "login_ip": "127.0.0.1"
            },
            "remember": True,
            "remember_for": 3600,
            "subject": "266c6a42-6131-4d62-8f39-853e7093701c"
        }
        res = request(method="PUT", url="http://" + self.host + ":9080/oauth2/auth/requests/login/accept",
                      params=params, json=json,
                      verify=False, cookies=self.cookies,
                      allow_redirects=False)
        if res.status_code == 200:
            # print(res.content)
            return res.json()["redirect_to"]
        else:
            # self.registered_client()
            print(getattr(self.accept_login_request, "__name__"), res.status_code, res.content)

    def get_auth_redirect_to(self):
        """
        #获取授权
        :return:
        """
        try:
            redirect_to = self.accept_login_request()
            res = request(method="GET", url=redirect_to,
                          verify=False, cookies=self.cookies,
                          allow_redirects=False)
        except MissingSchema:
            self.registered_client()
            redirect_to = self.accept_login_request()
            res = request(method="GET", url=redirect_to,
                          verify=False, cookies=self.cookies,
                          allow_redirects=False)

        if res.status_code == 302:
            self.cookies = res.cookies
            # print(res.headers)
            return res.headers["Location"].split("=")[-1]
        else:
            print(getattr(self.get_auth_redirect_to, "__name__"), res.status_code, res.content)

    def get_auth_request(self):
        """
        #获取授权请求
        :return:
        """
        consent_challenge = self.get_auth_redirect_to()
        # print(consent_challenge)
        params = {"consent_challenge": consent_challenge}
        res = request(method="GET", url="http://" + self.host + ":9080/oauth2/auth/requests/consent", params=params,
                      verify=False, cookies=self.cookies,
                      allow_redirects=False)
        if res.status_code == 200:
            return res.json(), consent_challenge
        else:
            print(getattr(self.get_auth_request, "__name__"), res.status_code, res.content)

    def accept_auth_request(self):
        """
        #接受授权请求
        :return:
        """
        auth_data = self.get_auth_request()
        consent_challenge = auth_data[1]
        params = {"consent_challenge": consent_challenge}
        json = {
            "grant_access_token_audience": [
                "string"
            ],
            "grant_scope": auth_data[0]["requested_scope"],
            "remember": True,
            "remember_for": 0,
            "session": {
                "access_token": auth_data[0]["context"],
                "id_token": {}
            }
        }
        res = request(method="PUT", url="http://" + self.host + ":9080/oauth2/auth/requests/consent/accept",
                      params=params, cookies=self.cookies,
                      json=json, verify=False,
                      allow_redirects=False)
        if res.status_code == 200:
            # self.cookies=res.cookies
            return res.json()["redirect_to"]
        else:
            print(getattr(self.accept_auth_request, "__name__"), res.status_code, res.content)

    def get_code(self):
        """
        #获取implicit token GetCode
        :return:
        """
        redirect_to = self.accept_auth_request()
        parse.unquote(redirect_to)
        # print(self.cookies)
        res = request(method="GET", url=parse.unquote(redirect_to), cookies=self.cookies, verify=False,
                      allow_redirects=False)
        if res.status_code == 302:
            # print(res.headers)
            return res.headers["Location"].split("&")[0].split("=")[-1]
        else:
            print(getattr(self.get_code, "__name__"), res.status_code, res.content)

    def get_token(self):
        """
        #申请令牌
        :return:
        """
        code = self.get_code()
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        res = request(method="POST", url="https://" + self.host + "/oauth2/token", verify=False, data=data,
                      allow_redirects=False, headers={"Content-Type": "application/x-www-form-urlencoded"},
                      auth=HTTPBasicAuth(self.client_id, self.client_secret))
        if res.status_code == 200:
            return res.json()
        else:
            print(getattr(self.get_token, "__name__"), res.status_code, res.content)


if __name__ == '__main__':
    # 只能用vip去获取token 主机IP获取token会失败
    print(Token(host="10.2.176.176").get_token())
    # def is_odd(n):
    #     return n % 2 == 1
    #
    #
    # print(filter(is_odd, [1, 2, 3, 4, 5, 6]))
