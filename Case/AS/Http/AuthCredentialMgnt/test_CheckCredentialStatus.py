import pytest
import allure
from Common.http_request import Http_client
from DB_connect.mysqlconnect import DB_connect
from Common.readjson import JsonRead
from Case.AS.Http.AuthCredentialMgnt.CommonAuthCredentialMgnt import CommonAuthCredentialMgnt
from Case.AS.Http.DocPolicyMgnt.CommonDocPolicyMgnt import CommonDocPolicyMgnt
from Case.AS.Http.DocDomainMgnt.CommonDocDomain import CommonDocDomain


@pytest.mark.ASP_4581
@pytest.mark.high
@allure.feature("认证凭据管理")
class Test_CreateCredential201(object):
    @allure.testcase("11105 认证凭据status和bind_domain信息检查")
    @pytest.fixture(scope="function")
    def create_credential(self, metadata_host):
        father_host = metadata_host["self.eisoo.com"]
        child_host = metadata_host["child.eisoo.com"]
        parallel_host = metadata_host["replace.eisoo.com"]
        father_host = (father_host.split(":")[1]).strip("/")
        child_host = (child_host.split(":")[1]).strip("/")
        parallel_host = (parallel_host.split(":")[1]).strip("/")
        # 获取子域/平级域凭据
        result1 = CommonAuthCredentialMgnt().get_credential(host=child_host, credential_type="child")
        credential_id1 = result1[0]
        credential_key1 = result1[1]
        result2 = CommonAuthCredentialMgnt().get_credential(host=parallel_host)
        credential_id2 = result2[0]
        credential_key2 = result2[1]
        yield credential_id1, credential_id2, credential_key1, credential_key2, father_host, child_host, parallel_host
        CommonAuthCredentialMgnt().del_credential(host=child_host, credential_id=credential_id1)
        CommonAuthCredentialMgnt().del_credential(host=parallel_host, credential_id=credential_id2)

    def test_CheckCredentialStatus(self, create_credential):
        credential_id1 = create_credential[0]
        credential_id2 = create_credential[1]
        credential_key1 = create_credential[2]
        credential_key2 = create_credential[3]
        father_host = create_credential[4]
        child_host = create_credential[5]
        parallel_host = create_credential[6]
        get_sql = "select f_status,f_bind_domain from " \
                  "domain_mgnt.t_self_credentials where f_credential_id='%s'" % credential_id1
        db = DB_connect(host=child_host)
        result = db.select_all(get_sql)
        # 未使用凭据
        assert result[0][0] == "unused"
        assert result[0][1] == ""
        # 添加父子域
        domain_id2 = CommonDocDomain().addRelationDomain(httphost=father_host, host=child_host, port=443,
                                                         domaintype="child",
                                                         credential_id=credential_id1, credential_key=credential_key1)
        # 添加平级域
        domain_id1 = CommonDocDomain().addRelationDomain(httphost=father_host, host=parallel_host, port=443,
                                                         domaintype="parallel",
                                                         credential_id=credential_id2, credential_key=credential_key2)
        get_sql1 = "select f_status,f_bind_domain from " \
                   "domain_mgnt.t_self_credentials where f_credential_id='%s'" % credential_id1
        get_sql2 = "select f_status,f_bind_domain from " \
                   "domain_mgnt.t_self_credentials where f_credential_id='%s'" % credential_id2
        db = DB_connect(host=child_host)
        result = db.select_all(get_sql1)
        # 验证使用凭据添加关系域
        assert result[0][0] == "used"
        assert result[0][1] == father_host
        db = DB_connect(host=parallel_host)
        result = db.select_all(get_sql2)
        # 验证使用凭据添加关系域
        assert result[0][0] == "used"
        assert result[0][1] == father_host
        CommonDocDomain().delRelationDomain(host=father_host, uuid=domain_id1[0])
        CommonDocDomain().delRelationDomain(host=father_host, uuid=domain_id2[0])
        get_sql1 = "select f_status,f_bind_domain from " \
                   "domain_mgnt.t_self_credentials where f_credential_id='%s'" % credential_id1
        get_sql2 = "select f_status,f_bind_domain from " \
                   "domain_mgnt.t_self_credentials where f_credential_id='%s'" % credential_id2
        db = DB_connect(host=child_host)
        result = db.select_all(get_sql1)
        # 验证删除关系域后,凭据信息
        assert result[0][0] == "invalid"
        assert result[0][1] == ""
        db = DB_connect(host=parallel_host)
        result = db.select_all(get_sql2)
        # 验证删除关系域后,凭据信息
        assert result[0][0] == "invalid"
        assert result[0][1] == ""

    @pytest.fixture(scope="function")
    def bind_paralleldomain(self, metadata_host):
        father_host = metadata_host["self.eisoo.com"]
        parallel_host = metadata_host["replace.eisoo.com"]
        father_host = (father_host.split(":")[1]).strip("/")
        parallel_host = (parallel_host.split(":")[1]).strip("/")
        # 获取平级域凭据
        result1 = CommonAuthCredentialMgnt().get_credential(host=parallel_host)
        credential_id1 = result1[0]
        credential_key1 = result1[1]
        result2 = CommonAuthCredentialMgnt().get_credential(host=parallel_host)
        credential_id2 = result2[0]
        credential_key2 = result2[1]
        # 添加平级域
        domain_id1 = CommonDocDomain().addRelationDomain(httphost=father_host, host=parallel_host, port=443,
                                                         domaintype="parallel",
                                                         credential_id=credential_id1, credential_key=credential_key1)
        yield domain_id1, credential_id1, credential_key1, credential_id2, credential_key2, father_host, parallel_host
        CommonDocDomain().delRelationDomain(host=father_host, uuid=domain_id1[0])
        CommonAuthCredentialMgnt().del_credential(host=parallel_host, credential_id=credential_id1)
        CommonAuthCredentialMgnt().del_credential(host=parallel_host, credential_id=credential_id2)

    def test_CheckCredentialStatus(self, bind_paralleldomain):
        domain_id1 = bind_paralleldomain[0]
        credential_id1 = bind_paralleldomain[1]
        credential_id2 = bind_paralleldomain[3]
        credential_key2 = bind_paralleldomain[4]
        father_host = bind_paralleldomain[5]
        parallel_host = bind_paralleldomain[6]
        # 编辑平级域，更换为新凭据
        client = Http_client()
        put_url = "https://" + "{ip}/api/document-domain-management/v1/domain/{domain_id}".format(ip=father_host,
                                                                                                  domain_id=domain_id1[0])
        client.put(url=put_url,
                   header={"Content-Type": "application/json"},
                   json={"type": "parallel", "port": 443, "credential_id": credential_id2,
                         "credential_key": credential_key2})
        assert client.status_code == 200
        get_sql1 = "select f_status,f_bind_domain from " \
                   "domain_mgnt.t_self_credentials where f_credential_id='%s'" % credential_id1
        get_sql2 = "select f_status,f_bind_domain from " \
                   "domain_mgnt.t_self_credentials where f_credential_id='%s'" % credential_id2
        db = DB_connect(host=parallel_host)
        result = db.select_all(get_sql1)
        # 验证使用凭据添加关系域
        assert result[0][0] == "invalid"
        assert result[0][1] == ""
        result = db.select_all(get_sql2)
        # 验证使用凭据添加关系域
        assert result[0][0] == "used"
        assert result[0][1] == father_host
