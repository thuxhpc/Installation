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


