# Configure an existing OpenStack installation to enable Docker
## Installing Docker for OpenStack

------
##### **✱ All node**

* 取的最新版Docker
```
$ sudo apt-get install apt-transport-https
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
$ sudo bash -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"
$ sudo apt-get update
$ sudo apt-get install -y lxc-docker
```

------
##### **✱ On Compute node**

* 修改Nova 權限
```
$ sudo usermod -G docker nova
$ sudo chmod 666 /var/run/docker.sock
$ sudo chmod 777 /var/run/libvirt/libvirt-sock
```

* 在Compute node 上安裝Nova-docker
```
$ sudo apt-get install python-pip python-dev -y
$ git clone -b stable/kilo https://github.com/stackforge/nova-docker.git
$ cd nova-docker
$ sudo python setup.py install
$ sudo pip list | grep nova-docker
$ sudo cp nova-docker/etc/nova/rootwrap.d/docker.filters \
  /etc/nova/rootwrap.d/
```

------
##### **✱ On Controller node**

* 切換 root 身分
```
$ sudo su
```
> 以下皆用 root 身分操作

* 建立 ssh-keygen
```
$ ssh-keygen
```

* 將公鑰複製到其他節點上做認證使用
```
$ ssh-copy-id {USERNAME}@{NODE_IP}
```

* 修改設定
```
$ vim ~/.ssh/config
```
```
Host {COMPUTE_HOSTNAME}
   Hostname {COMPUTE_HOSTNAME}
   User {USERNAME}
```

------
* 下載 Script
```
# wget https://www.dropbox.com/s/y1402bdty18y9rx/kilo-20160313.tar
```

* 解壓縮並進入資料夾
```
# tar xvf kilo-20160313.tar && cd kilo-20160313
```

* 開始安裝
```
# sh Setup.sh
```
> 安裝後需輸入節點IP，設定各項服務密碼，以及 compute node 的對外與橋接網卡名稱

------

* 驗證
```
http://{CONTROLLER_IP}/horizon/
```
> 前往網站驗證各項服務
