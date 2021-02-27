from base import Base, func_call

class System(Base):

    def __init__(self):
        super().__init__()
        self.cpus_stats = []
        self.memory_stats = []
        self.disks_stats = []
        self.network_stats = []

    def cpus(self):

        items = [ 
                ('cpu_times', {}),
                ('cpu_percent', {'interval':1}),
                ('cpu_times_percent', {'interval':1}),
                ('cpu_stats', {}),
                ('getloadavg', {})]

        res = func_call(items)
        self.cpus_stats.append(res)
        return res

    def memory(self):

        items = [
                ('virtual_memory', {}),
                ('swap_memory', {})]
        
        res = func_call(items)
        self.memory_stats.append(res)
        return res

    def disks(self):

        items = [
                ('disk_partitions', {}),
                ('disk_usage', '/'),
                ('disk_io_counters', {'perdisk':False})]

        res = func_call(items)
        self.disks_stats.append(res)
        return res

    def network(self):

        items = [
                ('net_io_counters', {}),
                ('net_connections', {'kind':'tcp'}),
                ('net_if_addrs', {}),
                ('net_if_stats', {})]

        res = func_call(items)
        self.network_stats.append(res)
        return res

if __name__ == "__main__":
    obj = System()
    cpus = obj.cpus()
    print(cpus)
    mem = obj.memory()
    print(mem)
    #obj.network()
    #print(obj.network)
