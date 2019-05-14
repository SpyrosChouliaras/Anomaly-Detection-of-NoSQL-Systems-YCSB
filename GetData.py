import datetime
import numpy as np
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import timedelta
import matplotlib.pyplot as plt
from collections import OrderedDict
import matplotlib.dates as mdates
import re


client = MongoClient('vm3',27017)


db = client.Atlas

collection = db.atlas_data
## S for Starting point // F for Finishing point
def getdata(Syear,Smonth,Sday,Shour,Sminute,Ssecond,Fyear,Fmonth,Fday,Fhour,Fminute,Fsecond):


		gen_time1 = datetime.datetime(Syear,Smonth,Sday,Shour,Sminute,Ssecond)
		gen_time2 = datetime.datetime(Fyear,Fmonth,Fday,Fhour,Fminute,Fsecond)

		dummy_id1 = ObjectId.from_datetime(gen_time1)
		dummy_id2 = ObjectId.from_datetime(gen_time2)


		result = collection.find({"_id": {"$lte": dummy_id2 , "$gte": dummy_id1}})

		dataCPU = []
		dataMemory =[]
		diskUsage = []
		top = []
		dates = []
		labels = []
		data = []
		for i in result:
			dataCPU.append(i['Resourse_Usage']['cpu_percent']['cpu_percent'])
			dataMemory.append(i['Resourse_Usage']['virtual_memory']['virtual_memory_percent'])
			diskUsage.append(i['Resourse_Usage']['disk_usage']['disk_percent'])
			top.append([i['Records_pid_usage'][0]['cpu_percent']/i['Resourse_Usage']['cpu_times']['cpu_count'],i['Records_pid_usage'][1]['cpu_percent']/2])
			labels.append(i['Records_pid_usage'][0]['name'])
			dates.append(i['_id'].generation_time)
			data.append(i['Records_pid_usage'])

		return dataCPU,dataMemory,diskUsage,labels,dates,top,data


# cpu,memory,disk,labels,dates,top,data = getdata(2019,3,29,10,13,0,2019,3,29,10,38,0)
cpu,memory,disk,labels,dates,top,data = getdata(2019,3,30,11,41,15,2019,3,30,11,56,35)


# throughput = []
# with open("/Users/spyroschouliaras/Desktop/test.txt","r") as n:
#     for line in n:
#         if line.startswith("2019") and "CLEANUP" not in line:
#             throughput.append(float(re.split(',|=',line)[7]))



#CPU by PROCESS : Return a float representing the process CPU utilization as a
#percentage which can also be > 100.0 in case of a process running multiple threads on different CPUs.

#MAXLIST gives us all the cpu_percent by process in all records - the maximum price is 193.2 which is the last process as we expected
#max is the maximum number of all the (last process id ) which is 193.2
#maxtest2 = 100.0 is the maximum number in the general cpu system
#Conclusion : we have found that the last process id is indeed the largest one but it is not 200% as the CPU is 100%
# the CPU percent seems to be 100% as the maximum process is 193.2% (mauby because is calculated in Dual Core system) ?

month = mdates.MonthLocator()  # every month
minute = mdates.MinuteLocator(interval = 1)
h_fmt = mdates.DateFormatter('%H:%M')
fig,ax = plt.subplots()

ax.set_ylabel("Central Processing Unit Usage %",fontsize=14)
ax.set_xlabel("Day & Time",fontsize=14)
# ax.set_title("Yahoo Cloud Serving Benchmark",fontsize=14)
ax.yaxis.set_label_coords(-0.05,0.5)
# ax.plot(dates,[i[0] for i in top],label="per process") ## Plot the process
ax.plot(dates, cpu,label="CPU")
ax.xaxis.set_major_locator(minute)
ax.xaxis.set_major_formatter(h_fmt)
# ax.plot(dates,memory,label='Memory')
# ax.plot(dates,disk,label='Disk')
ax.yaxis.set_ticks(np.arange(0, 101, 10))
ax.yaxis.grid(True,linewidth = 0.5)
counter = 0
for i in range(len(cpu)):
	if cpu[i] > 94 and i - counter > 3: # (and i - counter > 2)setting the threshold if is more than 95 annotate and distance at least 3 between ids
		if i == 128 or i == 140:
			counter = i
			continue
		else:
			plt.annotate(labels[i],xy = (dates[i],cpu[i] + 2.5))
			counter = i
			print(i)
ax.legend(loc ='upper left')
plt.show()


#
# ax.set_ylabel("AVG",fontsize=14)
# ax.yaxis.set_label_coords(-0.07,0.5)
# ax.set_xlabel("Day & Time",fontsize=14)
# # ax.plot(dates,[i[0] for i in top],label="per process") ## Plot the process
# # ax.plot(dates, cpu,label="CPU")
# ax.plot(dates,throughput,label = "Throughput")
# ax.xaxis.set_major_locator(minute)
# ax.xaxis.set_major_formatter(h_fmt)
# # ax.plot(dates,memory,label='Memory')
# # ax.plot(dates,disk,label='Disk')
# # ax.yaxis.set_ticks(np.arange(0, 101, 10))
# ax.yaxis.set_ticks(np.arange(0, 1000, 100))
# ax.yaxis.grid(True,linewidth = 0.5)
# plt.show()
