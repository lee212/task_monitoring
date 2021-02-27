import os
import psutil
import getpass
import time
import json

class Base(object):

    def __init__(self):
        sysname, nodename, release, version, machine = os.uname()
        self.hostname = nodename
        self.username = getpass.getuser()

    def save_all(self, opath=None):
        opath = "{}{}_{}_{}".format(opath or "",
                type(self).__name__.lower(), self.hostname, self.username)
        save(opath, self.__dict__)


def func_call(items):
    res = {}
    for item in items:
        name, args = item
        func = getattr(psutil, name)
        res[name] = { 
                'value': func(**args),
                'time_measured': time.time()}

    return res

def save(fname, data):
    fname = "{}_{}.json".format(fname, time.time())
    with open(fname, 'w') as f:
        json.dump(data, f, indent=4)
    
