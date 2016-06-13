OwnCloud On FreeNAS
#### 基本環境:<br>
VM Platform: VMware Workstation 12 VM OS: FreeNAS 9.3<br>
VM RAM: 4096MB VM HD: 20GBs<br>
FreeNAS環境已安裝完成<br><br>

#### 安裝方法:<br>
登入Plugins選單，點擊ownCloud<br>
選擇OwnCLoud後，點選Install按鈕，接著按OK<br>
之後點擊Edit Jail<br>
將ip address改成外網ip address<br>
重新啟動OwnCloud<br>
在FreeNAS網頁端選擇Jails > Add Storage<br>
輸入資料來源(owncloud_1)以及目的路徑(/media)<br>
登入Plugins > owncloud後點擊here連接<br>
輸入FreeNAS帳號以及密碼 , 帳號：root; 密碼：freenas<br>
OwnCloud首頁可看到有兩個預設資料夾 “Documents” 以及 “Photos”
