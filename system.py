from base import Base, psutil_func_call

class System(Base):

    def __init__(self):
        super().__init__()
        self.cpus_cache = None
        self.memory_cache = None
        self.disks_cache = None
        self.network_cache = None

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
