# coding = utf-8
import time
import pytest
from Common.get_token import Token


@pytest.fixture(scope="class", autouse=True)
def token_cache(request):
    # res = requests.post(url="http://10.2.176.208:30001/oauth2/token", data={"grant_type": "client_credentials"},
    #                     headers={"Content-Type": "application/x-www-form-urlencoded"}, verify=False,
    #                     auth=HTTPBasicAuth("6198e01a-2862-4aa0-84d0-f22d0be9a35c", "1FwfY~YS-ee8"))
    # print(res.json())
    cache_path = f"cache/token"
    # val = Get_token().get_token_byname2(hydra_ip="10.2.176.245", username="1", password="111111")
    # Token(host="10.2.176.245").get_token()
    # print(val)
    # print(time.asctime(time.localtime(time.time())))
    # cache.set(cache_path, {"access_token": val.strip("\n"), "expires_in": 3599, "scope": "", "token_type": "bearer"})
    request.config.cache.set(cache_path,Token(host="10.2.176.245").get_token())

