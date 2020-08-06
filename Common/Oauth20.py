from Common.http_request import Http_client
from Common import ssh_client
from requests.auth import HTTPBasicAuth


class Get_token(object):
    def get_token_byid(self, clientid, secret):
        auth = HTTPBasicAuth(clientid, secret)
        get_client = Http_client()
        get_client.post(url="http://10.2.176.208:30001/oauth2/token",
                        params={"grant_type": "client_credentials"},
                        header={"Content-Type": "application/x-www-form-urlencoded"},
                        auth=auth)
        if get_client.status_code != 200:
            return get_client.jsonResponse
        else:
            token = get_client.jsonResponse["access_token"]
            return token

    def get_token_byname(self, hydra_ip, username, password):
        sh = ssh_client.SSHClient(host=hydra_ip)
        cmd_val = "cd /root/;python oauthclientformanager.py {} {} {}".format(hydra_ip, username, password)
        val = sh.command(cmd_val)
        print((eval(val.decode()))["access_token"])
        token = (eval(val.decode()))["access_token"]
        sh.ssh_close()
        return token

    # 该方法临时用，后期注释
    def get_token_byname2(self, hydra_ip, username, password):
        sh = ssh_client.SSHClient(host=hydra_ip)
        cmd_val = "cd /root/;python oauthclientformanager.py {} {} {}".format(hydra_ip, username, password)
        val = sh.command(cmd_val)
        # print("打印245："+val.decode())
        token = (eval(val.decode()))["access_token"]
        try:
            if token.index('oauthclient') > 0:
                pass
        except ValueError:
            sh.ssh_close()
            return token
        else:
            cmd_val = "cd /root/;python oauthclient.py {} {} {}".format(hydra_ip, username, password)
            val = sh.command(cmd_val)
            # print("打印245："+val.decode())
            token = (eval(val.decode()))["access_token"]
            sh.ssh_close()
            return token

# if __name__ == "__main__":
#     Get_token().get_token_byname(hydra_ip="10.2.176.208", username="1",password="11")

