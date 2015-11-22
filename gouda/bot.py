import importlib
from peewee import SqliteDatabase

from .settings import Settings


DATABASE = SqliteDatabase("gouda.db")

class Gouda(object):
    def __init__(self):
        self.settings = Settings("config/config.json")
        self.name = self.settings.core['nick']
        self.modules = {}
        self.mains = {}
        self.load_modules()
        self.commands = self.load_commands()
        self.db = DATABASE
        self.db.connect()

    def load_module(self, module):
        try:
            self.modules[module] = importlib.import_module('gouda.modules.%s.main' % module)
            try:
                self.modules[module].run_schema()
                self.mains[module] = getattr(self.modules[module], "main")
            except AttributeError:
                # no main function
                pass
        except ImportError:
            pass

    def load_modules(self):
        """ only run on init, innit """
        module_list = self.settings['modules']
        for module in module_list:
            self.load_module(module)

    def manage_modules(self, loads, unloads, reloads):
        for load in loads:
            if load in self.modules:
                reloads.append(load)
            else:
                self.load_module(load)
        for unload in unloads:
            if unload in self.modules:
                self.modules.pop(unload, None)
        for reload_ in reloads:
            importlib.reload(self.modules[reload_])
            if reload_ in self.mains:
                self.mains[reload_] = self.modules[reload_].main

    def load_commands(self):
        cmds = {}
        for name, module in self.modules.items():
            try:
                commands = getattr(module, "commands")
            except AttributeError:
                # no command list implemented in module
                pass

            for command in commands:
                if command.lower() != 'none':
                    cmds[command] = name

        return cmds

    def get_loads(self, kind, mod):
        loads, unloads, reloads = [], [], []
        if kind == "load":
            loads.append(mod)
        elif kind == "unload":
            unloads.append(mod)
        elif kind == "reload":
            reloads.append(mod)
        return loads, unloads, reloads

    def run(self, conn):
        kwargs = {'writer': conn.message, 'db': self.db, 'log': True}
        while True:
            nick, line = conn.read()
            loads, unloads, reloads = [], [], []
            if line and line[0] != '':
                offset = 0
                if line[0][:-1] == self.name and len(line) > 1:
                    offset = 1
                    # addressed to the bot
                    kwargs['log'] = False
                    if len(line) > 2:
                        loads, unloads, reloads = self.get_loads(line[offset], line[offset+1])
                    if not (loads or unloads or reloads):
                        # nothing *loaded, try commands
                        try:
                            module = self.commands[line[1].lower()]
                            func = getattr(self.modules[module], line[1])
                            msg = line[offset:]
                            func(
                                message=msg,
                                commands=self.commands.keys(),
                                modules=self.modules.keys(),
                                **kwargs
                            )
                        except:
                            # pretty much anything can fuck it up
                            pass
                # run anything else...
                for func in self.mains.values():
                    func(line=line, nick=nick, **kwargs)
            # load/unload/reload
            self.manage_modules(loads, unloads, reloads)
            kwargs['log'] = True
