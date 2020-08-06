# -*- coding=utf-8 -*-
from Common.http_request import Http_client
from Common.get_token import Token
from Common.http_request import Http_client
from functools import lru_cache


@lru_cache()
def get_token(host="10.2.176.245"):
    access_token = Token(host=host).get_token()["access_token"]
    return access_token


class CommonAuthCredentialMgnt(object):
    # 新建认证凭据
    def create_credential(self, host=None, credential_type="parallel", note="string"):
        create_client = Http_client()
        token = get_token(host=host)
        post_url = "https://" + "{host}/api/document-domain-management/v1/credential".format(host=host)
        create_client.post(url=post_url,
                           jsondata={"credential_type": credential_type, "note": note},
                           header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        if create_client.status_code != 201:
            print(create_client.jsonResponse)
        else:
            return create_client.status_code, create_client.respheaders['Location'].split("/")[-1]

    # 查看指定认证凭据
    def get_specific_credential(self, host="10.2.181.58", credential_id=None):
        get_client = Http_client()
        token = get_token(host=host)
        get_url = "https://" + "{host}/api/document-domain-management/v1/credential/{id}".format(host=host, id=credential_id)
        get_client.get(url=get_url, header={"Content-Type": "application/json", "Authorization": "Bearer " + token})
        if get_client.status_code != 200:
            print(get_client.jsonResponse)
            return get_client.status_code, get_client.jsonResponse
        else:
            return get_client.status_code, get_client.jsonResponse

    # 获取认证凭据
    def get_credential(self, host="10.2.181.58", credential_type="parallel", note="string"):
        # 调用新建认证凭据接口
        create_client = Http_client()
        token = get_token(host=host)
        print(token)
        header = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        data = {"credential_type": credential_type, "note": note}
        create_url = "https://" + "{host}/api/document-domain-management/v1/credential".format(host=host)
        create_client.post(url=create_url,
                           jsondata=data,
                           header=header)
        if create_client.status_code != 201:
            print(create_client.jsonResponse)
        else:
            pass
        credential_id = create_client.respheaders['Location'].split("/")[-1]
        get_client = Http_client()
        get_url = "https://" + "{host}/api/document-domain-management/v1/credential/{id}".format(host=host,
                                                                                                 id=credential_id)
        get_client.get(url=get_url,
                       header=header)
        if get_client.status_code != 200:
            print(get_client.jsonResponse)
        else:
            credential_key = get_client.jsonResponse["credential_key"]
            print(credential_id, credential_key)
            print(get_client.jsonResponse)
            return credential_id, credential_key

    # 删除认证凭据
    def del_credential(self, host, credential_id):
        del_client = Http_client()
        token = get_token(host=host)
        print(token)
        header = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        del_url = "https://" + host + "/api/document-domain-management/v1/credential/{id}".format(id=credential_id)
        del_client.delete(url=del_url,
                          header=header)
        print(del_client.status_code)


if __name__ == "__main__":
    credential_id, credential_key = CommonAuthCredentialMgnt().get_credential(host="10.2.176.208",credential_type="child")
    print(credential_id, credential_key)
    CommonAuthCredentialMgnt().del_credential(credential_id=credential_id,host="10.2.176.208")
