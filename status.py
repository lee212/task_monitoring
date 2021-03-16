import glob
import os, sys
import curses
import time
import datetime
import argparse
import aggregate
from collections import OrderedDict

def report_progress(header, data_dict, footer):

    idx = 0
    stdscr.addstr(idx, 0, header)
    idx += 1
    stdscr.addstr(idx, 0, "-")
    idx += 1

    footer = "{} ({})".format(datetime.datetime.now(), footer)

    for k, v in data_dict.items():
        if k.strip() == "":
            continue
        #stdscr.addstr(idx, 0, "{}: {}".format(k, v))
        # x: 1node
        # X: 10 node
        value = v['value']
        elapsed = v['elapsed_time']
        if value > 0:
            cnt = value // 168
            progress = ("x" * cnt + " " * (10 - cnt))  or ("x" + " " * 9) 
        
            stdscr.addstr(idx, 0, "{0}:\t\t[{1:10}]\t{2} (cores),\t elapsed: {3} sec\t".format(k,
                progress, value, elapsed))
        else:
            stdscr.addstr(idx, 0, "{0}:\t\t[(stopped)]\t\t({1})\t".format(k, elapsed))
        idx += 1
    if idx == 2:
        stdscr.addstr(idx, 0, "waiting...")

    stdscr.addstr(11, 0, "" )
    stdscr.addstr(12, 0, "-")
    stdscr.addstr(13, 0, footer)
    stdscr.refresh()

def update_task_list(old, new):
    for k, v in new.items():
        old[k] = v
    #print(old.keys(), new.keys())
    reset_list = set(old.keys()) - set(new.keys())
    #print(reset_list)
    for k in reset_list:
        old[k] = 0
        #print(k, old[k])

if __name__ == "__main__":

    parser = argparse.ArgumentParser('task monitoring - progress')
    parser.add_argument('--input_path', '-i')
    args = parser.parse_args()
    if args.input_path is None:
        parser.print_help()
        sys.exit()

    agg = aggregate.Aggregator()

    refresh_interval = 5
    data = OrderedDict()

    try:
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()

        while 1:
            #last_10sec = str(int(time.time()) - 12990)[:9]
            last_100sec = str(int(time.time()) - 10)[:8]
            #jsons = agg.load_json(path = args.input_path, 
            #        load_type = f"process_*_{last_10sec}*.json" )
            #TEMP
            list_of_files = glob.glob(args.input_path + "/*json")
            if len(list_of_files) == 0:
                time.sleep(refresh_interval)
                continue
            latest_file = max(list_of_files, key=os.path.getctime)
            # process_0_g19n02_hrlee_1615876149.21877.json
            #print(latest_file)
            latest_idx = os.path.basename(latest_file).split("_")[1]
            jsons = agg.load_json(path = args.input_path, 
                    load_type = f"process_{latest_idx}_*_{last_100sec}*.json" )
            #print(glob.glob(args.input_path + f"process_*_{last_10sec}*.json" ))
            proc_infos = agg.merge_process_by_task_name()
            # Temp for presentation
            first = list(proc_infos.keys())
            if len(first) > 0:
                node_count = len(set(proc_infos[first[0]][0]['environ']['LSB_HOSTS'].split())) - 1
            else:
                node_count = 0
            header = "Running cores per Task ({} nodes)".format(node_count)
            footer = "refresh interval {} sec".format(refresh_interval)
            newdata = agg.sum_core_count_by_task(proc_infos)
            update_task_list(data, newdata)
            #print(data)
            report_progress(header, data, footer)
            time.sleep(refresh_interval)
    finally:
        curses.echo()
        curses.nocbreak()
        curses.endwin()
