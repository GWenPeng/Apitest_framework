import os
import configparser


class readconfigs:
    def __init__(self, configName='config.ini'):
        # 获取当前路径
        # current_path = os.path.dirname(os.path.abspath(__file__))
        # 获取当前文件夹的父级路径第一种办法
        # father_path = os.path.abspath(current_path+os.path.sep+"..")
        # 获取当前文件夹的父级路径第二种办法
        father_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.dirpath = os.path.join(father_path, configName)
        self.conf = configparser.ConfigParser()
        # 读取config.ini文件参数信息
        self.conf.read(self.dirpath, encoding="utf-8")
        # self.conf.has_section()

    # 获取[database]的配置信息
    def get_db(self, dbname, name):
        value = self.conf.get(section=dbname, option=name).strip("'").strip('"')
        if str(name).lower() == "port":
            value = int(value)
        else:
            return value
        return value

    # 获取[HTTP]的配置信息
    def get_http(self, tagname, name):
        value = self.conf.get(tagname, name).strip("'").strip('"')
        return value

    # 获取[thriftSocket]配置信息
    def get_thriftSocket(self, tagname, name):
        value = self.conf.get(tagname, name).strip("'").strip('"')
        return value

    # 获取[Email]配置信息
    def get_emailconf(self, name):
        value = self.conf.get("Email", name).strip("'").strip('"')
        return value

    # 获取[SSHClient]配置信息
    def get_sshclient(self, ssh_name, name):
        value = self.conf.get(section=ssh_name, option=name).strip("'").strip('"')
        return value

    def get_option(self, section):
        return self.conf.options(section)

    def get_sections(self):
        return self.conf.sections()

    def get_strValue(self, section, option):
        return self.conf.get(section, option)

    def get_items(self, section):
        return dict(self.conf.items(section))

    def set_option_value(self, section, option, value):
        self.conf.set(section, option, value)
        with open(self.dirpath, "w", encoding='UTF-8') as f:
            self.conf.write(f)


if __name__ == '__main__':
    rc = readconfigs()
    rc.conf.sections()
    print(rc.get_strValue(section="env", option="host"))
    print(rc.get_option(section="env"))
    print(rc.get_items("env"))
