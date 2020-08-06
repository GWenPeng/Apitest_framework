# coding=UTF-8
import pytest
import os
from initialize_Env import Init_Env
import shutil

if __name__ == '__main__':
    # pytest.main(["-q", "Testcase/thriftcase/test_Usrm_GetUserInfo.py"]) #指定测试文件

    # pytest.main(["Testcase"])  # 指定测试目录
    # # os.system('pytest -k "SMTP or Usrm"')  # 通过模糊查询文件名的方式执行  -k的方式执行一系列测试用例了,同时表达式中科包含 and、or、not
    # os.system('pytest -m "high or normal " --alluredir="Report/data ')  # -m选项也可以用表达式指定多个标记名，例如-m “mark1 and
    # # mark2” 或者-m “mark1 and not mark2” 或者-m “mark1 or mark2”
    # # os.system('pytest --alluredir="Report/data"')  # 生成测试数据
    # os.system('allure generate Report/data -o  Report/result --clean')  # 生成测试报告
    # shutil.rmtree("Report/data")  # 清空测试数据Report/data
    #
    # # os.system('pytest --collect-only')  # 在批量执行测试用例之前，我们往s往会想知道哪些用例将被执行是否符合我们的预期等等，这种场景下可以使用–collect-only选项
    # os.system("pytest --tests-per-worker 6") #多线程运行
    # os.system("pytest -s  -n=2")  # 多进程运行
    os.system('pytest -v -s -m ASP_317 ')  # 生成测试数据
    os.system("copy  allure_report\\environment.properties  allure_report\\allure_results\\environment.properties")
    os.system("copy  allure_report\\categories.json  allure_report\\allure_results\\categories.json")
    # env = Init_Env()
    # env.init()
    os.system('allure generate allure_report/allure_results -o  allure_report/report  --clean')

    # shutil.rmtree("allure_report/allure_results")  # 清空测试数据report/allure-result
