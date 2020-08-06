import pytest
import allure
import sys
sys.path.append("../../../../")
from Common.readjson import JsonRead
from Common.http_request import Http_client
from .CommonDocPolicyMgnt import CommonDocPolicyMgnt


@pytest.mark.ASP_344
@pytest.mark.high
@allure.severity('blocker')  # 优先级
@allure.feature("文档域策略管控")
class Test_EditPolicy_PwdStrength200(object):
    @allure.testcase("ID5689,用例名：编辑策略配置--非子域编辑密码强度，编辑成功--返回200")
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
    @pytest.mark.parametrize("headers, jsondata", argvalues=JsonRead(
         "AS\\Http\\DocPolicyMgnt\\testdata\\test_EditPolicyPwdStrength200.json").dict_value_join())
    def test_EditPolicy_PwdStrength200(self, jsondata, headers, teardown):
        '''
               用例描述：该用例用于测试编辑策略接口中“策略名称及配置项个数”的编辑检查，详情可见禅道用例
               编辑策略接口，只关注了策略的编辑成功,策略功能是否正常应用到子域以及子域功能的检验，在应用策略接口中覆盖
        '''
        # 调用策略id到编辑策略的path路径中
        editurl = "/api/document-domain-management/v1/policy-tpl/%s" % (policyid)
        #将json字符串转为字典格式
        dic_jsondata=eval(jsondata)
        #调用编辑策略接口，编辑策略
        edit_client = Http_client()
        edit_client.put(url=editurl, json=dic_jsondata, header=headers)
        assert edit_client.status_code == 200

        # 调用获取文档域策略详细配置，获取编辑后的策略详情
        editpolicy = CommonDocPolicyMgnt().GetPolicyDetail(policyid)
        #根据获取值判断是否编辑成功
        assert editpolicy["content"] == dic_jsondata["content"]
        assert editpolicy["name"] == dic_jsondata["name"]

if __name__ == '__main__':
    pytest.main(['-q', '-v', 'test_EditPolicyPwdStrength200.py'])
