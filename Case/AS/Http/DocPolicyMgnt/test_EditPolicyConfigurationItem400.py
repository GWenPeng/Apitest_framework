import pytest
import allure
import sys
sys.path.append("../../../../")
from Common.readjson import JsonRead
from Common.http_request import Http_client
from .CommonDocPolicyMgnt import CommonDocPolicyMgnt

@pytest.mark.ASP_344
@pytest.mark.medium
@allure.severity('normal')  # 优先级
@allure.feature("文档域策略管控")
class Test_EditPolicy_ConfigurationItemCheck400(object):
    @allure.testcase("ID5333,用例名：编辑策略配置--非子域配置项非法检查--返回400")
    @pytest.fixture(scope='function')
    def teardown(self):
        # 新增策略
        global policyid
        policyid = CommonDocPolicyMgnt().AddPolicy('{"content":[{"name":"password_strength_meter",'
                                                   '"value":{"enable":False,"length":12}}],'
                                                   '"name":"policy1"}')
        yield
        # 删除策略配置
        CommonDocPolicyMgnt().DeletePolicy(policyid)

    @pytest.mark.parametrize("headers, jsondata, checkpoint", argvalues=JsonRead(
         "AS\\Http\\DocPolicyMgnt\\testdata\\test_EditPolicyConfigurationItem400.json").dict_value_join())
    def test_EditPolicyConfigurationItem400(self, jsondata, headers, checkpoint,teardown):
        # 策略id到编辑策略的path路径中
        editurl = "/api/document-domain-management/v1/policy-tpl/%s" % (policyid)
        #将编辑数据的json字符串转为字典格式
        dic_jsondata=eval(jsondata)
        #调用编辑策略接口，编辑策略
        edit_client = Http_client()
        edit_client.put(url=editurl, json=dic_jsondata, header=headers)
        assert edit_client.status_code == checkpoint['status_code']
        assert edit_client.jsonResponse["code"] == checkpoint["code"]
        assert edit_client.jsonResponse["message"] == checkpoint["message"]

if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_EditPolicyConfigurationItem400.py'])
