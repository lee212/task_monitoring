import process, system
import time
import argparse

class Host(object):

    def __init__(self):
        self.process = process.Process()
        self.system = system.System()
        self.get_argparse()

    def status(self, interval=None, times=None):
        interval = interval or self.args.interval
        times = times or self.args.times
        for i in range(times):
            self.process.processes()
            self.system.cpus()
            self.system.memory()
            self.process.save_all(self.args.output_path)
            self.system.save_all(self.args.output_path)
            time.sleep(interval)

    def get_argparse(self):
        parser = argparse.ArgumentParser(description="Host monitoring")
        parser.add_argument("--interval", default=5)
        parser.add_argument("--times", type=int, default=5)
        parser.add_argument("--output_path")
        args = parser.parse_args()
        self.args = args
          
if __name__ == "__main__":
    obj = Host()
    obj.status()
