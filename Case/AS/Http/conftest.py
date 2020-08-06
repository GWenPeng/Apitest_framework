# coding = utf-8
import time
import pytest
from DB_connect.mysqlconnect import DB_connect
from Common.ssh_client import SSHClient
from Common.Oauth20 import Get_token
from Common.http_request import Http_client
from requests.auth import HTTPBasicAuth
import requests


@pytest.fixture(scope="session", autouse=True)
def change_mirror(request):
    mirror = request.config.getoption(name="--mirror")
    if mirror == "false" or mirror == "False":
        pass
    else:
        setlist = request.config.getoption(name="--env")
        mirrorlist = mirror.split(";")
        envlist = setlist.split(";")
        for mirr in mirrorlist:
            for hostip in envlist:
                ssh = SSHClient(host=hostip)
                ssh.command("cd /root/")
                # 格式化镜像脚本
                mirrorversion = "./%s.sh" % mirr
                print(mirrorversion)
                ssh.command(mirrorversion)
                time.sleep(30)


def pytest_addoption(parser):
    parser.addoption("--mirror", action="store", default="False")
    parser.addoption("--env", action="store", default="10.2.176.176;10.2.176.208;10.2.176.245;10.2.180.162")


@pytest.fixture(scope='session', autouse=False)
def DomainCheck():
    '''
    sharemgnt_db/HTTP/SSHClient=10.2.176.176;
    db_domain_self/HTTPGWP/SSHClient_self=10.2.176.245
    db_domain_Child/HTTP_child2/SSHClient_parallel=10.2.180.162
    db_domain_parallel/HTTP_child1/SSHClient_Child=10.2.176.208
    后续线上环境更改，此处要更新
    '''
    for domain, http, ssh in [("sharemgnt_db", "HTTP", "SSHClient"),
                              ("db_domain_self", "HTTP_child1", "SSHClient_Child"),
                              ("db_domain_Child", "HTTP_child2", "SSHClient_parallel"),
                              ("db_domain_parallel", "HTTPGWP", "SSHClient_self")]:
        db_self = DB_connect(dbname=domain)
        # 更新domain.t_domain_self和policy_mgnt.t_policies
        db_self.update("UPDATE domain_mgnt.t_domain_self,policy_mgnt.t_policies SET "
                       "domain_mgnt.t_domain_self.f_type = 'parallel',"
                       "domain_mgnt.t_domain_self.f_parent_host = null,"
                       "policy_mgnt.t_policies.f_locked = 0")
        # 删除相关表中脏数据
        db_self.delete("DELETE FROM anyshare.t_acs_doc")
        db_self.delete("DELETE FROM domain_mgnt.t_library_sync_plan")
        db_self.delete("DELETE FROM domain_mgnt.t_policy_tpl_domains")
        db_self.delete("DELETE FROM domain_mgnt.t_policy_tpls")
        db_self.delete("DELETE FROM domain_mgnt.t_relationship_domain")
        db_self.delete("DELETE FROM sharemgnt_db.t_person_group")

        db_self.delete(
            "DELETE FROM sharemgnt_db.t_user WHERE f_login_name not in ('system','admin','security','audit')")
        db_self.close()

    # @pytest.fixture(scope="module", autouse=True)
    # def token_cache(request):
    #     # res = requests.post(url="http://10.2.176.208:30001/oauth2/token", data={"grant_type": "client_credentials"},
    #     #                     headers={"Content-Type": "application/x-www-form-urlencoded"}, verify=False,
    #     #                     auth=HTTPBasicAuth("6198e01a-2862-4aa0-84d0-f22d0be9a35c", "1FwfY~YS-ee8"))
    #     # print(res.json())
    #     cache_path = f"cache/token"
    #     val = Get_token().get_token_byname2(hydra_ip="10.2.176.176", username="1", password="111111")
    #     print(val)
    #     # print(time.asctime(time.localtime(time.time())))
    #     # cache.set(cache_path, {"access_token": val.strip("\n"), "expires_in": 3599, "scope": "", "token_type": "bearer"})
    #     request.config.cache.set(cache_path,
    #                              {"access_token": val.strip("\n"), "expires_in": 3599, "scope": "", "token_type": "bearer"})
    #
    #
    # if __name__ == '__main__':
    #     token_cache()


@pytest.fixture(scope='session', autouse=True)
def metadata_host(metadata):
    if "JOB_NAME" in metadata:
        if metadata["JOB_NAME"] == "Tester_ApiTest_7.0":
            return eval(metadata["branch_host"])
        elif metadata["JOB_NAME"] == "Tester_ApiTest_7.0":
            return eval(metadata["master_host"])
    else:
        return eval(metadata["local_host"])
