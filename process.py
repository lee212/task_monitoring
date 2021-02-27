from host import Host, func_call

class Process(Host):

    def __init__(self):
        super().__init__()

    def processes(self):
        
        process_iter = func_call([('process_iter',
            {'attrs':['pid','username']})])['process_iter']
        procs = {p.pid: p.info for p in process_iter if p.info['username'] ==
                self.username}
        print(procs)

    # 'name', 'num_ctx_switches', 'exe', 'cwd', 'memory_full_info',
    # 'memory_info', 'pid', 'create_time', 'nice', 'cpu_times', 'memory_maps',
    # 'uids', 'open_files', 'username', 'terminal', 'memory_percent',
    # 'connections', 'cpu_num', 'environ', 'num_threads', 'cpu_percent',
    # 'io_counters', 'gids', 'num_fds', 'cmdline', 'ppid', 'cpu_affinity',
    # 'threads', 'ionice', 'status']

if __name__ == "__main__":
    obj = Process()
    obj.processes()
