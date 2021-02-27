import process, system
import time

class Host(object):

    def __init__(self):
        self.process = process.Process()
        self.system = system.System()

    def status(self, interval=5, times=5):
        for i in range(times):
            self.process.processes()
            self.system.cpus()
            self.system.memory()
            self.process.save_all()
            self.system.save_all()
            time.sleep(interval)
          
if __name__ == "__main__":
    obj = Host()
    obj.status()
