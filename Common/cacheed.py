# class Spam:
#     def __init__(self, name):
#         self.name = name
#         self.value = {name: "value" + name}
#
#
# # Caching support
# import weakref
#
# _spam_cache = weakref.WeakValueDictionary()
#
#
# def get_spam(name):
#     if name not in _spam_cache:
#         s = Spam(name)
#         _spam_cache[name] = s
#     else:
#         s = _spam_cache[name]
#     return s


import weakref


class SPam:
    _Spam_cache = weakref.WeakValueDictionary()

    def __new__(cls, name):
        if name in cls._Spam_cache:
            return cls._Spam_cache[name]
        else:
            self = super().__new__(cls)
            cls._Spam_cache[name] = self
            return self

    def __init__(self, name):
        print("Initinaizing ,Spam")
        self.name = name


if __name__ == '__main__':
    s = SPam("Dave")
    t = SPam("Dave")
    print(s is t)
