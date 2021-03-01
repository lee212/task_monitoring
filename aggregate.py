import json
import glob, os
import numpy as np
import pandas as pd
from base import gen_time_seq

DEBUG=True

class Aggregator(object):
    def __init__(self, ipath="./"):
        entities = self.load(ipath)

    def load(self, path):
        jsons = {}
        for fname in glob.glob(path + "*json"):
            with open(fname) as f:
                if DEBUG: print(f"{fname} loaded.")
                data = json.load(f)
                jsons[os.path.basename(fname)] = data
        self.loaded_jsons = jsons
        return jsons

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






