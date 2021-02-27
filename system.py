from host import Host, func_call

class System(Host):

    def __init__(self):
        super().__init__()

    def cpus(self):

        items = [ 
                ('cpu_times', {}),
                ('cpu_percent', {'interval':1}),
                ('cpu_times_percent', {'interval':1}),
                ('cpu_stats', {}),
                ('getloadavg', {})]

        self.cpus = func_call(items)

    def memory(self):

        items = [
                ('virtual_memory', {}),
                ('swap_memory', {})]
        
        self.memory = func_call(items)

    def disks(self):

        items = [
                ('disk_partitions', {}),
                ('disk_usage', '/'),
                ('disk_io_counters', {'perdisk':False})]

        self.disks = func_call(items)

    def network(self):

        items = [
                ('net_io_counters', {}),
                ('net_connections', {'kind':'tcp'}),
                ('net_if_addrs', {}),
                ('net_if_stats', {})]

        self.network = func_call(items)


if __name__ == "__main__":
    obj = Host()
    obj.cpus()
    print(obj.cpus)
    obj.memory()
    print(obj.memory)
    obj.network()
    print(obj.network)
