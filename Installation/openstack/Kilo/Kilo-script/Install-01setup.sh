# Install-01setup.sh
#!/bin/bash

############################################################

clear

echo "Input controller IP"
read CONTROLLER_IP
export CONTROLLER_IP

echo "\nInput DB_PASS:"
#stty -echo
read DB_PASS
export DB_PASS
#stty echo

echo "\nInput RABBIT_PASS:"
#stty -echo
read RABBIT_PASS
export RABBIT_PASS
#stty echo

echo "\nInput KEYSTONE_DBPASS:"
#stty -echo
read KEYSTONE_DBPASS
export KEYSTONE_DBPASS
#stty echo

############################################################

# sudo 免密碼設定
export USER
echo "${USER} ALL = (root) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/${USER}
echo sudo chmod 0440 /etc/sudoers.d/${USER}

# SQL 免密碼設定
echo -n "[client]\npassword=${DB_PASS}" | sudo tee ~/.my.cnf

# vim 設定
echo -n "set background=dark\n:set nu" | sudo tee ~/.vimrc

clear

############################################################

echo "\n\nSystem: Preparing to Install...\n"
sleep 1
echo "5\n"
sleep 1
echo "4\n"
sleep 1
echo "3\n"
sleep 1
echo "2\n"
sleep 1
echo "1\n"
sleep 1

clear

############################################################

sh Install-02BasicEnvironment.sh
sh Install-03AddTheIdentityService.sh

############################################################