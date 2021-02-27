from base import Base, func_call
import time

class Process(Base):

    def __init__(self):
        super().__init__()
        self.processes_stats = []

    def processes(self):
        
        process_iter = func_call([('process_iter',
            {'attrs':[
                'pid',
                'username', 
                'cpu_times',
                'memory_info',
                'open_files', # owner only
                'connections',# owner only
                'num_threads'
                ]})])
        process_iter_val = process_iter['process_iter']['value']
        res = {p.pid: p.info | {'time_measured': time.time()} for p in process_iter_val if p.info['username'] ==
                self.username}
        self.processes_stats.append(res)
        return res

    # 'name', 'num_ctx_switches', 'exe', 'cwd', 'memory_full_info',
    # 'memory_info', 'pid', 'create_time', 'nice', 'cpu_times', 'memory_maps',
    # 'uids', 'open_files', 'username', 'terminal', 'memory_percent',
    # 'connections', 'cpu_num', 'environ', 'num_threads', 'cpu_percent',
    # 'io_counters', 'gids', 'num_fds', 'cmdline', 'ppid', 'cpu_affinity',
    # 'threads', 'ionice', 'status']

if __name__ == "__main__":
    obj = Process()
    procs = obj.processes()
    print(procs)
