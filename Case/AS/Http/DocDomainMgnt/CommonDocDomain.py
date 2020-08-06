import allure
from Common.get_token import Token
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect
from functools import lru_cache
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt
from pymysql.err import OperationalError


@lru_cache()
def get_token(host="10.2.176.245"):
    access_token = Token(host=host).get_token()["access_token"]
    return access_token


class CommonDocDomain(object):
    @allure.step("修改本域类型")
    def setSelfDomain(self, host="10.2.176.208", domaintype="parallel", fatherdomain="10.2.176.245"):
        """

        :param fatherdomain: 父域域名或ip
        :param host: 本域域名或ip
        :param domaintype: 本域类型
        :return: None
        """
        if host == "10.2.176.245":
            header = {"Content-Type": "application/json"}
        else:
            token = get_token(host=host)
            header = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        client = Http_client(tagname="HTTPGWP")
        client.put(url="https://" + host + ":443/api/document-domain-management/v1/domain/self/type",
                   header=header,
                   json={"type": domaintype, "host": fatherdomain})
        assert client.status_code == 200

    @allure.step("查询本域的详情")
    def getSelfDomain(self, host):
        """

        :param host: 本域域名或ip
        :return:jsonResponse
        """
        if host == "10.2.176.245":
            header = {"Content-Type": "application/json"}
        else:
            token = get_token(host=host)
            header = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        client = Http_client(tagname="HTTPGWP")
        client.get(url="https://" + host + ":443/api/document-domain-management/v1/domain/self",
                   header=header)
        assert client.status_code == 200
        return client.jsonResponse

    @allure.step("查询关系域的详情")
    def getRelationDomain(self, uuid, host="10.2.176.245"):
        """

        :param host:
        :param uuid: 关系域UUID
        :return:jsonResponse
        """
        if host == "10.2.176.245":
            header = {"Content-Type": "application/json"}
        else:
            token = get_token(host=host)
            header = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        client = Http_client(tagname="HTTPGWP")
        client.get(url="https://" + host + ":443/api/document-domain-management/v1/domain/" + uuid,
                   header=header)
        # print(client.jsonResponse)
        assert client.status_code == 200
        return client.jsonResponse

    @allure.step("查询关系域列表")
    def getRelationDomainList(self, host="10.2.176.245", keyword="", offset=0, limit=1000):
        """

        :param limit: 获取数据量，默认20;如果limit为-1，则获取所有数据;如果limit小于-1，则忽略该参数，使用默认值;如果limit大于200，则设置为200
        :param offset:获取数据起始下标，0开始，默认0;如果offset小于0，则忽略该参数，使用默认值;如果offset大于数据总数，则返回空列表
        :param keyword:搜索的关键字，可以为关系域域名，支持模糊搜索； 如果不填，返回所有结果
        :param host: 本域域名或ip
        :return:jsonResponse
        """
        if host == "10.2.176.245":
            header = {"Content-Type": "application/json"}
        else:
            token = get_token(host=host)
            header = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        client = Http_client(tagname="HTTPGWP")
        client.get(
            url="https://" + host + ":443/api/document-domain-management/v1/domain",
            params={"keyword": keyword, "offset": offset, "limit": limit},
            header=header)
        if client.status_code == 200:
            return client.jsonResponse
        else:
            return client.status_code

    @allure.step("删除关系域")
    def delRelationDomain(self, host="10.2.176.245", uuid=""):
        """

        :param uuid: 关系域的id
        :param host: 关系域域名或ip
        :return:None
        """
        if host == "10.2.176.245":
            header = {"Content-Type": "application/json"}
        else:
            token = get_token(host=host)
            header = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        client = Http_client(tagname="HTTPGWP")
        res = CommonDocDomain().getRelationDomain(uuid=uuid, host=host)
        if res["port"] != 443:
            client.put(url="/api/document-domain-management/v1/domain/" + res["id"],
                       header={"Content-Type": "application/json"},
                       json={"type": res["type"], "port": 443, "credential_id": "appid", "credential_key": "appkey"})
        client.delete(url="https://" + host + ":443/api/document-domain-management/v1/domain/" + uuid,
                      header=header)
        # assert client.status_code == 200
        if client.status_code == 409:
            assert client.jsonResponse["code"] == 409014000
            assert client.jsonResponse["message"] == "Conflict resource."
        return client.status_code

    @allure.step("添加关系域")
    def addRelationDomain(self, host, port=443, domaintype="child", credential_id=None,
                          credential_key=None, httphost="10.2.176.245", network_type="direct"):
        """
        默认添加子域为关系域
        :param network_type:
        :param httphost: http的域
        :param credential_key:
        :param credential_id:
        :param port:
        :param domaintype: 域类型 child or parallel
        :param host: 域名或者ip
        :return:添加成功的关系域uuid
        """
        if network_type == "direct" or domaintype == "child":
            if host == "child.eisoo.com":
                CommonDocDomain.del_invalid_credential(host="10.2.176.208", domain_type=domaintype)
                if credential_id is None and credential_key is None:
                    credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(host="10.2.176.208",
                                                                                              credential_type=domaintype)
            elif host == "parallel.eisoo.com":
                CommonDocDomain.del_invalid_credential(host="10.2.180.162", domain_type=domaintype)
                if credential_id is None and credential_key is None:
                    credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(host="10.2.180.162",
                                                                                              credential_type=domaintype)
            elif credential_id is None and credential_key is None:
                CommonDocDomain.del_invalid_credential(host=host, domain_type=domaintype)
                credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(host=host,
                                                                                          credential_type=domaintype)
        elif network_type == "indirect" and domaintype == "parallel":
            if credential_id is None and credential_key is None:
                credential_id = "credential_id"
                credential_key = "credential_id"

        if httphost == "10.2.176.245":
            header = {"Content-Type": "application/json"}
        else:
            token = get_token(host=httphost)
            header = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        client = Http_client(tagname="HTTPGWP")
        client.post(url="https://" + httphost + ":443/api/document-domain-management/v1/domain/",
                    header=header,
                    jsondata={"host": host, "port": port, "type": domaintype, "credential_id": credential_id,
                              "credential_key": credential_key,
                              "network_type": network_type})
        # print(httphost, host, domaintype)
        # print(client.jsonResponse)
        try:
            assert client.status_code == 201
            location = client.respheaders['Location']
            uuid = location.split("/")[-1]
            return uuid, credential_id, credential_key
        except AssertionError as e:
            print("状态码：%s,ResponseBody:%s" % (client.status_code, client.jsonResponse))
            raise e

    @allure.step("递归清除所有的关系域")
    def clearRelationDomain(self, host=None):
        """
        :param host:要清除的本域域名或IP
        :return: None
        """
        if host is None:
            host = ["10.2.176.245"]
        if isinstance(host, str):
            host = [host]
        for Host in host:
            L = CommonDocDomain().getRelationDomainList(host=Host)
            if isinstance(L, int):
                print(L)
            elif len(L["data"]) != 0:
                for index in range(len(L["data"])):
                    CommonDocDomain().delRelationDomain(host=Host, uuid=L["data"][index]["id"])
        return None

    @allure.step("设置关系域详情")
    def setRelationDomain(self, uuid, domaintype="parallel", port=443, credential_id="admin",
                          credential_key="eisoo.com", secret=""):
        """
        :param secret:传输密钥
        :param domaintype:关系域类型，可填：child, parallel
        :param credential_id:credential_id，可为任何不为空的字符串
        :param credential_key:credential_key，可为任何不为空字符串
        :param port:关系域端口，必须大于等于1，小于等于65535；
        :param uuid:关系域uuid
        :return:None
        """
        # token = get_token()
        if domaintype == "parallel":
            data = {"type": domaintype, "port": port, "credential_id": credential_id, "credential_key": credential_key,
                    "secret": secret}
        else:
            data = {"type": domaintype, "port": port, "credential_id": credential_id, "credential_key": credential_key}
        client = Http_client(tagname="HTTPGWP")
        client.put(url="/api/document-domain-management/v1/domain/" + uuid,
                   header={"Content-Type": "application/json"}, json=data)
        assert client.status_code == 200
        return None

    @allure.step("获取策略列表")
    def getPolicyList(self, httphost="10.2.176.245", key_word="", offset=0, limit=1000):
        """

        :param offset:
        :param limit:
        :param httphost:
        :param key_word:
        :return:
        """
        if httphost == "10.2.176.245":
            header = {"Content-Type": "application/json"}
        else:
            token = get_token(host=httphost)
            header = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        client = Http_client(tagname="HTTPGWP")
        client.get(url="https://" + httphost + ":443/api/document-domain-management/v1/policy-tpl",
                   params={"key_word": key_word, "offset": offset, "limit": limit},
                   header=header)
        return client.jsonResponse

    @allure.step("新增策略")
    def addPolicy(self, httphost="10.2.176.245", content=None, name="PolicyName"):
        """

        :param content:
        :param name:
        :param httphost:
        :return:
        """
        if httphost == "10.2.176.245":
            header = {"Content-Type": "application/json"}
        else:
            token = get_token(host=httphost)
            header = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        if content is None:
            content = [{"name": "password_strength_meter", "value": {"enable": True, "length": 8}}]
        client = Http_client(tagname="HTTPGWP")
        client.post(url="https://" + httphost + ":443/api/document-domain-management/v1/policy-tpl",
                    jsondata={"content": content, "name": name},
                    header=header)
        print(client.jsonResponse)
        location = client.respheaders['Location']
        uuid = location.split("/")[-1]
        return uuid

    @allure.step("子域绑定策略")
    def BoundPolicy(self, httphost="10.2.176.245", PolicyUUID=None, ChildDomainUUID=None):
        """

        :param ChildDomainUUID:
        :param PolicyUUID:
        :param httphost:
        :return:
        """
        if httphost == "10.2.176.245":
            header = {"Content-Type": "application/json"}
        else:
            token = get_token(host=httphost)
            header = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        client = Http_client(tagname="HTTPGWP")
        client.put(
            url="https://" + httphost + ":443/api/document-domain-management/v1/policy-tpl/" + PolicyUUID + "/bound-domain/" + ChildDomainUUID,
            header=header)
        return client.status_code

    @allure.step("子域解除策略绑定")
    def delboundPolicy(self, httphost="10.2.176.245", PolicyUUID=None, ChildDomainUUID=None):
        """

        :param ChildDomainUUID:
        :param PolicyUUID:
        :param httphost:
        :return:
        """
        if httphost == "10.2.176.245":
            header = {"Content-Type": "application/json"}
        else:
            token = get_token(host=httphost)
            header = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        client = Http_client(tagname="HTTPGWP")
        client.delete(
            url="https://" + httphost + ":443/api/document-domain-management/v1/policy-tpl/" + PolicyUUID + "/bound-domain/" + ChildDomainUUID,
            header=header)
        return client.status_code

    @allure.step("获取已绑定策略的子域")
    def getBoundPolicyChild(self, httphost="10.2.176.245", ChildDomainUUID=None):
        """

        :param ChildDomainUUID:
        :param httphost:
        :return:
        """
        if httphost == "10.2.176.245":
            header = {"Content-Type": "application/json"}
        else:
            token = get_token(host=httphost)
            header = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        client = Http_client(tagname="HTTPGWP")
        client.get(
            url="https://" + httphost + ":443/api/document-domain-management/v1/domain/" + ChildDomainUUID + "/bound-policy-tpl",
            header=header)
        return client.jsonResponse

    @allure.step("获取策略已绑定的子文档域")
    def getPolicyChildDomainList(self, httphost="10.2.176.245", policyuuid=None):
        """

        :param httphost:
        :param policyuuid:
        :return:
        """
        if httphost == "10.2.176.245":
            header = {"Content-Type": "application/json"}
        else:
            token = get_token(host=httphost)
            header = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        client = Http_client(tagname="HTTPGWP")
        client.get(
            url="https://" + httphost + ":443/api/document-domain-management/v1/policy-tpl/" + policyuuid + "/bound-domain?offset=0&limit"
                                                                                                            "=1000 "
                                                                                                            "&key_word=",
            header=header)
        return client.jsonResponse

    @allure.step("清空绑定子域策略")
    def clearBoundPolicyChild(self, httphost, policyuuid):
        """

        :param httphost:
        :param policyuuid:
        :return:
        """
        res = CommonDocDomain().getPolicyChildDomainList(httphost=httphost, policyuuid=policyuuid)
        if len(res["data"]) != 0:
            for index in range(len(res["data"])):
                CommonDocDomain().delboundPolicy(httphost=httphost, PolicyUUID=policyuuid,
                                                 ChildDomainUUID=res["data"][index]["id"])
        return None

    @allure.step("获取同步计划列表")
    def getSynchronizationPlanList(self, httphost="10.2.176.245", offset="0", limit="1000", key_word=""):
        """

        :return:
        """
        if httphost == "10.2.176.245":
            header = {"Content-Type": "application/json"}
        else:
            token = get_token(host=httphost)
            header = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        client = Http_client(tagname="HTTPGWP")
        client.get(
            url="https://" + httphost + ":443/api/document-domain-management/v1/library-sync?offset=" + offset +
                "&limit=" + limit + "&key_word=" + key_word,
            header=header)
        return client.jsonResponse

    @allure.step("创建文档库同步计划")
    def creatSynchronizationPlan(self, httphost="10.2.176.245", jsondata=None, mode="live", docid=None, domainid=None,
                                 libname=None):
        """

        :param libname:
        :param domainid:
        :param docid:
        :param mode:
        :param httphost:
        :param jsondata:
        :return:
        ''"""
        if httphost == "10.2.176.245":
            header = {"Content-Type": "application/json"}
        else:
            token = get_token(host=httphost)
            header = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        if jsondata is None:
            jsondata = {"interval": {"mode": mode}, "source": {"id": docid},
                        "target": {"domain": {"id": domainid}, "library": libname}}
        client = Http_client(tagname="HTTPGWP")
        client.post(url="https://" + httphost + ":443/api/document-domain-management/v1/library-sync",
                    jsondata=jsondata,
                    header=header)
        return client.jsonResponse

    @staticmethod
    def del_invalid_credential(host, domain_type="child"):
        """
        删除无效的认证凭据
        :return:
        """
        try:
            db = DB_connect(host=host)
            db.delete(
                'DELETE from domain_mgnt.t_self_credentials where f_type="%s" and f_status in ("invalid","unused");' % domain_type)
            db.close()
        except OperationalError:
            print(host + "连接超时")

    @staticmethod
    def get_credential(host, domain_type="child", f_status="used"):
        """

        :param f_status:
        :param host:
        :param domain_type:
        :return:
        """
        db = DB_connect(host=host)

        if f_status == "invalid":
            credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(host=host,
                                                                                      credential_type=domain_type)
            db.update('UPDATE  domain_mgnt.t_self_credentials  set  f_status="invalid" where  f_credential_id="%s" '
                      'and f_credential_key="%s" and  f_type="%s";' % (credential_id, credential_key, domain_type))

        rs = db.select_one('SELECT * from domain_mgnt.t_self_credentials where f_type="%s" and f_status="%s";' % (
            domain_type, f_status))
        db.close()
        return rs


if __name__ == '__main__':
    CommonDocDomain.del_invalid_credential(host="10.2.176.208", domain_type="child")
