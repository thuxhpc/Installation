#Flume 1.6.0 安裝

##Preparation
Install Hadoop-2.X.0 version, make sure Hadoop jps is working well  

Agent1  
	Hostname: master  
	Ipaddress : 192.168.86.128  
Agent2  
	Hostname: node01  
	Ipaddress : 192.168.86.129  
	:  
	:  

##Setup
Agent1
```
cd ~
wget http://www.eu.apache.org/dist/flume/1.6.0/apache-flume-1.6.0-bin.tar.gz
wget http://www.eu.apache.org/dist/flume/1.6.0/apache-flume-1.6.0-src.tar.gz
sudo tar zxf apache-flume-1.6.0-bin.tar.gz
sudo tar zxf apache-flume-1.6.0-src.tar.gz
sudo cp -r apache-flume-1.6.0-src/* apache-flume-1.6.0-bin
mv apache-flume-1.6.0-bin flume	 	# 將下載的檔案改名
mv apache-flume-1.6.0-bin.tar.gz flume	# 放置壓縮檔
mv apache-flume-1.6.0-src.tar.gz flume
rm -rf apache-flume-1.6.0-src
scp -r ~/flume node01:~/		# 複製到Agent2
```
##Set Environment Variable
Both agents
```
cd ~
vim .bashrc
	export FLUME_HOME=/home/hduser/flume
	export FLUME_CONF_DIR=$FLUME_HOME/conf
	export PATH=$PATH:$FLUME_HOME/bin
source .bashrc
```

##Configure File

Both agents  
`cd flume`  
Source Directory		# Monitor Directory  
	`mkdir flume_log`  
Channel Directory		# Backup File  
	```
	mkdir flume_tmp
	mkdir flume_tmp1
	```
##Configure File
Agent1  
Hadoop File System		# Creat HDFS directory  
	```
	cd ~/hadoop
	hadoop fs -mkdir /flumelog
	```  
Check on hdfs  

##Configure File

Both agents
```
cd conf/
cp flume-env.sh.template flume-env.sh
vim flume-env.sh		# Configure JAVA_HOME
```
##Setup Agents
Agent1
```
vim flume_conf

agent1.sources=source1
agent1.sinks=sink1
agent1.channels=channel1

agent1.sources.source1.type=avro
agent1.sources.source1.bind=0.0.0.0
agent1.sources.source1.channels=channel1
agent1.sources.source1.port=41414

agent1.sinks.sink1.type=hdfs	 	# 上傳至HDFS
agent1.sinks.sink1.hdfs.path=hdfs://master:9000/flumelog
agent1.sinks.sink1.hdfs.fileType=DataStream
agent1.sinks.sink1.hdfs.writeFormat=TEXT
agent1.sinks.sink1.channel=channel1

agent1.channels.channel1.type=file
agent1.channels.channel1.checkpointDir=/home/hduser/flume/flume_tmp1
agent1.channels.channel1.dataDirs=/home/hduser/flume/flume_tmp
```
##Setup Agents
Agent2
```
vim flume_conf

agent2.sources=source2
agent2.sinks=sink2
agent2.channels=channel2

agent2.sources.source2.type=spooldir	 # 採監控目錄變更方法
agent2.sources.source2.spoolDir=/home/hduser/flume/flume_log
agent2.sources.source2.channels=channel2
agent2.sources.source2.fileHeader = false

agent2.sinks.sink2.type=avro
agent2.sinks.sink2.hostname=master	
agent2.sinks.sink2.port=41414
agent2.sinks.sink2.channel=channel2

agent2.channels.channel2.type=file	# 將event儲存在硬碟中
agent2.channels.channel2.checkpointDir=/home/hduser/flume/flume_tmp1
agent2.channels.channel2.dataDirs=/home/hduser/flume/flume_tmp
```

#Start Agent1
 Agent1---master
```
cd ~/flume
chmod -R 777 flume_tmp & chmod -R 777 flume_tmp1
flume-ng agent -n agent1 -c conf -f /home/hduser/flume/conf/flume_conf -Dflume.root.logger=DEBUG,console
```
連接Agent1, 並持續掃描

##Start Agent2

 Agent2---node01
```
cd ~/flume
chmod -R 777 flume_tmp & chmod -R 777 flume_tmp1
flume-ng agent -n agent2 -c conf -f /home/hduser/flume/conf/flume_conf -Dflume.root.logger=DEBUG,console
```



持續掃描flume_log 目錄

##New an event
Agent2  

Open another shell
`vim /flume/flume_log/test1`
Adding text as below


##Check uploaded file
Back to the Agent2 shell, confirming upload messages

##Check uploaded file
Back to Agent1 shell, confirming upload messages
##Check on HDFS
http://master_IP:50070


`hadoop fs -text /flumelog/FlumeData.1443627094379`

##Related Links
Official File  
https://flume.apache.org/FlumeUserGuide.html


