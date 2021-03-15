import json
import glob, os
import numpy as np
import pandas as pd
from base import gen_time_seq
from collections import OrderedDict

DEBUG=True

class Aggregator(object):
    def __init__(self, ipath="./"):
        entities = self.load_json(ipath)
        self.input_path = ipath

    def load_json(self, path):
        jsons = {}
        for fname in glob.glob(path + "*json"):
            with open(fname) as f:
                if DEBUG: print(f"{fname} loaded.")
                data = json.load(f)
                jsons[os.path.basename(fname)] = data
        self.loaded_jsons = jsons
        return jsons

    def refresh(self, force_to_reload=False):
        jsons = self.loaded_jsons
        jsons_fnames = jsons.keys()
        path = self.input_path
        for fname in glob.glob(path + "*json"):
            if os.path.basename(fname) in jsons_fnames and not force_to_reload:
                continue
            with open(fname) as f:
                if DEBUG: print(f"{fname} loaded.")
                data = json.load(f)
                jsons[os.path.basename(fname)] = data
        #self.loaded_jsons = {**self.loaded_jsons , **jsons} 
        return jsons

    def collect_systems_cpu_by(self, column):
        sys_infos_by_group = {}
        for fname, saved_data in self.loaded_jsons.items():
            if fname[0:6] != "system":
                continue
            sys_info = saved_data['cpus_cache'][column]
            if saved_data['hostname'] in sys_infos_by_group:
               sys_infos_by_group[saved_data['hostname']].append(sys_info)
            else:
               sys_infos_by_group[saved_data['hostname']] = [sys_info]
        return sys_infos_by_group

    # user=0.1, nice=0.0, system=0.1, idle=99.8, iowait=0.0, irq=0.0, softirq=0.0, steal=0.0, guest=0.0, guest_nice=0.0
    def collect_systems_cpy_by_cpu_times_percent(self):
        return self.collect_systems_cpu_by('cpu_times_percent')

    def collect_systems_cpu_by_getloadavg(self):
        return self.collect_systems_cpu_by('getloadavg')

    def cpu_times_percent_to_dataframe(self, sys_infos_by_group):
        dict_data = {}
        for hostname, sys_infos in sys_infos_by_group.items():
            # NEED TO MANAGE hostnames
            tmp = OrderedDict({ "user": {}, "nice": {}, "system": {}, "idle": {}, "iowait": {}, "irq": {}, "softirq": {}, "steal": {}, "guest": {}, "guest_nice": {}})
            for sys_info in sys_infos:
                time_seq = gen_time_seq(sys_info['time_measured'])
                for idx, column in enumerate(tmp.keys()):
                    if time_seq in tmp[column]:
                        tmp[column][time_seq].append(sys_info['value'][idx])
                    else:
                        tmp[column][time_seq] = [sys_info['value'][idx]]
            for column in tmp.keys():
                dict_data[column] = {pd.to_datetime(k, unit='s', origin='unix') : np.mean(v) for k, v in tmp[column].items()}
 
        df = pd.DataFrame.from_dict(dict_data)
        return df

    def getloadavg_to_dataframe(self, sys_infos_by_group):
        dict_data = {}
        for hostname, sys_infos in sys_infos_by_group.items():
            tmp = {}
            for sys_info in sys_infos:
               time_seq = gen_time_seq(sys_info['time_measured'])
               if time_seq in tmp:
                   tmp[time_seq].append(sys_info['value'][0])
               else:
                   tmp[time_seq] = [sys_info['value'][0]]
            dict_data[hostname] = {pd.to_datetime(k, unit='s', origin='unix') : np.mean(v) for k, v in tmp.items()}
        df = pd.DataFrame.from_dict(dict_data)
        return df

    def gpu_device_info(self):
        dlist = []
        column1 = 'device_info'
        column2 = 'gpu'
        for fname, saved_data in self.loaded_jsons.items():
            if fname[0:6] != "system":
                continue
            sys_info = saved_data['gpus_cache'][column1]
            time_seq = gen_time_seq(sys_info['time_measured'])
            hostname = saved_data['hostname']
            for device_idx in range(sys_info['count']):
                dev_info = sys_info[column2][device_idx]
                data = [
                        time_seq,
                        hostname,
                        device_idx,
                        dev_info['product_name'],
                        # frame buffer memory in bytes (from MiB)
                        dev_info['fb_memory_usage']['total'] * (1024**2),
                        dev_info['fb_memory_usage']['free'] * (1024**2),
                        dev_info['utilization']['gpu_util'],
                        dev_info['utilization']['memory_util'],
                        ]
                dlist.append(data)
        return pd.DataFrame(dlist,
        columns=['date', 'hostname', 'device_index', 'product_name',
        'fb_memory_usage_total', 'fb_memory_usage_free', 'gpu_util',
        'memory_util'])

    def merge_process_by_name(self):
        return self.merge_process_by('name')

    def merge_process_by(self, gname):
        proc_infos_by_group = {}
        for fname, saved_data in self.loaded_jsons.items():
            if fname[0:6] != "proces":
                continue
            proc_infos = saved_data['cached']
            for pid, proc_info in proc_infos.items():
                if proc_info[gname] in proc_infos_by_group:
                   proc_infos_by_group[proc_info[gname]].append(proc_info)
                else:
                   proc_infos_by_group[proc_info[gname]] = [proc_info]
        return proc_infos_by_group

    def merge_process_by_task_name(self):
        # a.loaded_jsons['process_h36n13_hrlee_1614571657.029896.json']['cached']['162996']['environ']['RP_TASK_NAME']
        # 'task.0005,my cpu task 5,stage.0000,None,pipeline.0000,None'
        proc_infos_by_group = {}
        for fname, saved_data in self.loaded_jsons.items():
            if fname[0:6] != "proces":
                continue
            proc_infos = saved_data['cached']
            for pid, proc_info in proc_infos.items():
                environ = proc_info['environ']
                if not environ:
                    continue
                if not 'RP_TASK_NAME' in environ:
                    continue
                rp_task_name = environ['RP_TASK_NAME']

                task_id, task_name, stage_id, stage_name, pipe_id, pipe_name = rp_task_name.split(",")
                gname = task_name[0:11]
                if gname in proc_infos_by_group:
                   proc_infos_by_group[gname].append(proc_info)
                else:
                   proc_infos_by_group[gname] = [proc_info]
        return proc_infos_by_group

    def mean_cpu_percent_by_time(self, proc_infos_by_group):
        dict_data = {}
        for gname, proc_infos in proc_infos_by_group.items():
            tmp = {}
            for proc_info in proc_infos:
               time_seq = gen_time_seq(proc_info['time_measured'])
               if time_seq in tmp:
                   tmp[time_seq].append(proc_info['cpu_percent'])
               else:
                   tmp[time_seq] = [proc_info['cpu_percent']]
            dict_data[gname] = {pd.to_datetime(k, unit='s', origin='unix') : np.mean(v) for k, v in tmp.items()}
        df = pd.DataFrame.from_dict(dict_data)
        return df

    def mean_memory_info_rss_by_time(self, proc_infos_by_group):
        dict_data = {}
        for gname, proc_infos in proc_infos_by_group.items():
            tmp = {}
            for proc_info in proc_infos:
               time_seq = gen_time_seq(proc_info['time_measured'])
               if time_seq in tmp:
                   tmp[time_seq].append(proc_info['memory_info'][0]) # rss, vms, shared, text, lib, data, dirty
               else:
                   tmp[time_seq] = [proc_info['memory_info'][0]]
            dict_data[gname] = {pd.to_datetime(k, unit='s', origin='unix') : np.mean(v) for k, v in tmp.items()}
        df = pd.DataFrame.from_dict(dict_data)
        return df

