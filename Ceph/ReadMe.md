# Ceph-deploy Installation

以 deploy 方式安裝共需四個節點，各自功用分別如下所示

| 節點名稱 |          用途         |      IP       |
|:--------:|:---------------------:|:-------------:|
|   admin  | ceph-deploy           | 172.24.12.102 |
|    mon   | monitor               | 172.24.12.103 |
|   OSD1   | object storage daemon | 172.24.12.104 |
|   OSD2   | object storage daemon | 172.24.12.105 |


```
$ wget -q -O- 'https://download.ceph.com/keys/release.asc' | sudo apt-key add -
```
```
$ echo deb http://download.ceph.com/debian-{ceph-stable-release}/ $(lsb_release -sc) main \
  | sudo tee /etc/apt/sources.list.d/ceph.list
```
```
$ sudo apt-get update && sudo apt-get install ceph-deploy
```
