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
        self.name = type(self).__name__
        self.snapshot_idx = 0

    def save_all(self, opath=None):
        opath = "{}{}_{}_{}_{}".format(opath or "",
                type(self).__name__.lower(), self.snapshot_idx, self.hostname, self.username)
        save(opath, self.__dict__)
        self.snapshot_idx += 1


def psutil_func_call(ftuple):
    res_dict = {}
    for fname, fargs in ftuple:
        func = getattr(psutil, fname)
        res_dict[fname] = { 
                'value': func(**fargs),
                'time_measured': time.time()}
    return res_dict

def save(fname, dict_data):
    fname = "{}_{}.json".format(fname, time.time())
    with open(fname, 'w') as f:
        json.dump(dict_data, f, indent=4)
    
def gen_time_seq(unix_time, freq=10):
    return unix_time - divmod(unix_time / freq, 1)[1] * freq

