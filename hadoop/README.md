# Hadoop 2.7.1 安裝

## 安裝環境
 OS: `Ubnutu 14.04.1LTS`
 
 先利用`ifconfig`查看所有機器的ip
 ```
 master	192.168.56.128
 node01	192.168.56.129
 node02	192.168.56.130
 ```
修改/etc/hostname (以下所有master, node1, node2請依照自己給機器的name設定，假設你的master叫做Hadoop-master，那以下所有master，皆要改成Hadoop-master，node同理)

```
sudo vim /etc/hostname
sudo service hostname start
```

 安裝Java JDK
 ```
 sudo apt-get install -y openjdk-7-jdk
 sudo ln -s /usr/lib/jvm/java-7-openjdk-amd64 /usr/lib/jvm/jdk
 ```

新增Hadoop使用者

```
sudo addgroup hadoop
sudo adduser --ingroup hadoop hduser
sudo adduser hduser sudo
su hduser
cd ~
```

建立SSH免密碼登入(以下皆為Master操作)

```
ssh-keygen -t rsa -f ~/.ssh/id_rsa -P ""
cp ~/.ssh/id_rsa.pub ~/.ssh/authorized_keys
scp –r ~/.ssh node1:~/
scp -r ~/.ssh node2:~/
```
下載Hadoop

```
cd ~
wget http://apache.stu.edu.tw/hadoop/common/hadoop-2.7.1/hadoop-2.7.1.tar.gz
tar zxf hadoop-2.7.1.tar.gz
mv hadoop-2.7.1 hadoop
```
新增環境變數

`vim .bashrc`

```
export JAVA_HOME=/usr/lib/jvm/jdk/
export HADOOP_INSTALL=/home/hduser/hadoop
export PATH=$PATH:$HADOOP_INSTALL/bin
export PATH=$PATH:$HADOOP_INSTALL/sbin
export HADOOP_MAPRED_HOME=$HADOOP_INSTALL
export HADOOP_COMMON_HOME=$HADOOP_INSTALL
export HADOOP_HDFS_HOME=$HADOOP_INSTALL
export YARN_HOME=$HADOOP_INSTALL
```
`source .bashrc`

設定Hadoop config

`cd hadoop/etc/hadoop`

`vim hadoop-env.sh`，修改內容下

`export JAVA_HOME=/usr/lib/jvm/jdk`

修改core-sit.xml，`vim core-site.xml`，新增在`<configuration></configuration>`內

```
<property>
   <name>fs.default.name</name>
   <value>hdfs://master:9000</value>
</property>
```

修改yarn-site.xml，`vim yarn-site.xml`，新增在`<configuration></configuration>`內

```
<property>
   <name>yarn.nodemanager.aux-services</name>
   <value>mapreduce_shuffle</value>
</property>
<property>
   <name>yarn.resourcemanager.hostname</name>
   <value>master</value>
</property>
<property>
   <name>yarn.resourcemanager.address</name>
   <value>master:8032</value>
</property>
<property>
   <name>yarn.resourcemanager.resource-tracker.address</name>
   <value>master:8031</value>
</property>
<property>
   <name>yarn.resourcemanager.scheduler.address</name>
   <value>master:8030</value>
</property>
<property>
   <name>yarn.resourcemanager.scheduler.class</name>
   <value>org.apache.hadoop.yarn.server.resourcemanager.scheduler.capacity.CapacityScheduler</value>
</property>
<property>
   <name>yarn.nodemanager.address</name>
   <value>0.0.0.0:8034</value>
</property>
<property>
   <name>yarn.nodemanager.aux-services.mapreduce.shuffle.class</name>
   <value>org.apache.hadoop.mapred.ShuffleHandler</value>
</property>

```

`cp mapred-site.xml.template mapred-site.xml`
`vim mapred-site.xml`

新增在`<configuration></configuration>`內

```
<property>
   <name>mapreduce.framework.name</name>
   <value>yarn</value>
</property>
```

新增兩個資料夾

```
mkdir -p ~/mydata/hdfs/namenode
mkdir -p ~/mydata/hdfs/datanode
```

修改hdfs-site.xml，`vim hdfs-site.xml`，新增在`<configuration></configuration>`內

```
<property>
   <name>dfs.replication</name>
   <value>2</value>
 </property>
 <property>
   <name>dfs.namenode.name.dir</name>
   <value>/home/hduser/mydata/hdfs/namenode</value>
 </property>
 <property>
   <name>dfs.datanode.data.dir</name>
   <value>/home/hduser/mydata/hdfs/datanode</value>
 </property>
<property>
    <name>dfs.webhdfs.enabled</name>
    <value>true</value>
</property>
<property>
  <name>dfs.permissions</name>
  <value>false</value>
</property>

```

修改`slaves`，`vim slaves`

```
node1
node2
```

將Hadoop資料夾複製給其他node

```
scp -r /home/hduser/hadoop node1:/home/hduser/
scp -r /home/hduser/hadoop node2:/home/hduser/

```

格式化HDFS

```
cd ~/hadoop
bin/hdfs namenode -format
```

啟動Hadoop，`sbin/start-all.sh`

使用`jps`查看java運行程式

執行範例程式
```
cd /home/hduser/hadoop
hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.1.jar pi 2 5
```

```
hadoop fs -ls /
hadoop fs -mkdir -p /hduser/test
```
將檔案放上HDFS
```
hadoop fs -put LICENSE.txt /hduser/test/
```
查看檔案是否放上去
```
hadoop fs -ls /hduser/test
```
執行wordcount
```
hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-2.7.1.jar wordcount /hduser/test/LICENSE.txt /hduser/test/output1/
```
查看結果
```
hadoop fs -ls /hduser/test/output1   (必須看到_SUCCESS)
hadoop fs -cat /hduser/test/output1/part-r-00000
```



