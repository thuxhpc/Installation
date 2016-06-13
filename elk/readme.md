#### ORACLE JAVA 8
###### sudo add-apt-repository -y ppa:webupd8team/java

###### sudo apt-get update

###### sudo apt-get -y install oracle-java8-installer

###### java -version

#### ELASTICSEARCH 安裝應用程式步驟
###### wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

###### echo "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list
 
###### sudo apt-get update

###### sudo apt-get -y install elasticsearch

###### sudo vim/etc/elasticsearch/elasticsearch.yml 
network.host	: IP Address
http.port		: 9200

###### sudo service elasticsearch restart

###### sudo update-rc.d elasticsearch defaults 95 10

###### curl -X GET ‘http://192.168.244.228:9200’

#### KIBANA 安裝應用程式步驟
###### cd ~; wget https://download.elastic.co/kibana/kibana/kibana-4.5.0-linux-x64.tar.gz
 
###### tar xvf kibana-*.tar.gz

###### sudo vim ~/kibana-4*/config/kibana.yml
server.port		: 5601
server.host		: "IP Address"
elasticsearch.url	: http://IP Address:9200

###### sudo mkdir -p /opt/kibana

###### sudo cp -R ~/kibana-4*/* /opt/kibana/

###### cd /etc/init.d && sudo wget https://gist.githubusercontent.com/thisismitch/8b15ac909aed214ad04a/raw/bce61d85643c2dcdfbc2728c55a41dab444dca20/kibana4

###### sudo chmod +x /etc/init.d/kibana4

###### sudo update-rc.d kibana4 defaults 96 9

###### sudo service kibana4 start

###### bin/kibana version

#### 安裝 NGINX服務步驟
###### sudo apt-get install nginx -y apache2-utils

###### sudo htpasswd -c /etc/nginx/htpasswd.users kibanaadmin
###### Password: admin

###### sudo vim /etc/nginx/sites-available/default

###### 加上下面的程式碼及IP Address
server {
    listen 80;

    server_name <your ip here>;

    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/htpasswd.users;

    location / {
       proxy_pass http://<your ip here>:5601;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;        
    }
}

###### sudo service nginx restart

#### 安裝 LOGSTASH應用程式步驟 

###### echo 'deb http://packages.elasticsearch.org/logstash/2.3/debian stable main' | sudo tee /etc/apt/sources.list.d/logstash.list

###### sudo apt-get update

###### sudo apt-get install logstash

###### sudo service logstash start

###### cd /opt/logstash

###### bin/logstash --version

#### K.	產生SSL憑證及設定Logstash Configuration文件
###### sudo mkdir -p /etc/certs

###### sudo vim /etc/ssl/openssl.cnf

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

###### 

