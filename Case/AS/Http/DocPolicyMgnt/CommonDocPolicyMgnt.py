# -*- coding = utf-8 -*-
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect
from Common.readConfig import readconfigs
from Common.get_token import Token
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt


class CommonDocPolicyMgnt:
    def get_token(self, host):
        access_token = Token(host=host).get_token()["access_token"]
        return access_token

    # 获取策略id
    def getStrategyId(self):
        db = DB_connect()
        strategyIds = db.select_one('select f_id from domain_mgnt.t_policy_tpls')
        db.close()
        if strategyIds is not None:
            for strategyId in strategyIds:
                url = strategyId
            return url
        else:
            client = Http_client()
            client.post(url='/api/document-domain-management/v1/policy-tpl/',
                        jsondata="{\"content\":[{\"name\":\"password_strength_meter"
                                 "\",\"value\":{\"enable\":False,\"length\":8}}],"
                                 "\"name\":\"this is a strategy\"}",
                        header="{\"Content-Type\":\"application/json\"}")
            StrategyDB = DB_connect()
            strIds = StrategyDB.select_one('select f_id from domain_mgnt.t_policy_tpls')
            for strId in strIds:
                url = strId
            return url

    def addDocDoamin(self, strategyId, father_host=None , child_host1=None, child_host2=None):
        # 添加子文档域
        db = DB_connect()
        sql = "insert into domain_mgnt.t_relationship_domain values" \
              "('9b04d18d-6c15-45a6-8c8c-6b8dc67a8681','domain.com',443,'','','child','direct','ad','ei',now(),'111')," \
              "('9b04d18d-6c15-45a6-8c8c-6b8dc67a8682','爱数',443,'','','child','direct','ad','ei',now(),'222')," \
              "('9b04d18d-6c15-45a6-8c8c-6b8dc67a8683','eio@!@.com',443,'','','child','direct','ad','ei',now(),'333')," \
              "('9b04d18d-6c15-45a6-8c8c-6b8dc67a8684','{child_host1}',443,'','','child','direct','ad','ei',now(),'4')," \
              "('9b04d18d-6c15-45a6-8c8c-6b8dc67a8686','{child_host2}',443,'','','child','direct','ad','ei',now(),'5')," \
              "('9b04d18d-6c15-45a6-8c8c-6b8dc67a8685','111',443,'','','child','direct','ad','ei',now(),'666')"
        insertSql = sql.format(child_host1=child_host1, child_host2=child_host2)
        db.insert(insertSql)
        # 绑定子文档域
        for i in range(6):
            ids = str(strategyId)
            domainId = '9b04d18d-6c15-45a6-8c8c-6b8dc67a868' + str(i + 1)
            insertDomain = "insert into domain_mgnt.t_policy_tpl_domains values('{}','{}')"
            domainSql = insertDomain.format(ids, domainId)
            db.insert(domainSql)
            i + 1
        db.close()

    def selectStrategyState(self, f_name):
        db = DB_connect()
        selectLocked = "select f_locked from policy_mgnt.t_policies where f_name='{}'"
        sql = selectLocked.format(f_name)
        locks = db.select_one(sql)
        for lock in locks:
            lk = lock
        return lk

        # 新增策略配置

    def AddPolicy(self, jsondata):
        add_client = Http_client()
        add_client.post(url="/api/document-domain-management/v1/policy-tpl", jsondata=jsondata,
                        header="{\"Content-Type\":\"application/json\"}")
        if add_client.status_code == 201:
            policyid = add_client.respheaders['Location'].split('/')[-1]
            return policyid
        else:
            print(add_client.jsonResponse)

    # 搜索策略配置
    def SearchPolicy(self, jsondata):
        search_client = Http_client()
        search_client.get(url="/api/doc-domain/v1/policy-tpl", params=eval(jsondata),
                          header="{\"Content-Type\":\"application/json\"}")
        if search_client.status_code == 201:
            return search_client.jsonResponse
        else:
            pass

    # 删除策略配置
    def DeletePolicy(self, id):
        delete_client = Http_client()
        deleteurl = "/api/document-domain-management/v1/policy-tpl/%s" % id
        delete_client.delete(url=deleteurl, header='{\"Content-Type\":\"application/json\"}')
        if delete_client.status_code != 200:
            print(delete_client.jsonResponse)
        else:
            assert delete_client.status_code == 200

    # 添加子域1
    def AddChildDomain1(self, father_host="10.2.176.176", child_host="10.2.176.208", credential_id="xx",
                        credential_key="yy"):
        client = Http_client()
        post_url = "https://" + "{host}/api/document-domain-management/v1/domain".format(host=father_host)
        client.post(url=post_url,
                    header='{"Content-Type":"application/json"}',
                    jsondata={"host": child_host, "port": 443, "type": "child", "credential_id": credential_id,
                              "credential_key": credential_key})
        assert client.status_code == 201
        location = client.respheaders['Location']
        uuid = location.split("/")[-1]
        return uuid

    # 添加子域2
    def AddChildDomain2(self, father_host="10.2.176.176", child_host="10.2.180.162", credential_id="xx",
                        credential_key="yy"):
        client = Http_client()
        post_url = "https://" + "{host}/api/document-domain-management/v1/domain".format(host=father_host)
        client.post(url=post_url,
                    header='{"Content-Type":"application/json"}',
                    jsondata={"host": child_host, "port": 443, "type": "child", "credential_id": credential_id,
                              "credential_key": credential_key})
        assert client.status_code == 201
        location = client.respheaders['Location']
        uuid = location.split("/")[-1]
        return uuid

    # 绑定策略和子域
    def BindChildDomain(self, id, domain1=None, domain2=None):
        bind_child = Http_client()
        if domain2 == None:
            bindurl = "/api/document-domain-management/v1/policy-tpl/%s/bound-domain/%s" % (id, domain1)
        else:
            bindurl = "/api/document-domain-management/v1/policy-tpl/%s/bound-domain/%s,%s" % (id, domain1, domain2)
        bind_child.put(url=bindurl, header='{"Content-Type":"application/json"}')
        assert bind_child.status_code == 200

    # 应用策略
    def ApplyPolicy(self, id, domain1=None, domain2=None):
        apply_client = Http_client()
        if domain2 == None:
            applyurl = "/api/doc-domain/v1/policy-tpl/%s/bound-domain/%s/policy" % (id, domain1)
        else:
            applyurl = "/api/doc-domain/v1/policy-tpl/%s/bound-domain/%s,%s/policy" % (id, domain1, domain2)
        apply_client.put(url=applyurl, header='{"Content-Type":"application/json"}')
        if apply_client != 200:
            print(apply_client.jsonResponse)
        else:
            assert apply_client.status_code == 200

    # 编辑策略
    def EditPolicy(self, host=None, id=None, jsondata=None):
        edit_client = Http_client()
        # 策略id到编辑策略的path路径中
        editurl = "https://" + "{ip}/api/document-domain-management/v1/policy-tpl/{policy_id}".format(ip=host, policy_id=id)
        # 将编辑数据的json字符串转为字典格式
        dic_jsondata = eval(jsondata[0])
        edit_client.put(url=editurl, json=dic_jsondata, header='{"Content-Type":"application/json"}')
        assert edit_client.status_code == 200

    # 获取文档域策略详细配置
    def GetPolicyDetail(self, id):
        client = Http_client()
        # 策略id到编辑策略的path路径中
        url = "/api/document-domain-management/v1/policy-tpl/%s" % (id)
        client.get(url=url, header='{"Content-Type":"application/json"}')
        assert client.status_code == 200
        return client.jsonResponse

    # 解绑子文档域
    def DeleteChildDomain(self, host=None, id=None, domain1=None, domain2=None):
        client = Http_client()
        if domain2 == None:
            deleteurl = "https://" + "{ip}/api/document-domain-management/v1/" \
                                     "policy-tpl/{policy_id}/bound-domain/{domain_id}".format(ip=host, policy_id=id, domain_id=domain1)
        else:
            deleteurl = "https://" + "{ip}/api/document-domain-management/v1/" \
                                     "policy-tpl/{policy_id}/bound-domain/{domain_id1},{domain_id2}".format(ip=host, policy_id=id, domain_id1=domain1, domain_id2=domain2)
        client.delete(url=deleteurl, header='{"Content-Type":"application/json"}')
        assert client.status_code == 200

    # 获取所有策略信息
    def GetAllPolicyInfo(self, host=None):
        if host == None:
            client = Http_client()
            client.get(url="/api/policy-management/v1/general", header='{"Content-Type":"application/json"}')
            assert client.status_code == 200
            return client.jsonResponse
        else:
            token = self.get_token(host=host)
            client = Http_client()
            get_url = "https://" + "{host}/api/policy-management/v1/general".format(host=host)
            client.get(url=get_url, header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
            assert client.status_code == 200
            return client.jsonResponse

    # 获取与文档域绑定的策略配置
    def GetBindedPolicy(self, domain):
        client = Http_client()
        bindedurl = "/api/document-domain-management/v1/domain/%s/bound-policy-tpl" % (domain)
        client.get(url=bindedurl, header='{"Content-Type":"application/json"}')
        assert client.status_code == 200
        return client.jsonResponse
