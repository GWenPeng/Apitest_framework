class domain(object):
    __host = {
        "self.eisoo.com": "10.2.176.245",
        "child.eisoo.com": "10.2.176.208",
        "parallel.eisoo.com": "10.2.180.162",
        "replace.eisoo.com": "10.2.176.176"
    }

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        self.__host.append(value)


if __name__ == '__main__':
    t = domain()
    t.host()
    print(t.host)
