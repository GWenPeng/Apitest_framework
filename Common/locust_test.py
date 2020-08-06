from locust import HttpUser, TaskSet, task


class UserBehavior(TaskSet):
    @task(1)
    def test_getOpaResult(self):
        with self.client.post(url="/api/proton-policy-engine/v1/query/network/accessible",
                              json={"input": {"accessor_id": "266c6a42-6131-4d62-8f39-853e7093701c",
                                              "ip": 167905281}}, catch_response=True) as response:

            if response.status_code == 200 and response.json()["result"] is True:
                response.success()
            elif response.status_code != 200:
                print(response.status_code, response.content)


class WebsiteUser(HttpUser):
    host = "http://10.2.176.245:32180"
    tasks = [UserBehavior]
    min_wait = 3000
    max_wait = 6000
