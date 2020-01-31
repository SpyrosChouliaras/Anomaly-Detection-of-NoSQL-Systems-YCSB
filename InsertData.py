import psutil
import pprint
import sys
import os
from pymongo import MongoClient
import time

#Connect with MongoDB in the storage node
conn = MongoClient('xxx',27017)
db = conn.Atlas
collection = db.atlas_data

counter =0
p = psutil.Process()
datalist = list()
data= dict()

while True:

#'name' : name of the process
#'pid' :  process ID
#'memory_percent' : Compare process memory to total physical system memory and calculate process memory utilization as a percentage
#'num_threads' : The number of trheads currently used by this process
#'num_fds' : The number of file descriptors currently opened by this process 
#'num_ctx_swtiches' : The number voluntary and involuntary context switches performed by this process 
#'terminal' : The terminal associated with this process, if any, else None
#'uids' : The real, effective and saved user ids of this process as a named tuple.
#'gids' : The real, effective and saved group ids of this process as a named tuple
#'cwd' : The process current working directory as an absolute path
#'status' : The current process status as a string
    cpu_percent = {'cpu_percent': psutil.cpu_percent(interval=0)}
    for proc in psutil.process_iter():
        try:
            z = (proc.as_dict(attrs=['name','ppid','memory_percent','memory_info',
                                    'cpu_times','num_fds','nice',
                                    'num_threads','num_ctx_switches','terminal',
                                    'uids','gids','cwd','status']))
            z['cpu_percent']=proc.cpu_percent(interval=0)
            datalist.append(z)
        except (psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
            pass
        ##Speed up Scenario for Linux  +2.6x
        # z = (proc.as_dict(attrs=['cpu_num','cpu_percent','cpu_times',
        #                       'create_time','name','ppid','status','terminal',
        #                       'gids','num_ctx_switches','num_threads','uids',
        #                       'username','memory_full_info','memory_maps']))
        datalist = sorted(datalist,key=lambda procObj : procObj['cpu_percent'],reverse=True)

    #Process ID
    # process = psutil.Process(os.getpid())
    # pname = process.name()
    # pid = process.pid

    # CPU_TIMES

    cpu_user = psutil.cpu_times().user
    system = psutil.cpu_times().system
    idle = psutil.cpu_times().idle
    nice = psutil.cpu_times().nice
    cpu_count = psutil.cpu_count()
    # iowait = psutil.cpu_times().iowait---
    # irq = psutil.cpu_times().irq    ----
    # softirq = psutil.cpu_times().softirq-  L   I   N   U   X
    # steal = psutil.cpu_times().steal-----
    # guest = psutil.cpu_times().guest-----
    # guest_nice = psutil.cpu_times().guest_nice

    # VIRTUAL_MEMORY
    virtual_memory_total = psutil.virtual_memory().total  # otal physical memory available
    # the actual amount of available memory that can be given instantly to processes that request more memory in bytes; this is calculated by summing different memory values depending on the platform (e.g. free + buffers + cached on Linux) and it is supposed to be used to monitor actual memory usage in a cross platform fashion.
    virtual_memory_available = psutil.virtual_memory().available
    # the percentage usage calculated as (total - available) / total * 100.
    virtual_memory_percent = psutil.virtual_memory().percent
    # memory used, calculated differently depending on the platform and designed for informational purposes only.
    virtual_memory_used = psutil.virtual_memory().used
    virtual_memory_free = psutil.virtual_memory().free
    # memory currently in use or very recently used, and so it is in RAM
    virtual_memory_active = psutil.virtual_memory().active
    virtual_memory_inactive = psutil.virtual_memory().inactive  # memory that is marked as not used.

    # Swap Memory

    swap_memory_total = psutil.swap_memory().total
    swap_memory_used = psutil.swap_memory().used
    swap_memory_free = psutil.swap_memory().free
    swap_memory_percent = psutil.swap_memory().percent
    swap_memory_sin = psutil.swap_memory().sin
    swap_memory_sout = psutil.swap_memory().sout

    # CPU_PERCENT

    # Disk Usage //Return disk usage statistics about the given
    # path as a namedtuple including total, used and free space
    # expressed in bytes, plus the percentage usage//

    disk_total = psutil.disk_usage('/').total
    disk_used = psutil.disk_usage('/').used
    disk_free = psutil.disk_usage('/').free
    disk_percent = psutil.disk_usage('/').percent

    # Disk IoCounters //Return system-wide disk I/O statistics as a
    # namedtuple including the following fields://

    disk_read_count = psutil.disk_io_counters(perdisk=False).read_count
    disk_write_count = psutil.disk_io_counters(perdisk=False).write_count
    disk_read_bytes = psutil.disk_io_counters(perdisk=False).read_bytes
    disk_write_bytes = psutil.disk_io_counters(perdisk=False).write_bytes
    disk_read_time = psutil.disk_io_counters(perdisk=False).read_time
    disk_write_time = psutil.disk_io_counters(perdisk=False).write_time

    # string = str(datetime.datetime.now())

    # d = datetime.datetime.strptime(string, "%Y-%m-%d  %H:%M:%S.%f")
    # times = (str(d.year) + str(d.month) + str(d.day) + str(d.hour) +
    #          str(d.minute) + str(d.second))

    cpu_times = {'cpu_user': cpu_user, 'system': system,
                 'idle': idle, 'nice': nice, 'cpu_count': cpu_count}

    virtual_memory = {'virtual_memory_total': virtual_memory_total,
                      'virtual_memory_available': virtual_memory_available,
                      'virtual_memory_percent': virtual_memory_percent,
                      'virtual_memory_used': virtual_memory_used,
                      'virtual_memory_free': virtual_memory_free,
                      'virtual_memory_active': virtual_memory_active,
                      'virtual_memory_inactive': virtual_memory_inactive}

    swap_memory = {'swap_memory_total': swap_memory_total,
                   'swap_memory_used': swap_memory_used,
                   'swap_memory_free': swap_memory_free,
                   'swap_memory_percent': swap_memory_percent,
                   'swap_memory_sin': swap_memory_sin,
                   'swap_memory_sout': swap_memory_sout}

    disk_iocounters = {'disk_read_count': disk_read_count, 'disk_write_count': disk_write_count,
                       'disk_read_bytes': disk_read_bytes, 'disk_write_bytes': disk_write_bytes,
                       'disk_read_time': disk_read_time, 'disk_write_time': disk_write_time}

    disk_usage = {'disk_total': disk_total, 'disk_used': disk_used,
                  'disk_free': disk_free, 'disk_percent': disk_percent}

    # cpu_percent = {'cpu_percent': psutil.cpu_percent(interval=1)}

    elements = {'cpu_times': cpu_times, 'virtual_memory': virtual_memory, 'cpu_percent': cpu_percent,
                'disk_usage': disk_usage, 'swap_memory': swap_memory, 'disk_iocounters': disk_iocounters}


    data['Resourse_Usage'] = elements
    data['Records_pid_usage'] = datalist


    collection.insert_one(data)
    counter += 1
    elements = {}
    data = {}
    datalist=[]
    time.sleep(5)
