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
> 將 {ceph-stable-release} 更改為需安裝之版本，如 firefly, hammer。[參考](http://docs.ceph.com/docs/master/releases/)

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
ceph-deploy install {deploy-node} {mon-nodes} {osd-nodes}
```

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
```
> 可以看到每個 OSD 的 ID 以及 weight 等等資訊

------
##### **✱ Storing/Retrieving Object Data**

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

* 刪除檔案
```
$ rados rm {fileName} --pool={poolName}
```
