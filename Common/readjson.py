# coding=utf8
import os
import json


def is_json(myjson):  # 判断是否是json格式，是返回True ,否返回false
    try:
        json.load(myjson)
    except ValueError:
        return False
    return True


class JsonRead:
    def __init__(self, datafile):
        self.load_dirt = None
        self.datafile = datafile
        father_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # self.file = os.path.join(father_path, 'Test_data\\' + datafile)
        self.file = os.path.join(father_path, 'Case/' + datafile)
        print(self.file)
        with open(self.file, 'r', encoding='UTF-8') as load_f:
            try:
                self.load_dirt = json.load(load_f)
            except Exception as e:
                print("Please Input Right Json Format !")

    def get_array_jsonkey(self, key, index=0):
        return self.load_dirt[index][key]

    def dict_value_join(self):
        popElement = self.load_dirt.pop("args", "404,not found 'args'")
        List = []
        if len(popElement) > 0 and "404" not in popElement:
            for i in range(len(popElement)):
                L = []
                self.load_dirt.update(popElement[i])
                for Key in self.load_dirt:
                    L.append(self.load_dirt[Key])
                List.append(tuple(L))
        else:
            print("%s, please input  right 'args' !" % popElement)
        return List

    def dict_key_join(self):
        self.load_dirt.pop("args", "404,not found 'args'")
        return ','.join(list(self.load_dirt.keys()))  # 返回一个迭代器dict_keys


if __name__ == '__main__':
    # JR = JsonRead("login.json")
    # value = JR.get_jsonkey(key="url", index=0)
    # print(value)
    JR = JsonRead("AS/Http/Policy/testdata/GetNetworkRestrictionSwitch.json")
    print(JR.dict_value_join())
    print(JR.dict_key_join())
