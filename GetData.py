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
import seaborn as sns


#Connection to MongoDB in the storage node
client = MongoClient('xxx',27017)


db = client.Atlas


collection = db.atlas_data

#Function to Query Data from MongoDB between time intervals
## S for Starting point // F for Finishing point
def getdata(Syear,Smonth,Sday,Shour,Sminute,Ssecond,Fyear,Fmonth,Fday,Fhour,Fminute,Fsecond):


		gen_time1 = datetime.datetime(Syear,Smonth,Sday,Shour-1,Sminute,Ssecond)
		gen_time2 = datetime.datetime(Fyear,Fmonth,Fday,Fhour-1,Fminute,Fsecond)

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
		disk = []

		#Retrieve different records on the time interval
		for i in result:

			dataCPU.append(i['Resourse_Usage']['cpu_percent']['cpu_percent'])
			dataMemory.append(i['Resourse_Usage']['virtual_memory']['virtual_memory_percent'])
			diskUsage.append(i['Resourse_Usage']['disk_usage']['disk_percent'])
			top.append([i['Records_pid_usage'][0]['cpu_percent']/i['Resourse_Usage']['cpu_times']['cpu_count'],i['Records_pid_usage'][1]['cpu_percent']/2])
			labels.append(i['Records_pid_usage'][0]['name'])
			dates.append(i['_id'].generation_time)
			data.append(i['Records_pid_usage'])
			# disk.append(i['Resourse_Usage']['disk_iocounters']['disk_read_count']/i['Resourse_Usage']['disk_iocounters']['disk_read_time'])

		return dataCPU,dataMemory,diskUsage,labels,dates,top,data



#Call the function to retrieve data in various days

# cpu,memory,disk,labels,dates,top,data = getdata(2019,8,17,19,11,0,2019,8,17,19,39,0)
# cpu,memory,disk,labels,dates,top,data = getdata(2019,8,19,20,43,0,2019,8,19,21,50,0) # -//- 50/50 ( workloada)
# cpu,memory,disk,labels,dates,top,data,disk = getdata(2019,8,20,18,9,50,2019,8,20,18,20,0) #read/update 95/5 (workloadb) (run 13)
# cpu,memory,disk,labels,dates,top,data = getdata(2019,8,20,18,29,50,2019,8,20,18,40,0) #read/update  1/0 (workloadc)
# cpu,memory,disk,labels,dates,top,data = getdata(2019,8,22,22,44,50,2019,8,22,23,13,0) #read/update  1/0 (workloadb)
cpu,memory,disk,labels,dates,top,data= getdata(2019,8,23,11,29,50,2019,8,23,12,59,0) #95/5 (workloadb) Stress in the last 3 wavelets


#Set the SNS styel and figure size
sns.set(rc={'figure.figsize':(15, 7)},style = 'whitegrid')
#Set the labels in x axis to filtered by hour or month
month = mdates.MonthLocator()  # every month
minute = mdates.MinuteLocator(interval = 10)
h_fmt = mdates.DateFormatter('%H:%M')
fig,ax = plt.subplots()

#Set y label and fontsize
ax.set_ylabel("CPU Usage %",fontsize=15)

#Set the coordinates
ax.yaxis.set_label_coords(-0.05,0.5)
#Plot the CPU usage and the dates
ax.plot(dates, cpu,label="CPU")
ax.xaxis.set_major_locator(minute)
ax.xaxis.set_major_formatter(h_fmt)

#Set the ticks in y axis
ax.yaxis.set_ticks(np.arange(0, 101, 10))
ax.yaxis.grid(True,linewidth = 0.5)
counter = 0

print(len(cpu),len(labels))
for i in range(len(cpu)):
	print(cpu[i],labels[i])

	#SET THE CPU THRESHOLD (if the process is below 85 it will not appear in the graph)
	if cpu[i] > 85 :

		counter = i
		if labels[i] == "java":	
			plt.plot(dates[i],cpu[i],"r*",markersize=7,label = "Java")
			# plt.annotate(labels[i],xy = (dates[i],cpu[i] + 2.5))
			# counter = i
			# print(i)
		if labels[i] == "mongod":	
				plt.plot(dates[i],cpu[i],"go",markersize=5, label = "Mongod")
		if labels[i] == "stress":	
				plt.plot(dates[i],cpu[i],"bd",markersize=5, label = "Stress")

#Create a legend box for visualisation
from matplotlib.font_manager import FontProperties
fontP = FontProperties()
fontP.set_size('small')
handles, labels = plt.gca().get_legend_handles_labels()
by_label = OrderedDict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(),loc='upper center', bbox_to_anchor=(0.5, 1.1),
          fancybox=False, shadow=False, ncol=4,fontsize=15)
# ax.legend(loc ='upper right')

plt.show()


#Create file to store CPU and DATES in order to create later Pandas Dataframe for the analysis
with open("/Users/spyroschouliaras/Desktop/file.txt", "w") as f:
    for s in cpu:
        f.write(str(s) +"\n")

with open("/Users/spyroschouliaras/Desktop/file2.txt", "w") as f:
    for s in dates:
        f.write(str(s) +"\n")


