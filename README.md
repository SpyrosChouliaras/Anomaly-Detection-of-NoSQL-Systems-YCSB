# Anomaly-Detection-of-NoSQL-Systems

*Insert Data*

Inserting data into a virtual machine with ssh connection.
Using psutil to collect system data (interval = 5)  and store them to MongoDB (JSON form) installed in the VM.

*GetData*

Connect to MongoDB, obtain the time-series data and detect abnormalities in our Application (MongoDB).
Create graphs and observe anomalies in the CPU as well as the processes that provokes these abnormalities
in a specific period of time. Explore abnormlities also in the average throughput of the database.

*Crontab* has been used from cron which is a Linux utility that schedules a command or script on your server to run automatically at a specified time and date. In this research it has been used to schedule the run of YCSB workloads inside the application.

*YCSB* is a script file that has been used in parallel with cron to run YCSB workloads inside the first Virtual Machine. 

*DataModeling* is a python script that demonstrates ADNS solution. The data visualisation (e.g. ACF, PACF plots), data modeling (ARIMA,SARIMA,LSTM-RNN) and the anomaly detection with DTW algorithm is being demonstrated in this file. It is worth mentioning that Jupyter Notebook has been used as the primary platform for this study.

**YCSB and Stress packages have been used to create real case scenarios.**
