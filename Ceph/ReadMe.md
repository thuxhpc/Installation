# Ceph-deploy Installation

##### 以 deploy 方式安裝共需四個節點，各自功用分別如下表所示

| 節點名稱 |          用途         |      IP       |
|:--------:|:---------------------:|:-------------:|
|   admin  | ceph-deploy           | 172.24.12.105 |
|    mon   | monitor               | 172.24.12.102 |
|   OSD1   | object storage daemon | 172.24.12.103 |
|   OSD2   | object storage daemon | 172.24.12.104 |

*官方推薦的 Ceph 最小節點配置數量為 3+2，也就是 3 個 mon + 2 個 OSD，但以練習為目的的話以 1+2 的架構便已足夠。*

----

##### 安裝過程中主要是透過 admin node 以 deploy 方式安裝其他節點所需套件，故首先須於 admon node 安裝 ceph-deploy 套件，並設定好 admin 與各節點的 SSH 相關設定。
<br/>
##### **✱ admin node**

* 下載 realase key
```
$ wget -q -O- 'https://download.ceph.com/keys/release.asc' | sudo apt-key add -
```

* 新增 Ceph packages 至 repository
```
$ echo deb http://download.ceph.com/debian-{ceph-stable-release}/ $(lsb_release -sc) main \
  | sudo tee /etc/apt/sources.list.d/ceph.list
```
  > 將 {ceph-stable-release} 更改為需安裝之版本，本次安裝使用版本為 HAMMER。

* 更新並開始安裝 ceph-deploy
```
$ sudo apt-get update && sudo apt-get install ceph-deploy
```




