import os
import yaml


class Config(object):
    def __init__(self, config):
        self.config = config

    def __getattr__(self, item):
        # FIXME: This code is not thread safe, collection is mutable
        if not item in self.config:
            raise ValueError('Undefined config property: %s' % item)
        res = self.config[item]
        if isinstance(res, dict):
            res = Config(res)
            self.config[item] = res
        return res


def load_yaml(filepath):
    with open(os.path.abspath(filepath), 'r') as file:
        config = yaml.load(file)
        return Config(config)
