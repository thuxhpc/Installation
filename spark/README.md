## Spark 安裝

### 版本，以下安裝皆是在hduser這個使用者底下，請先確定所有機器皆有hduser或同Hadoop的user

```
Ubuntu 14.04
Hadoop-2.7.1
Spark-1.4.1
Scala-2.11.4
```

### Scala 安裝，在所有機器

```
wget http://downloads.typesafe.com/scala/2.11.4/scala-2.11.4.tgz
tar zxf scala-2.11.4.tgz
mv scala-2.11.4 scala
sudo mv scala /usr/lib/
```

修改環境變數，`vim .bashrc`，#新增這兩行
```
export SCALA_HOME=/usr/lib/scala
export PATH=$SCALA_HOME/bin:$PATH
```

利用`scala -version`驗證是否安裝成功

### Spark 安裝，在Master執行即可

```
wget  http://ftp.twaren.net/Unix/Web/apache/spark/spark-1.4.1/spark-1.4.1-bin-hadoop2.6.tgz 
tar zxf spark-1.4.1-bin-hadoop2.6.tgz
mv spark-1.4.1-bin-hadoop2.6 spark
cd spark/conf
```

修改`spark-env.sh`內容，麻煩注意所有參數的路徑與自己的配置是否相同

`cp spark-env.sh.template spark-env.sh`

`vim spark-env.sh`

```
export SCALA_HOME=/usr/lib/scala
export JAVA_HOME=/usr/lib/jvm/jdk
export SPARK_MASTER=master
export HADOOP_HOME=/home/hduser/hadoop
export SPARK_HOME=/home/hduser/spark
export SPARK_LIBARY_PATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib:$HADOOP_HOME/lib/native
export YARN_CONF_DIR=$HADOOP_HOME/etc/hadoop
```

修改slaves，`vim slaves`

```
master
node1
node2
```

複製到其他節點上

```
cd ~
scp -r spark node1:/home/hduser
scp -r spark node2:/home/hduser
```

啟動服務

```
cd spark
sbin/start-all.sh
./build/env/bin/hue livy_server
```

測試範例`bin/run-example org.apache.spark.examples.SparkPi 100`

Web UI `http://master_ip:8080`


參考資料

```
http://samchu.logdown.com/posts/250103-spark-teaching-1-hadoop26-installation
http://samchu.logdown.com/posts/250281-spark-teaching-2-spark12-installation
```



