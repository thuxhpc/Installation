# Configure an existing OpenStack installation to enable Docker
## Installing Docker for OpenStack

------
##### **✱ All node**

* 取得最新版Docker
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
 * 在Compute node 上配置Nova 文件
```
$ sudo vim /etc/nova/nova-compute.conf
```
```vim
[DEFAULT]
compute_driver = novadocker.virt.docker.DockerDriver
#compute_driver = libvirt.LibvirtDriver
[libvirt]
virt_type=docker
#virt_type=kvm
```
```
$ sudo vim /etc/nova/nova.conf
```
```vim
..........
#firewall_driver = nova.virt.libvirt.firewall.IptablesFirewallDriver
..........
```
```
$ sudo service nova-compute restart

$ sudo service docker restart
```

------
##### **✱ On Controller node**

* 修改Glance 設定
```
$ sudo vim /etc/glance/glance-api.conf
```
```vim
[DEFAULT]
container_formats = ami,ari,aki,bare,ovf,docker
```
```
$ sudo service glance-api restart

$ sudo service glance-registry restart
```

* 製造Docker 映像檔並存入Glance
```
$ docker pull {IMAGE_NAME}

$ mkdir file

$ tar cf file.tar file

$ tar --delete -f file.tar file

$ docker save {IMAGE_NAME} > file.tar

$ glance image-create --file file.tar --container-format docker --disk-format raw --name {IMAGE_NAME}

$ nova boot --flavor {FLAVOR_TYPE} --image {IMAGE_NAME} {INSTANCE_NAME}
```
