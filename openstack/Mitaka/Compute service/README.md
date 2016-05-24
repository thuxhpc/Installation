# OpenStack Liberty Installation on Ubuntu 14.04 LTS 
# **Identity service PART**
---
## ✱ 在MySql中建立Identity的使用者

```
$ sudo su
$ mysql -u root -p
```
將keystone_DBPASS改成你的密碼
```
> CREATE DATABASE keystone;
> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' \
  IDENTIFIED BY 'KEYSTONE_DBPASS';
> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' \
  IDENTIFIED BY 'KEYSTONE_DBPASS';
> exit
```
產生一組亂數文字，後面來取代ADMIN_TOKEN用
```
$openssl rand -hex 10
```
將此字串紀錄起來
```
30302230c4152996f742
```
```
$ echo "manual" > /etc/init/keystone.override
$ apt-get install keystone apache2 libapache2-mod-wsgi -y
```
新增並修改 /etc/keystone/keystone.conf 
P.S. 若原先已有相同的參數，就先註解掉 以免錯誤
```
$ vim /etc/keystone/keystone.conf 
```
將ADMIN_TOKEN取代為前面產生的亂數TOKEN
```vim
[DEFAULT]
...
admin_token = ADMIN_TOKEN
```
將KEYSTONE_DBPASS取代為你的密碼
```vim
[database]
...
connection = mysql+pymysql://keystone:KEYSTONE_DBPASS@controller/keystone
```
```vim
[token]
...
provider = fernet
```
```
$ su -s /bin/sh -c "keystone-manage db_sync" keystone
$ keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
```
修改/etc/apache2/apache2.conf
```
$ vim /etc/apache2/apache2.conf
```
將ServerName controller加上去
```vim
ServerName controller
```

新增並修改/etc/apache2/sites-available/wsgi-keystone.conf
```
$ vim /etc/apache2/sites-available/wsgi-keystone.conf
```
```vim
Listen 5000
Listen 35357

<VirtualHost *:5000>
    WSGIDaemonProcess keystone-public processes=5 threads=1 user=keystone group=keystone display-name=%{GROUP}
    WSGIProcessGroup keystone-public
    WSGIScriptAlias / /usr/bin/keystone-wsgi-public
    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
    ErrorLogFormat "%{cu}t %M"
    ErrorLog /var/log/apache2/keystone.log
    CustomLog /var/log/apache2/keystone_access.log combined

    <Directory /usr/bin>
        Require all granted
    </Directory>
</VirtualHost>

<VirtualHost *:35357>
    WSGIDaemonProcess keystone-admin processes=5 threads=1 user=keystone group=keystone display-name=%{GROUP}
    WSGIProcessGroup keystone-admin
    WSGIScriptAlias / /usr/bin/keystone-wsgi-admin
    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
    ErrorLogFormat "%{cu}t %M"
    ErrorLog /var/log/apache2/keystone.log
    CustomLog /var/log/apache2/keystone_access.log combined

    <Directory /usr/bin>
        Require all granted
    </Directory>
</VirtualHost>
```
將檔案做連結
```
$ ln -s /etc/apache2/sites-available/wsgi-keystone.conf /etc/apache2/sites-enabled
```
重啟服務
```
$ service apache2 restart
$ rm -f /var/lib/keystone/keystone.db
```
---
## ✱ 建立service entity 及 API endpoint
將**ADMIN_TOKEN**改成前面產生的TOEKN，**controller**改成你的controller IP
```
$ export OS_TOKEN=ADMIN_TOKEN
$ export OS_URL=http://controller:35357/v3
$ export OS_IDENTITY_API_VERSION=3
```
如下
```
$ export OS_TOKEN=30302230c4152996f742
$ export OS_URL=http://172.23.2.49:35357/v3
$ export OS_IDENTITY_API_VERSION=3
```
建立 service
```
$ openstack service create \
  --name keystone --description "OpenStack Identity" identity
```
output ↓ (表格內並不一定完全相同，但要類似)
```output
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | OpenStack Identity               |
| enabled     | True                             |
| id          | 6ca4707f6bba423884253c9e7fa29470 |
| name        | keystone                         |
| type        | identity                         |
+-------------+----------------------------------+
```

```
$ openstack endpoint create --region RegionOne \
  identity public http://172.23.2.49:5000/v3
```
```output
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | 5e571ce85ce545828ef162e68cb47165 |
| interface    | public                           |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 6ca4707f6bba423884253c9e7fa29470 |
| service_name | keystone                         |
| service_type | identity                         |
| url          | http://172.23.2.49:5000/v3       |
+--------------+----------------------------------+
```

```
$ openstack endpoint create --region RegionOne \
  identity internal http://172.23.2.49:5000/v3
```
```ouput
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | daa9fc45548e4ebba0feef677a8b7549 |
| interface    | internal                         |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 6ca4707f6bba423884253c9e7fa29470 |
| service_name | keystone                         |
| service_type | identity                         |
| url          | http://172.23.2.49:5000/v3       |
+--------------+----------------------------------+
```

