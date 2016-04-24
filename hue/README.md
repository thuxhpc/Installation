###Hue Install

##安裝前先安裝以下軟體，可參考`installation`其他安裝文件
```
Hadoop-2.7.1
Zookeeper-3.4.5-cdh5.4.5
HBase-1.0.0-cdh5.4.5
Hive-1.2.1
```



安裝相關軟體

```
sudo apt-get install git
sudo apt-get install python2.7-dev make libkrb5-dev libxml2-dev libxslt-dev libsqlite3-dev libssl-dev libldap2-dev python-pip ant gcc g++ libkrb5-dev libmysqlclient-dev libssl-dev libsasl2-dev libsasl2-modules-gssapi-mit libsqlite3-dev libtidy-0.99-0 libxml2-dev libxslt-dev make libldap2-dev maven python-dev python-setuptools libgmp3-dev 
```


利用`git`安裝
```
git clone https://github.com/cloudera/hue.git
cd hue
make apps
build/env/bin/hue runserver
```

`cd ~`

修改Hadoop配置，`vim hadoop/etc/hadoop/hdfs-site.xml`，增加以下
```
<property>
  <name>dfs.webhdfs.enabled</name>
  <value>true</value>
</property>
```

修改Hadoop配置，`vim hadoop/etc/hadoop/core-site.xml`，增加以下
```
<property>
  <name>hadoop.proxyuser.hduser.hosts</name>
  <value>*</value>
</property>
<property>
  <name>hadoop.proxyuser.hduser.groups</name>
  <value>*</value>
</property>
```

修改Hive配置，`vim hive/conf/hive-site.xml`，搜尋並修改
```
<property>
    <name>hive.server2.authentication</name>
    <value>NOSASL</value>
  </property>
```


接下來進行Hue文件配置
```
vim desktop/conf/pseudo-distributed.ini
```

須修改的內容如下:(用搜尋修改)
```
配置項目                  值                                說明
http_host                 master_ip                         如果hue放在整個叢集的主機上，這個值不用更改
http_port                 8000                              port
server_user               hduser                            執行Hue Web Server的使用者
server_group              hadoop                            執行Hue Web Server的群組
default_hdfs_superuser    hduser                            HDFS管理用戶
default_user              hduser                            Hue的管理者
fs_defaultfs              hdfs://master:8020                要跟hadoop的core-sit.xml配置一樣
hadoop_conf_dir           /home/hduser/hadoop/etc/hadoop/   hadoop家目錄
resourcemanager_host      master                            對應到hadoop的yarn-site.xml
resourcemanager_api_url   http://master:8088                對應到hadoop的yarn-site.xml

hive_server_host          master                            hive所在主機ip
hive_server_port          10000                             port
hive_conf_dir             /home/hduser/hive/conf            Hive家目錄
```

新增Hue使用者
```
sudo adduser hadoop hue
sudo adduser hue sudo
```

啟動所有服務，如果啟動過就不用再次啟動

Hadoop，`sbin/start-all.sh`
Zookeeper，`bin/zkServer.sh start`
HBase，`bin/start-hbase.sh`，`hbase thrift start &`
Hive
```
hive --service metastore &
bin/hiveserver2 &
```

啟動Hue`build/env/bin/hue runserver 0.0.0.0:8000`

接下來開起網頁`http://master_ip:8000`，查看還有什麼問題，再去修改hue設定檔
