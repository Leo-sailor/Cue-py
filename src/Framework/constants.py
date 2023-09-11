import LocalDependencies.Framework.base_func as base


class constants(dict):
    _self = None

    def __new__(cls, file_loc: str = 'config.ini'):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self, file_loc: str = 'config.ini'):
        file_dump = []
        try:
            with open(file_loc, 'r') as f:
                for line in f:
                    line = '  ' + line
                    if line[-2] != ',' and line[-1] != '}' and line[-2] != '{':
                        line += ','
                    file_dump.append(line)
                whole_file = ' '.join(file_dump)
            whole_file = base.findandreplace(whole_file, '\n', '', True)
        except FileNotFoundError:
            with open(file_loc, "x") as f:
                f.writelines(["{", "'hello':'world'", "}"])
            whole_file = '{}'
        super().__init__(eval(whole_file))

    def __getitem__(self, item, default=None):
        return self.get(item, default)
