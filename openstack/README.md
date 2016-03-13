# OpenStack Kilo Installation on Ubuntu 14.04 LTS
## Nova-network

------
##### **✱ all node**

* DNS 設定
```
$ sudo vim /etc/hosts
```
```vim
172.24.12.105  controller
172.24.12.106  compute01
```

* 更新並安裝套件
```
$ sudo apt-get update && sudo apt-get upgrade
$ sudo apt-get install ntp openssh-server
```

------
##### **✱ On Compute nodes **

* 在節點上新增一個帳戶
```
sudo useradd -d /home/{USERNAME} -m {USERNAME}
sudo passwd {USERNAME}
```

* 為此用戶增加 root 權限
```
echo "{USERNAME} ALL = (root) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/{USERNAME}
sudo chmod 0440 /etc/sudoers.d/{USERNAME}
```

------
##### **✱ On Controller nodes **

* 建立 ssh-keygen
```
ssh-keygen
```

* 將公鑰複製到其他節點上做認證使用
```
ssh-copy-id {USERNAME}@{NODE_IP}
```

* 修改設定
```
vim ~/.ssh/config
```
```
Host {COMPUTE_HOSTNAME}
   Hostname {COMPUTE_HOSTNAME}
   User {USERNAME}
```

------

https://www.dropbox.com/s/y1402bdty18y9rx/kilo-20160313.tar?dl=0