```
$ openstack endpoint create --region RegionOne \
  identity admin http://172.23.2.49:35357/v3
```
```
+--------------+----------------------------------+
| Field        | Value                            |
+--------------+----------------------------------+
| enabled      | True                             |
| id           | f75d467e28854cd28aa33177bbf8b312 |
| interface    | admin                            |
| region       | RegionOne                        |
| region_id    | RegionOne                        |
| service_id   | 6ca4707f6bba423884253c9e7fa29470 |
| service_name | keystone                         |
| service_type | identity                         |
| url          | http://172.23.2.49:35357/v3      |
+--------------+----------------------------------+
```
------
## ✱ Create a domain, projects, users, and roles

```
$ openstack domain create --description "Default Domain" default
```
```output
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | Default Domain                   |
| enabled     | True                             |
| id          | b999b28364ec4647ba79f988db9b48e2 |
| name        | default                          |
+-------------+----------------------------------+
```

```
$ openstack project create --domain default \
  --description "Admin Project" admin
```
```
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | Admin Project                    |
| domain_id   | b999b28364ec4647ba79f988db9b48e2 |
| enabled     | True                             |
| id          | edd30189734b4eb5bd29fc0c95135558 |
| is_domain   | False                            |
| name        | admin                            |
| parent_id   | b999b28364ec4647ba79f988db9b48e2 |
+-------------+----------------------------------+
```
```
$ openstack user create --domain default \
  --password-prompt admin
```
```output
+-----------+----------------------------------+
| Field     | Value                            |
+-----------+----------------------------------+
| domain_id | b999b28364ec4647ba79f988db9b48e2 |
| enabled   | True                             |
| id        | 9923104b7a0348e0bd96dc5cdf0b7b6b |
| name      | admin                            |
+-----------+----------------------------------+

```
```
$ openstack role create admin
```
```output
+-----------+----------------------------------+
| Field     | Value                            |
+-----------+----------------------------------+
| domain_id | None                             |
| id        | 95b3e7db97e04322a131c01f19a926ca |
| name      | admin                            |
+-----------+----------------------------------+
```
↓這行不會有output
```
$ openstack role add --project admin --user admin admin
```
```
$ openstack project create --domain default \
  --description "Service Project" service
```
```
+-------------+----------------------------------+
| Field       | Value                            |
+-------------+----------------------------------+
| description | Service Project                  |
| domain_id   | b999b28364ec4647ba79f988db9b48e2 |
| enabled     | True                             |
| id          | 2939b9abdf0444e6982ae0515e2af8cd |
| is_domain   | False                            |
| name        | service                          |
| parent_id   | b999b28364ec4647ba79f988db9b48e2 |
+-------------+----------------------------------+

```
## ✱ Verify operation
---
```
$ unset OS_TOKEN OS_URL
```
```
$ openstack --os-auth-url http://172.23.2.49:35357/v3 \
  --os-project-domain-name default --os-user-domain-name default \
  --os-project-name admin --os-username admin token issue
```
```
+------------+---------------------------------------------------------------------------------+
| Field      | Value                                                                           |                                                                                                                       |
+------------+---------------------------------------------------------------------------------+
| expires    | 2016-05-20T10:25:06.927064Z                                                     |                                                                                                                       |
| id         | gAAAAABXPtf3280y3Vd8flEl0UAI1-GW0HHeQiB6kDE0uMfqbYFuZ1_J0Ss1X2ESivywiAHqJIPRR0k2F88YF8jLBt2KOxi8M4qpueg9DluW7wZmwbNz9r06YGtqr7rXE4Wim1etw_Fz-fEmLLCwMfRJuMgiqOT5FacWUmUFrOWxURRB9kmq-hY         |
| project_id | edd30189734b4eb5bd29fc0c95135558                                                |                                                                                                                       |
| user_id    | 9923104b7a0348e0bd96dc5cdf0b7b6b                                                |                                                                                                                       |
+------------+---------------------------------------------------------------------------------+
```

```
$ openstack --os-auth-url http://controller:5000/v3 \
  --os-project-domain-name default --os-user-domain-name default \
  --os-project-name demo --os-username demo token issue
 ```
 
 ```
 +------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Field      | Value                                                                                                                                                                                  |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| expires    | 2016-05-20T10:25:06.927064Z                                                                                                                                                            |
| id         | gAAAAABXPtf3280y3Vd8flEl0UAI1-GW0HHeQiB6kDE0uMfqbYFuZ1_J0Ss1X2ESivywiAHqJIPRR0k2F88YF8jLBt2KOxi8M4qpueg9DluW7wZmwbNz9r06YGtqr7rXE4Wim1etw_Fz-fEmLLCwMfRJuMgiqT5FacWUmUFrOWxURRB9kmq-hY |
| project_id | edd30189734b4eb5bd29fc0c95135558                                                                                                                                                       |
| user_id    | 9923104b7a0348e0bd96dc5cdf0b7b6b                                                                                                                                                       |
+------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
 ```
 ---
 ## ✱ Creating the scripts
 ```
 $ cd ~
 $ vim admin-openrc
 ```
 把ADMIN_PASS改成自己的密碼
 
 把controller 改成自己的controller IP
 ```
export OS_PROJECT_DOMAIN_NAME=default
export OS_USER_DOMAIN_NAME=default
export OS_PROJECT_NAME=admin
export OS_USERNAME=admin
export OS_PASSWORD=ADMIN_PASS
export OS_AUTH_URL=http://controller:35357/v3
export OS_IDENTITY_API_VERSION=3
export OS_IMAGE_API_VERSION=2
 ```
 


