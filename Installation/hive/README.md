###Hive Install

### 版本，以下安裝皆是在hduser這個使用者底下，請先確定所有機器皆有hduser或同Hadoop的user

```
Ubuntu 14.04
Hadoop-2.7.1
hive-1.2.1
```

##將Hive安裝於Master(切記注意使用者須切換至同Hadoop使用者)

`sudo wget http://apache.stu.edu.tw/hive/hive-1.2.1/apache-hive-1.2.1-bin.tar.gz`

解壓縮 : `tar -zxvf apache-hive-1.2.1-bin.tar.gz`

更名 : 　`mv apache-hive-1.2.1-bin/ hive`

在`.bashrc`增加Hive環境變數

````
vim .bashrc
  export HIVE_HOME=/home/hduser/hive
  export PATH=$HIVE_HOME/bin:$HIVE_HOME/conf:$PATH
  ```

讀取.bashrc，`source .bashrc`

建立Hive所需的HDFS目錄與更改權限，`/tmp` 可能已經存在，若已經存在不須建立，但也須更改權限

```
主要用在存放一些Hive執行過程的臨時資料
hadoop fs -mkdir /tmp 
Hive進行管理的資料目錄
hadoop fs -mkdir /user/warehouse
hadoop fs -chmod 777 /tmp
hadoop fs -chnow 777 /user/hive/warehouse
```

安裝`libmysql-java`，用`JDBC`時需用到。

`sudo apt-get install libmysql-java`

安裝完成後，將`/usr/share/java/mysql-connector-java-5.1.28.jar`複製到`hive/lib`底下

`sudo cp /usr/share/java/mysql-connector-java-5.1.28.jar ~/hive/lib`

接著啟動MySQL，建立一個專屬Hive的帳號，啟動方式如下:

`mysql -u root -p`

接著會要你輸入root密碼，輸入完後會進到`mysql>`的command模式，複製指令時不要複製到`mysql>`以及註解
```
建立一個hive的database

mysql > create database hive; 

建立一個MySQL使用者，帳號跟密碼都是hive，且用%代表在任何hostname都可登入

mysql> grant all on *.* to'hive'@'%' identified by 'hive';    

更新User清單

mysql> flush privileges; 

結束mysql

mysql> exit; #結束mysql

```

修改MySQL的參數設定檔案`my.cnf`：

`sudo vim /etc/mysql/my.cnf`

將`bind-address = 127.0.0.1`這行用#註解，不要讓MySQL綁定local，`#bind-address = 127.0.0.1`

在Hive的目錄裡建立一個新目錄：

`mkdir -p /home/hduser/hive/iotmp`    #Hive config會需要用到

`chmod 777 /home/hduser/hive/iotmp`

進入到Hive的目錄，將hive/conf下的`hive-default.xml.template`改成`hive-site.xml`： 

`cp hive-default.xml.template hive-site.xml`

更改`hive-site.xml`的設定：，用/搜尋修改

```
<configuration>
    <property>
        <name>javax.jdo.option.ConnectionURL</name>  <!-- 連結MySQL的port -->
        <value>jdbc:mysql://master:3306/hive?createDatabaseIfNotExist=true</value>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionDriverName</name> <!– 使用MySQL作為metastore
        <value>com.mysql.jdbc.Driver</value>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionUserName</name> <!-- MySQL的帳號 -->
        <value>hive</value>
    </property>
    <property>
        <name>javax.jdo.option.ConnectionPassword</name> <!-- MySQL的密碼-->
        <value>hive</value>
    </property>
    <property>
        <name>hive.metastore.uris</name>  <!-- 遠端的remote metastore，可以使client連線 -->
        <value>thrift://master:9083</value> 
    </property>
    <!-- 以下4種參數原先是system:java.io.tmpdir，若不更改啟動Hive會發生錯誤，所以改成上述的iotmp目錄 -->
    <property>
        <name>hive.exec.local.scratchdir</name>
        <value>/home/hduser/hive/iotmp</value>
        <description>Local scratch space for Hive jobs</description>
    </property>
    <property>
        <name>hive.downloaded.resources.dir</name>
        <value>/home/hduser/hive/iotmp</value>
        <description>Temporary local directory for added resources in the remote file system.</description>
    </property>
    <property>
        <name>hive.querylog.location</name>
        <value>/home/hduser/hive/iotmp</value>
        <description>Location of Hive run time structured log file</description>
    </property>
    <property>
        <name>hive.server2.logging.operation.log.location</name>
        <value>/home/hduser/hive/iotmp</value>
        <description>Top level directory where operation logs are stored if logging functionality is enabled</description>
    </property>
</configuration>
```

更改conf的`hive-env.sh.template`

`cp hive-env.sh.template hive-env.sh`

```
sudo vim hive-env.sh
 export HADOOP_HEAPSIZE=1024
 export HADOOP_HOME=/home/hduser/hadoop
 export HIVE_CONF_DIR=/home/hduser/hive/conf
 export HIVE_AUX_JARS_PATH=/home/hduser/hive/lib
```

執行

```
hive --service metastore &
bin/hiveserver2 &
```

輸入hive進入hive-shell

```
hive
show tables;
```

參考資料
`http://glj8989332.blogspot.tw/2015/10/hadoop-hive-121.html`




