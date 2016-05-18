# Ceph-deploy Installation

##### 以 deploy 方式安裝共需四個節點，各自功用分別如下表所示

| 節點名稱 |          用途         |      IP       |
|:--------:|:---------------------:|:-------------:|
|  deploy  | ceph-deploy           | 172.24.12.110 |
|   MON1   | monitor               | 172.24.12.111 |
|   OSD1   | object storage daemon | 172.24.12.112 |
|   OSD2   | object storage daemon | 172.24.12.113 |

> 安裝環境：Ubuntu 14.04.3 LTS

*官方推薦的 Ceph 最小節點配置數量為 3+2，也就是 3 個 mon + 2 個 OSD，但以練習為目的的話以 1+2 的架構便已足夠。*

======

#### Preflight

> 安裝過程中主要是透過 admin node 以 deploy 方式安裝其他節點所需套件，故首先須於 admon node 安裝 ceph-deploy 套件，並設定好 admin 與各節點的 SSH 相關設定。


------
##### **✱ all node**

* DNS 設定
```
$ sudo vim /etc/hosts
```
```vim
172.24.12.110   deploy
172.24.12.111   MON1
172.24.12.112   OSD1
172.24.12.113   OSD2
```

* 更新並安裝套件
```
$ sudo apt-get update && sudo apt-get -y upgrade
$ sudo apt-get install -y ntp openssh-server
```

------
##### **✱ MON and OSD nodes**

* 在每個節點上新增一個帳戶(包含deploy)
```
$ sudo addgroup {groupname}
$ sudo adduser --ingroup {groupname} {username}
$ sudo adduser {username} sudo
```
> 將 {username} 更改為自訂的使用者帳戶名稱。

* 為此用戶增加 root 權限
```
$ echo "{username} ALL = (root) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/{username}
$ sudo chmod 0440 /etc/sudoers.d/{username}
```

------
##### **✱ deploy node**
* 建立 ssh-keygen
```
$ ssh-keygen
```
> 過程選項可直接 enter

* 將公鑰複製到其他節點上做認證使用
```
$ ssh-copy-id {username}@{nodeIP}
```

* 修改設定
```
$ vim ~/.ssh/config
```
```vim
  Host MON1
     Hostname MON1
     User {username}
  Host OSD1
     Hostname OSD1
     User {username}
  Host OSD2
     Hostname OSD2
     User {username}
```

------
##### **✱ deploy node**

* 下載 realase key
```
$ wget -q -O- 'https://ceph.com/git/?p=ceph.git;a=blob_plain;f=keys/release.asc' | sudo apt-key add -
```

