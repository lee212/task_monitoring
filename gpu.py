from base import Base, save
import time
from pynvml import *
from pynvml.smi import nvidia_smi

class GPU(Base):

    device_info = None
    proc_infos = {}
    proc_stats = {}

    def __init__(self):
        super().__init__()
        nvmlInit()
        self.deviceCount = nvmlDeviceGetCount()
        self.nvsmi = nvidia_smi.getInstance()

    def get_handles(self):
        handles = [None] * self.deviceCount
        for i in range(self.deviceCount):
            handle = nvmlDeviceGetHandleByIndex(i)
            handles[i] = handle
        self.handles = handles
        return handles

    def device_query(self):
        device_info = self.nvsmi.DeviceQuery('memory.free, memory.total, timestamp, count, name, index, compute_mode, utilization.gpu, utilization.memory')
        self.device_info = device_info
        return device_info

    def get_running_processes(self):
        proc_infos = {}
        for idx, handle in enumerate(self.handles):
            procs = nvmlDeviceGetComputeRunningProcesses(handle)
            for proc in procs:
                proc_infos[proc.pid] = { 
                        'pname': str(nvmlSystemGetProcessName(proc.pid)),
                        'usedMemory':  proc.usedGpuMemory,
                        'deviceIndex': idx,
                        'time_measured': time.time()
                        }
        self.proc_infos = proc_infos
        return proc_infos

    def get_accounting_stats(self):
        proc_stats = {}
        for idx, handle in enumerate(self.handles):
            for pid in nvmlDeviceGetAccountingPids(handle):
                stats = nvmlDeviceGetAccountingStats(handle, pid)
                proc_stats[pid] = { 
                        'gpuUtilization': stats.gpuUtilization,
                        'memoryUtilization': stats.memoryUtilization,
                        'time': stats.time,
                        'status': stats.isRunning,
                        'deviceIndex': idx
                        }
        self.proc_stats = proc_stats
        return proc_stats

    def save_serializable(self, opath=None):
        opath = "{}{}_{}_{}".format(opath or "", type(self).__name__.lower(), self.hostname, self.username)
        save(opath, { 
            'proc_infos': self.proc_infos,
            'proc_stats': self.proc_stats,
            'device_info': self.device_info})

