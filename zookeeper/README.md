###Zookeeper Install


這邊參考的是國網中心所提供的大資料軟體開發平台

安裝版本為
```
hadoop-2.7.1
zookeeper-3.4.5-cdh5.4.5
```

將`zookeeper-3.4.5-cdh5.4.5.tar.gz`放到機器裡面或下載
```
wget http://archive.cloudera.com/cdh5/cdh/5/zookeeper-3.4.5-cdh5.4.5.tar.gz
tar -zxvf zookeeper-3.4.5-cdh5.4.5.tar.gz
mv zookeeper-3.4.5-cdh5.4.5 zookeeper
```
複製config檔
```
cp /home/hduser/zookeeper/conf/zoo_sample.cfg /home/hduser/zookeeper/conf/zoo.cfg
```

修改`zookeeper/conf/zoo.cfg`，`vim zookeeper/conf/zoo.cfg`，修改為你要放myid檔案的路徑
```
dataDir=/home/hduser/zookeeper
```
並增加一行
```
server.1=master:2888:3888
```
新增`myid`檔案
```
cd /home/hduser/zookeeper
vim myid
```
內容填入`1`，如果要再其他台也部署zookeeper，則其他台id依序為`2`，`3`以此類推

啟動zookeeper
```
cd zookeeper
bin/zkServer.sh start
```

使用jps查看，必須有`QuorumPeerMain`這項服務
