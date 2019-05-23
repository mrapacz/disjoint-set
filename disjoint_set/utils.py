from collections import defaultdict


class key_dependent_dict(defaultdict):
    def __init__(self, fun_with_param):
        super().__init__(None)
        self.fun = fun_with_param

    def __missing__(self, key):
        ret = self.fun(key)
        self[key] = ret
        return ret
