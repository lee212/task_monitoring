import os
import psutil
import getpass

class Host(object):

    def __init__(self):
        sysname, nodename, release, version, machine = os.uname()
        self.hostname = nodename
        self.username = getpass.getuser()

def func_call(items):
    res = {}
    for item in items:
        name, args = item
        func = getattr(psutil, name)
        res[name] = func(**args)

    return res

