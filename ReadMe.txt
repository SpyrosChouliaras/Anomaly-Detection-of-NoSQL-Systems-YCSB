- All the coding files have been used to demonstrate Anomaly detection on NoSQL systems.


- "InsertData.py" used to monitor MongoDB application on-the-fly. In detail, Psutil library captures information about resource usage and processes in order to insert the data in MongoDB storage node every 5 seconds. 

- "GetData.py" has been used to collect and visualise data from MongoDB storage node to ADNS system. 

- "Crontab.txt" has been used from cron which is a Linux utility that schedules a command or script on your server to run automatically at a specified time and date. In this research it has been used to schedule the run of YCSB workloads inside the application.

- "YCSB.sh" is a script file that used in parallel with cron to run YCSB workloads inside the first Virtual Machine. 

- "DataModeling.ipynb" is a python script that demonstrates ADNS solution. The data visualisation (e.g. ACF, PACF plots), data modeling (ARIMA,SARIMA,LSTM-RNN) and the anomaly detection with DTW algorithm is being demonstrated in this file. It is worth mentioning that Jupyter Notebook has been used as the primary platform for this study.
