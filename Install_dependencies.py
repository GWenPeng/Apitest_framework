# coding=utf8
import os


def install_dependencies(str):
    f = os.popen(r'%s' % str)
    d = f.read()
    print(d)
    f.close()


if __name__ == '__main__':
    # 安装pytest依赖
    install_dependencies("pip3 install pytest")
    # 安装pymysql依赖
    install_dependencies("pip3 install pymysql")
    # 安装thrift依赖
    install_dependencies("pip3 install thrift")
    # 安装requests依赖
    install_dependencies("pip3 install requests")

    # install_dependencies("pip3 install xlrd")

    install_dependencies('pip3 install paramiko')
    install_dependencies('pip3 install allure-pytest')
    install_dependencies('pip3 install pytest-parallel')  # 支持多线程
    install_dependencies('pip3 install pytest-xdist')  # 支持多进程
    # install_dependencies('pip3 install pipreqs') UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd0 in
    # position 586: invalid continuation byte
    # os.system("cd  ThriftAPI")
    # os.system("thrift-0.9.3.exe -gen py ShareMgnt.thrift")
