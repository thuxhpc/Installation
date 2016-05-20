## Requirements

### Software Requirements

Flink runs on all *UNIX-like environments*, e.g. **Linux**, **Mac OS X**, and **Cygwin** (for Windows) and expects the cluster to consist of **one master node** and **one or more worker nodes**. Before you start to setup the system, make sure you have the following software installed **on each node**:

- **Java 1.7.x** or higher,
- **ssh** (sshd must be running to use the Flink scripts that manage
  remote components)

If your cluster does not fulfill these software requirements you will need to install/upgrade it.


### `JAVA_HOME` Configuration

Flink requires the `JAVA_HOME` environment variable to be set on the master and all worker nodes and point to the directory of your Java installation.

You can set this variable in `conf/flink-conf.yaml` via the `env.java.home` key.


## Flink Setup

Go to the [downloads page](https://flink.apache.org/downloads.html) and get the ready to run package. Make sure to pick the Flink package **matching your Hadoop version**. If you don't plan to use Hadoop, pick any version.

After downloading the latest release, copy the archive to your master node and extract it:

~~~bash
tar xzf flink-*.tgz
cd flink-*
~~~

### Configuring Flink

After having extracted the system files, you need to configure Flink for the cluster by editing *conf/flink-conf.yaml*.

Set the `jobmanager.rpc.address` key to point to your master node.

Finally you must provide a list of all nodes in your cluster which shall be used as worker nodes. Therefore, similar to the HDFS configuration, edit the file *conf/slaves* and enter the IP/host name of each worker node. Each worker node will later run a TaskManager.

Each entry must be separated by a new line, as in the following example:

~~~
192.168.0.100
192.168.0.101
.
.
.
192.168.0.150
~~~

The Flink directory must be available on every worker under the same path. You can use a shared NSF directory, or copy the entire Flink directory to every worker node.

Please see the [configuration page](config.html) for details and additional configuration options.

In particular,

 * the amount of available memory per TaskManager (`taskmanager.heap.mb`),
 * the number of available CPUs per machine (`taskmanager.numberOfTaskSlots`),
 * the total number of CPUs in the cluster (`parallelism.default`) and
 * the temporary directories (`taskmanager.tmp.dirs`)

are very important configuration values.


### Starting Flink

The following script starts a JobManager on the local node and connects via SSH to all worker nodes listed in the *slaves* file to start the TaskManager on each node. Now your Flink system is up and running. The JobManager running on the local node will now accept jobs at the configured RPC port.

Assuming that you are on the master node and inside the Flink directory:

~~~bash
bin/start-cluster.sh
~~~

To stop Flink, there is also a `stop-cluster.sh` script.


### Adding JobManager/TaskManager Instances to a Cluster

You can add both JobManager and TaskManager instances to your running cluster with the `bin/taskmanager.sh` and `bin/jobmanager.sh` scripts.

#### Adding a JobManager

~~~bash
bin/jobmanager.sh (start cluster)|stop|stop-all
~~~

#### Adding a TaskManager

~~~bash
bin/taskmanager.sh start|stop|stop-all
~~~

Make sure to call these scripts on the hosts, on which you want to start/stop the respective instance.

