import psutil

class Host(object):
    def cpus(self):

        items = [ 
                ('cpu_times', {}),
                ('cpu_percent', {'interval':1}),
                ('cpu_times_percent', {'interval':1}),
                ('cpu_stats', {}),
                ('getloadavg', {})]

        res = {}
        for item in items:
            name, args = item
            func = getattr(psutil, name)
            res[name] = func(**args)

        self.cpus = res


obj = Host()
obj.cpus()
print(obj.cpus)
