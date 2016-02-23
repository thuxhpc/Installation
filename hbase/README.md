###Hbase Install


這裡版本參考國網中心的大資料開發平台

版本為
```
hadoop-2.7.1
zookeeper-3.4.5-cdh5.4.5
hbase-1.0.0-cdh5.4.5
```

這裡我們不使用HBase內建zookeeper，如沒安裝zookeeper請先安裝

先將檔案放進機器或下載
```
cd ~
wget http://archive.cloudera.com/cdh5/cdh/5/hbase-1.0.0-cdh5.4.5.tar.gz
tar -zxvf hbase-1.0.0-cdh5.4.5.tar.gz
mv hbase-1.0.0-cdh5.4.5 hbase
```

調整參數，關閉內建Zookeeper
```
vim hbase/conf/hbase-env.sh
```
加入以下兩條
```
export JAVA_HOME=/usr/lib/jvm/jdk
export HBASE_MANAGES_ZK=flase
```
這裡將`HBASE_MANAGES_ZK`設定為`false`，就是zookeeper部由HBase附帶起動


修改`hbase-site.xml`
```
vim hbase/conf/hbase-site.xml
```
將以下插入`<configuration>``</configuration>`之間
```
<property>
  <name>hbase.rootdir</name>
  <value>hdfs://master:9000/hbase</value>
</property>
<property>
  <name>hbase.master</name>
  <value>hdfs://master:60000</value>
</property>
<property>
  <name>hbase.cluster.distributed</name>
  <value>true</value>
</property>
<property>
  <name>hbase.zookeeper.property.clientPort</name>
  <value>2181</value>
</property>
<property>
  <name>hbase.zookeeper.quorum</name>
  <value>master</value>
</property>
<property>
  <name>hbase.zookeeper.property.dataDir</name>
  <value>/opt/hadoop/zookeeper</value>
</property>
<property>
  <name>hbase.client.scanner.caching</name>
  <value>200</value>
</property>
<property>
  <name>hbase.balancer.period</name>
  <value>300000</value>
</property>
<property>
  <name>hbase.client.write.buffer</name>
  <value>10485760</value>
</property>
<property>
  <name>hbase.hregion.majorcompaction</name>
  <value>7200000</value>
</property>
<property>
  <name>hbase.hregion.max.filesize</name>
  <value>67108864</value>
</property>
<property>
  <name>hbase.hregion.memstore.flush.size</name>
  <value>1048576</value>
</property>
<property>
  <name>hbase.server.thread.wakefrequency</name>
  <value>30000</value>
</property>
```
如果zookeeper有多台的話，`hbase.zookeeper.quorum`這項要修改如下
```
<property>
  <name>hbase.zookeeper.quorum</name>
  <value>master,node,slave</value>
</property>
```
在HDFS上建立HBase資料夾
```
hadoop fs -mkdir /hbase
```
新增slaves主機
```
vim hbase/conf/regionservers
```
內容如下:
```
master
node1
node2
```
設定環境變數
```
cd ~
vim .bashrc
```
內容如下:
```
export HBASE_HOME=/home/hduser/hbase
export PATH=$PATH:$HBASE_HOME/bin
```
載入環境變數
```
source .bashrc
```
將檔案複製到其他node上
```
scp -r hbase node1:/home/hduser
scp -r hbase node2:/home/hduser
```
啟動HBase
```
cd hbase
bin/start-hbase.sh
hbase thrift start &

```
使用`jps`查看，master必須有以下兩個服務
```
HRegionServer
HMaster
```
其他node則要有
```
HRegionServer
```
