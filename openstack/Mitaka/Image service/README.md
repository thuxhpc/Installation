# OpenStack Liberty Installation on Ubuntu 14.04 LTS 
# **Image service PART**
---
## ✱ Install and configure
```
$ mysql -u root -p
```
```
> CREATE DATABASE glance;
```
把GLANCE_DBPASS改成自己的密碼
```
GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' \
  IDENTIFIED BY 'GLANCE_DBPASS';
GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' \
  IDENTIFIED BY 'GLANCE_DBPASS';
```
```
> exit
```

```
$ cd ~
$source admin-openrc
```
```
$ openstack user create --domain default --password-prompt glance
```
```
+-----------+----------------------------------+
| Field     | Value                            |
+-----------+----------------------------------+
| domain_id | b999b28364ec4647ba79f988db9b48e2 |
| enabled   | True                             |
| id        | 41cb77c4e92c4be2a83d6583b0c9b2f5 |
| name      | glance                           |
+-----------+----------------------------------+
```
這行指令不會有輸出
```
$ openstack role add --project service --user glance admin
```
```
$ openstack service create --name glance \
  --description "OpenStack Image" image
```
```
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | OpenStack Image                  |
| enabled     | True                             |
| id          | 5b816f4d4ce748c09180e7539c0c849c |
| name        | glance                           |
| type        | image                            |
+-------------+----------------------------------+
```
將controller 改成自己的controller IP
```
$ openstack endpoint create --region RegionOne \
  image public http://controller:9292
$ openstack endpoint create --region RegionOne \
  image internal http://controller:9292
$ openstack endpoint create --region RegionOne \
  image admin http://controller:9292
```

```
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | e45f71db366846ad9599dd2d6a06c47a |
| interface    | public                           |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 5b816f4d4ce748c09180e7539c0c849c |
| service_name | glance                           |
| service_type | image                            |
| url          | http://172.23.2.49:9292          |
+--------------+----------------------------------+
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | 0cc6a46eb0d84bc99bc7fd3d15c497cf |
| interface    | internal                         |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 5b816f4d4ce748c09180e7539c0c849c |
| service_name | glance                           |
| service_type | image                            |
| url          | http://172.23.2.49:9292          |
+--------------+----------------------------------+
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | 1ad819187fc54beeb712c517e7fa9c3a |
| interface    | admin                            |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 5b816f4d4ce748c09180e7539c0c849c |
| service_name | glance                           |
| service_type | image                            |
| url          | http://172.23.2.49:9292          |
+--------------+----------------------------------+
```
## ✱ Install and configure components
```
$ apt-get install glance -y
```
```
$ vim /etc/glance/glance-api.conf
```
將**GLANCE_DBPASS** 改成自己的密碼
```vim
[database]
...
connection = mysql+pymysql://glance:GLANCE_DBPASS@controller/glance
```
將controller 改成自己的controller IP

GLANCE_PASS改成自己的密碼
```
[keystone_authtoken]
...
auth_uri = http://controller:5000
auth_url = http://controller:35357
memcached_servers = controller:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = glance
password = GLANCE_PASS
```
```
[glance_store]
...
stores = file,http
default_store = file
filesystem_store_datadir = /var/lib/glance/images/
```
```
$ vim /etc/glance/glance-registry.conf
```
將controller改成controller ip

GLANCE_PASS改成自己的密碼
```
[database]
...
connection = mysql+pymysql://glance:GLANCE_DBPASS@controller/glance

[keystone_authtoken]
...
auth_uri = http://controller:5000
auth_url = http://controller:35357
memcached_servers = controller:11211
auth_type = password
project_domain_name = default
user_domain_name = default
project_name = service
username = glance
password = GLANCE_PASS

[paste_deploy]
...
flavor = keystone
```

```
$ su -s /bin/sh -c "glance-manage db_sync" glance
```

```
$ service glance-registry restart
$ service glance-api restart
```
---
## ✱ Verify operation
```
$ source admin-openrc
$ wget http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img
$ openstack image create "cirros" \
  --file cirros-0.3.4-x86_64-disk.img \
  --disk-format qcow2 --container-format bare \
  --public
```
```
+------------------+------------------------------------------------------+
| Field            | Value                                                |
+------------------+------------------------------------------------------+
| checksum         | ee1eca47dc88f4879d8a229cc70a07c6                     |
| container_format | bare                                                 |
| created_at       | 2016-05-23T12:05:16Z                                 |
| disk_format      | qcow2                                                |
| file             | /v2/images/03c6a1e9-cb9f-4d2e-afff-955423a06091/file |
| id               | 03c6a1e9-cb9f-4d2e-afff-955423a06091                 |
| min_disk         | 0                                                    |
| min_ram          | 0                                                    |
| name             | cirros                                               |
| owner            | edd30189734b4eb5bd29fc0c95135558                     |
| protected        | False                                                |
| schema           | /v2/schemas/image                                    |
| size             | 13287936                                             |
| status           | active                                               |
| tags             |                                                      |
| updated_at       | 2016-05-23T12:05:16Z                                 |
| virtual_size     | None                                                 |
| visibility       | public                                               |
+------------------+------------------------------------------------------+

```
```
$ openstack image list
```
```
+--------------------------------------+--------+--------+
| ID                                   | Name   | Status |
+--------------------------------------+--------+--------+
| 03c6a1e9-cb9f-4d2e-afff-955423a06091 | cirros | active |
+--------------------------------------+--------+--------+
```



