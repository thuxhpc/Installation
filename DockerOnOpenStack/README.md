# Configure an existing OpenStack installation to enable Docker
## Installing Docker for OpenStack

------
##### **✱ all node**

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

* 在節點上新增一個帳戶
```
$ sudo useradd -d /home/{USERNAME} -m {USERNAME}
$ sudo passwd {USERNAME}
```

* 為此用戶增加 root 權限
```
$ echo "{USERNAME} ALL = (root) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/{USERNAME}
$ sudo chmod 0440 /etc/sudoers.d/{USERNAME}
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
