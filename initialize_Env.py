# encoding=utf-8
import os

# from Common.Log import MyLog as logging
from Common.readConfig import readconfigs

currentpath = os.path.dirname(os.path.abspath(__file__))
dirpath = os.path.join(currentpath, 'config.ini')
ENV_PATH = currentpath + "/allure_report/allure_results/environment.xml"


class Init_Env:
    """初始化环境信息，更新properties文件"""

    def __init__(self):
        # logging.info("获取环境配置信息")
        # 读取配置文件，返回字典格式
        rf = readconfigs()
        self.data = rf.get_items(section="env")
        # print(self.data)

    def dict_to_xml(self):
        parameter = []
        for k in sorted(self.data.keys()):
            xml = []
            v = self.data.get(k)
            if k == 'detail' and not v.startswith('<![CDATA['):
                v = '<![CDATA[{}]]>'.format(v)
            xml.append('<key>{value}</key>'.format(value=k))
            xml.append('<value>{value}</value>'.format(value=v))
            parameter.append('<parameter>{}</parameter>'.format(''.join(xml)))

        return '<environment>{}</environment>'.format(''.join(parameter))

    def init(self):
        data = self.dict_to_xml()
        file = open(ENV_PATH, 'w')
        # with open(ENV_PATH, 'w') as f:
        file.write(data)


if __name__ == '__main__':
    IE = Init_Env()
    IE.init()
