# coding=utf-8
import pytest
import allure
from ShareMgnt import ncTShareMgnt
from Common.thrift_client import Thrift_client
from ShareMgnt import ttypes
from DB_connect.mysqlconnect import DB_connect
from Common.readjson import JsonRead


# :arg scope: the scope for which this fixture is shared, one of  ``"function"`` (
# default), ``"class"``, ``"module"``, ``"package"`` or ``"session"``.
# ``"package"`` is considered **experimental** at this time.

@pytest.fixture(scope='function',
                autouse=False)
@allure.step("初始化Thrift连接对象and数据库DB_connect连接对象and初始化数据")
def fixtureFunc():
    # 创建一个结构体ncTSmtpSrvConf类对象
    tc = Thrift_client(ncTShareMgnt)  # 创建Thrift_cilent对象
    db = DB_connect()  # 创建数据库连接对象
    return tc, db


@pytest.mark.high
@allure.severity('critical')  # 优先级 包含blocker, critical, normal, minor, trivial 几个不同的等级
@allure.feature("SMTP模块")  # 功能块 feature功能分块时比story大,即同时存在feature和story时,feature为父节点
@allure.story("设置SMTP配置模块")  # 功能块 具有相同feature或story的用例将规整到相同模块下,执行时可用于筛选
# @allure.issue("BUG号 ：222  OR jira号： 222")  # 问题表识，关联标识已有的问题，可为一个url链接地址
@allure.testcase(url='https://eisoo.com', name="用例名：设置SMTP 邮箱配置")
@pytest.mark.parametrize("server, safeMode, port, email, password, openRelay, checkpoint",
                         argvalues=JsonRead("AS/Thrift/SMTP_suite/testdata/smtp_setconfig.json").dict_value_join())
# @pytest.mark.usefixtures("fixtureFunc")
def test_SMTP_SetConfig(fixtureFunc, server, safeMode, port, email, password, openRelay, checkpoint, worker_id="gw1"):
    tc = fixtureFunc[0]
    db = fixtureFunc[1]
    conf = ttypes.ncTSmtpSrvConf(server=server, safeMode=safeMode, port=port, email=email, password=password,
                                 openRelay=openRelay)
    # conf = ttypes.ncTSmtpSrvConf(server=server, safeMode=safeMode, port=port, email=email, password=password,
    #                              open_relay=open_relay)
    # 创建一个结构体ncTSmtpSrvConf类对象
    # tc = Thrift_client(ncTShareMgnt)  # 创建Thrift_cilent对象
    response = tc.client.SMTP_SetConfig(conf)  # 调用SMTP_SetConfig方法
    # db = DB_connect()  # 创建数据库连接对象
    Query_Results = db.select_one("SELECT f_value from sharemgnt_db.t_sharemgnt_config where f_key='smtp_config' ")
    print(type(Query_Results))
    assert response is None  # 断言response返回为None
    assert checkpoint["server"] in Query_Results[0]  # 断言Email插入到数据库表t_sharemgnt_config.f_key=smtp_config中
    db.delete(" DELETE  from sharemgnt_db.t_sharemgnt_config where f_key='smtp_config' ;")  # 清除插入的smtp_config数据
    tc.close()


if __name__ == '__main__':
    pytest.main(['-q', '-s', 'test_SMTP_SetConfig.py'])
