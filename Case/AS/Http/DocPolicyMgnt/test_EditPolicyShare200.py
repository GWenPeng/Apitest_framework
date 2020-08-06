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
class Test_EditPolicyShare200(object):
    @allure.testcase("ID5691,用例名：编辑策略配置--非子域编辑内外链共享，编辑成功--返回200 ")
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
         "AS\\Http\\DocPolicyMgnt\\testdata\\test_EditPolicyShare200.json").dict_value_join())
    def test_EditPolicyShare200(self, jsondata, headers,teardown):
        # 策略id到编辑策略的path路径中
        editurl = "/api/document-domain-management/v1/policy-tpl/%s" % (policyid)
        #将编辑数据的json字符串转为字典格式
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
    pytest.main(['-q', '-v', 'test_EditPolicyShare200.py'])
