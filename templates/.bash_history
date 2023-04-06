sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10
cd ~
python hello.py
python app.py
sudo apt-get update
sudo apt-get install -y python3-pip
pip3 --version
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
pip install flask
python app.py
wget -qO - https://www.mongodb.org/static/pgp/server-4.2.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.2.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo service mongod start
mongo
sudo service mongod restart
sudo vi /etc/mongod.conf
sudo service mongod restart
:~$ pip install requests beautifulsoup4 ptmo
pip install requests beautifulsoup4 pymongo
python app.py
sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 5000
python app.py
# 아래의 명령어로 실행하면 된다
nohup python app.py &
s
ps -ef | grep 'app.py'
kill -9 30820
kill -9 30828
nohup python app.py &
exit
cd ~
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10
pip3 --version
mongo
exit
ps -ef | grep 'app.py'
kill -9 30880
nohup python app.py &
ps -ef | grep 'app.py'
kill -9 32302
ps -ef | grep 'app.py'
kill -9 32310
nohup python app.py &
ps -ef | grep 'app.py'
kill -9 32498
ps -ef | grep 'app.py'
kill -9 32506
ps -ef | grep 'app.py'
nohup python app.py &
ps -ef | grep 'app.py'
kill -9 32734
nohup python app.py &
ps -ef | grep 'app.py'
kill -9 407
nohup python app.py &
ps -ef | grep 'app.py'
kill -9 1006
ps -ef | grep 'app.py'
nohup python app.py &
exit
sudo service mongod start
sudo vi /etc/mongod.comf
sudo vi /etc/mongod.conf
python dbcreate.py
nohup python main.py &
