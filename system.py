from base import Base, psutil_func_call
from gpu import GPU

class System(Base):
        
    __gpu = GPU()

    def __init__(self):
        super().__init__()
        self.cpus_cache = None
        self.memory_cache = None
        self.disks_cache = None
        self.network_cache = None
        self.gpus_cache = None

    def gpus(self):
        self.__gpu.get_handles()
        self.__gpu.device_query()
        self.__gpu.get_running_processes()
        self.__gpu.get_accounting_stats()
        self.gpus_cache = {
                'proc_infos': self.__gpu.proc_infos,
                'proc_stats': self.__gpu.proc_stats,
                'device_info': self.__gpu.device_info}
        return self.gpus_cache

    def cpus(self):

        # divide "default" vs "custom" (from yaml file)
        items = [ 
                ('cpu_times', {}),
                ('cpu_percent', {'interval':1, 'percpu':True}),
                ('cpu_times_percent', {'interval':1}),
                ('cpu_stats', {}),
                ('getloadavg', {})]

        self.cpus_cache = psutil_func_call(items)
        return self.cpus_cache

    def memory(self):

        items = [
                ('virtual_memory', {}),
                ('swap_memory', {})]
        
        self.memory_cache = psutil_func_call(items)
        return self.memory_cache

    def disks(self):

        items = [
                ('disk_partitions', {}),
                ('disk_usage', '/'),
                ('disk_io_counters', {'perdisk':False})]

        self.disks_cache = psutil_func_call(items)
        return self.disks_cache

    def network(self):

        items = [
                ('net_io_counters', {}),
                ('net_connections', {'kind':'tcp'}),
                ('net_if_addrs', {}),
                ('net_if_stats', {})]

        self.network_cache = psutil_func_call(items)
        return self.network_cache

if __name__ == "__main__":
    obj = System()
    cpus = obj.cpus()
    print(cpus)
    mem = obj.memory()
    print(mem)
    #obj.network()
    #print(obj.network)
