# Install-02BasicEnvironment.sh
#!/bin/bash

############################################################

## OpenStack packages ##

# Install the Ubuntu Cloud archive keyring and repository
sudo apt-get install ubuntu-cloud-keyring
echo -n "deb http://ubuntu-cloud.archive.canonical.com/ubuntu" \
  "trusty-updates/kilo main" > /etc/apt/sources.list.d/cloudarchive-kilo.list

# Upgrade the packages on your system
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install -y ntp

############################################################

## SQL database ##

# Install SQL database
sudo apt-get install -y mariadb-server python-mysqldb

# Create and edit the /etc/mysql/conf.d/mysqld_openstack.cnf file and complete the following actions
sudo echo "[mysqld]\nbind-address = ${CONTROLLER_IP}\n\n[mysqld]\ndefault-storage-engine = innodb\ninnodb_file_per_table\ncollation-server = utf8_general_ci\ninit-connect = 'SET NAMES utf8'\ncharacter-set-server = utf8" | sudo tee /etc/mysql/conf.d/mysqld_openstack.cnf

# Restart the database service
sudo service mysql restart

# Secure the database service
echo -e "\n${DB_PASS}\nn\ny\ny\ny\ny" | sudo mysql_secure_installation

############################################################

## Message queue ##

# To install the message queue service
sudo apt-get install -y rabbitmq-server

# To configure the message queue service
sudo rabbitmqctl add_user openstack ${DB_PASS}
sudo rabbitmqctl set_permissions openstack ".*" ".*" ".*"