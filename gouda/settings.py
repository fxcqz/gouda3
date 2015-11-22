import json


class Settings(dict):

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

    def __init__(self, filename):
        with open(filename, 'r') as handle:
            data = json.loads(handle.read())

        super(Settings, self).__init__(**data)

    @property
    def startup(self):
        return {
            'host': self.network['server'],
            'port': self.network['port'],
            'nick': self.core['nick'],
            'channel': self.core['channel'],
        }
