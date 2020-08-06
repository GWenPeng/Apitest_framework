from IPy import IP
import math


def IpToInt(ip):
    """

    :param ip: ip地址
    :return: IP地址整数
    """
    iplist = ip.split(".")
    # print(iplist)
    Sum = 0
    for index in range(4):
        Sum += int(iplist[index]) * int(math.pow(256, 4 - index - 1))

    return Sum


def ipAndNetmaskToStartipEndip(ip, netmask):
    """

    :param ip: ip地址
    :param netmask: 子网掩码
    :return: 起始IP和终止ip
    """
    StartEndip = IP(ip).make_net(netmask).strNormal(3)
    startip = str(IP(StartEndip)[1])
    endip = str(IP(StartEndip)[-2])
    return startip, endip


if __name__ == '__main__':
    print(IpToInt(ip="10.2.154.254"))
    print(ipAndNetmaskToStartipEndip(ip="10.2.154.231", netmask="255.255.255.0"))
