    # OpenStack Liberty Installation on Ubuntu 14.04 LTS

## ↓↓↓ Neutron 架構 ↓↓↓
##### ✱  1 controller node 
- 2張網卡
##### ✱ 1 compute node 
- 1張網卡
##### ✱ 1 network node 
- 2張網卡

# **若網卡設為static則需要再設定的地方開啟briged選項**
# IP部份請照自己情況設置，對應的地方請注意
---
## 網路設定

##### **✱ all node**

* DNS 設定
```
$ sudo vim /etc/hosts
```

```vim
172.23.2.49   controller
172.23.2.50   network
172.23.2.51   compute01
```
IP位置可自行調整

------
##### ✱ controller node 
* 設定hostname
```
$sudo vim /etc/hostname
```
```vim
controller
```
* 網卡設定
```
$sudo vim /etc/network/interfaces
```
```vim
auto eth0
iface eth0 inet static
address 140.128.101.69
gateway 140.128.101.250
netmask 255.255.255.0
dns-nameservers 8.8.8.8

auto eth1
iface eth1 inet static
address 172.23.2.49
netmask 255.255.255.0

```
```
$sudo reboot
```
---
##### ✱ network  node 
* 設定hostname
```
$sudo vim /etc/hostname
```
```vim
network
```

* 網卡設定
```
$sudo vim /etc/network/interfaces
```
```vim
auto eth0
iface eth0 inet static
address 172.23.2.50
netmask 255.255.255.0
gateway 172.23.2.254
dns-nameservers 8.8.8.8

auto eth1
iface eth1 inet manual
        up ip link set dev $IFACE up
        down ip link  set dev $IFACE down

```
* reboot
```
$sudo reboot
```
------


##### ✱ compute01 node 
* 設定hostname
```
$sudo vim /etc/hostname
```
```vim
compute01
```

* 網卡設定
```
$sudo vim /etc/network/interfaces
```
```vim
auto eth0
iface eth0 inet static
address 172.23.2.51
netmask 255.255.255.0
gateway 172.23.2.254
dns-nameservers 8.8.8.8
```
* reboot
```
$sudo reboot
```
##### ✱ all node 
對8.8.8.8 ping 測試網路是否有通
```
$ping 8.8.8.8
```
對內則 (以controller 為例 以此類推)
```
$ping compute01
$pint network
```

------
## ✱ 安裝OpenStack 套件(all node )
```
$ sudo apt-get install -y software-properties-common
$ sudo add-apt-repository -y cloud-archive:mitaka
```
更新&安裝 套件
```
$sudo apt-get update -y &&sudo apt-get dist-upgrade -y
```
安裝 OpenStack client
```
$sudo apt-get install python-openstackclient -y
```
reboot
```
$sudo reboot
```

---
## ✱ 安裝SQL Databse (controller node)

P.S. 安裝過程中需要輸入密碼
```
$sudo apt-get install mariadb-server python-pymysql -y
```
建立並修改 /etc/mysql/conf.d/openstack.cnf
```
$sudo vim /etc/mysql/conf.d/openstack.cnf
```
```vim
[mysqld]
bind-address = 172.23.2.49

default-storage-engine = innodb
innodb_file_per_table
collation-server = utf8_general_ci
character-set-server = utf8
```
restart mysql service
```
$sudo service mysql restart
```
secure設定 順序N/Y/Y/Y/Y
```
$mysql_secure_installation
```
---
## ✱ 安裝Message queue
```
$sudo apt-get install rabbitmq-server -y
```
將RABBIT_PASS更改為你要的密碼
```
$sudo rabbitmqctl add_user openstack RABBIT_PASS
$sudo rabbitmqctl set_permissions openstack ".*" ".*" ".*"
```
---
## ✱ 安裝Memcached
```
$sudo apt-get install memcached python-memcache -y
```
```
$sudo vim /etc/memcached.conf
```
將檔案內原先的-l 127.0.0.1，取代為自己的IP，如下
```
-l 172.23.2.49
```
restart service
```
$sudo service memcached restart
```


