* 新增 Ceph packages 至 repository
```
$ echo deb http://ceph.com/debian-{ceph-stable-release}/ $(lsb_release -sc) main | sudo tee /etc/apt/sources.list.d/ceph.list
```
> 將 {ceph-stable-release} 更改為需安裝之版本，如 firefly, hammer。
> 可參考 [ceph releases](http://docs.ceph.com/docs/master/releases/)。

* 更新並開始安裝 ceph-deploy
```
$ sudo apt-get update && sudo apt-get install -y ceph-deploy
```
======

#### Storage Cluster Quick Start

* 新增目錄
```
$ mkdir ~/ceph && cd ~/ceph
```

* 建立 Cluster
```
$ ceph-deploy new {mon-nodes}
```
> 將 {mon} 改為主要 monitor 節點，如 MON1

* 修改設定
```
$ sed -i '$a osd pool default size = 2' ceph.conf
```

* 安裝 ceph 套件
```
ceph-deploy install --release {ceph-stable-release} {deploy-node} {mon-nodes} {osd-nodes}
```
> 將 {ceph-stable-release} 更改為需安裝之版本。

* 建立 monitor 並將所有密鑰複製到工作目錄
```
$ ceph-deploy mon create-initial
```

* 於 OSD 新增儲存位置
```
$ ssh {OSD-node1}
$ sudo mkdir /var/local/osd0
$ sudo chown ceph:ceph /var/local/osd0
$ exit

$ ssh {OSD-node2}
$ sudo mkdir /var/local/osd1
$ sudo chown ceph:ceph /var/local/osd1
$ exit
```

* 啟動 OSD
```
$ ceph-deploy osd prepare {OSD-node1}:/var/local/osd0 {OSD-node2}:/var/local/osd1
$ ceph-deploy osd activate {OSD-node1}:/var/local/osd0 {OSD-node2}:/var/local/osd1
```

* 複製配置文件和管理密鑰到所有節點以便使用Ceph CLI
```
$ ceph-deploy admin {all nodes}
```

* 修改權限
```
$ sudo chmod +r /etc/ceph/ceph.client.admin.keyring
```

* 確認狀態
```
$ ceph health
```
> 出現 HEALTH_OK 代表 cluster 運作正常

* 檢視叢集狀態
```
$ ceph status
```

* 檢視 osd 清單
```
$ ceph osd ls
$ ceph osd tree
$ watch -n 1 ceph df
```
> 可以看到每個 OSD 的 ID 以及 weight 等等資訊

------
#### Operating Object Data

* 檢視現有的 pool
```
$ ceph osd pool ls
```

* 上傳檔案
```
$ rados put {fileName} {filePath} --pool={poolName}
```
> 可使用 $ man rados 查看用法

* 檢視檔案
```
$ rados -p {poolName} ls
```

* 檢視檔案位置
```
$ ceph osd map {poolName} {fileName}
```

* 下載檔案
```
$ rados get {fileName} {filePath} --pool={poolName}
```
> {filePath} 須包含檔案名稱，即下載後儲存的檔案。

* 刪除檔案
```
$ rados rm {fileName} --pool={poolName}
```

------
#### Adding/Removing OSDs

##### Adding OSDs

* 建立 osd
```
$ ceph osd create [{uuid}]
```

* 進入 osd 建立儲存位置
```
$ ssh {new-osd-host}
$ sudo mkdir /var/lib/ceph/osd/ceph-{osd-number}
$ exit
```

* 啟動 osd
```
$ sudo start ceph-osd id={osd-num}
```

======


##### Removing OSDs

* 將 osd 移出叢集
```
$ ceph osd out {osd-num}
```
> 讓系統將 osd 的檔案分布至其他 osd。

* 停止 osd 服務
```
$ ssh {osd-host}
$ sudo /etc/init.d/ceph stop osd.{osd-num}
```

* 將 OSD 從 CRUSH map 中移除
```
$ ceph osd crush remove {name}
```

* 移除驗證金鑰
```
$ ceph auth del osd.{osd-num}
```

* 移除 osd
```
$ ceph osd rm {osd-num}
```

------
# Ceph Object Gateway Installation

*Ceph RGW 可單獨為一獨立的節點。*

* 安裝 ceph object gateway
```
$ ceph-deploy install --release {ceph-stable-release} --rgw {CEPH-GATEWAY}
```
> 可以直接裝在 mon 上，或直接新增一個獨立的 gateway node。

* 建立 ceph object gateway instance
```
$ ceph-deploy rgw create {CEPH-GATEWAY}
```
> 前往 http://CEPH-GATEWAY:7480，有畫面則代表安裝成功

=====
##### 驗證安裝

* 建立使用者
```
$ sudo radosgw-admin user create --uid="cephuser" --display-name="First User"
```
> 記住產生的 access_key 與 secret_key。

* 安裝 python-boto
```
$ sudo apt-get install -y python-boto
```

* 建立 api 測試程式
```
$ vim s3test.py
```
```
import boto
import boto.s3.connection
access_key = '{YOUR_ACCESS_KEY}'
secret_key = '{YOUR_SECRET_KEY}'
conn = boto.connect_s3(
aws_access_key_id = access_key,
aws_secret_access_key = secret_key,
host = '{YOUR_GATEWAY_HOST}',
port = 7480,
is_secure=False,
calling_format = boto.s3.connection.OrdinaryCallingFormat(),
)
bucket = conn.create_bucket('my-new-bucket')
for bucket in conn.get_all_buckets():
  print "{name}\t{created}".format(name = bucket.name,created = bucket.creation_date)
```
> 修改 {YOUR_ACCESS_KEY}、{YOUR_SECRET_KEY}、{YOUR_GATEWAY_HOST}。

* 執行測試程式
```
$ python s3test.py
```
> 出現 my-new-bucket 2016-05-15T06:25:24.000Z 代表成功。

=====

*API 參考網站* 
> http://docs.ceph.com/docs/master/radosgw/s3/python/  
> http://boto.cloudhackers.com/en/latest/s3_tut.html  
