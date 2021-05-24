#!/bin/bash
source $HOME/.bashrc
if grep isMaster /mnt/var/lib/info/instance.json | grep true;
then
echo "This is master node"
echo "Kafka installations"
sudo -- sh -c 'mkdir -p /downloads;\
mkdir -p /usr/lib/kafka;\
mkdir -p /usr/lib/flume;\
mkdir -p /data/kafka;\
mkdir -p /usr/lib/app; \
cd /downloads;wget https://apache.mirrors.tworzy.net/kafka/2.7.0/kafka_2.12-2.7.0.tgz;\
tar -zxvf kafka_2.12-2.7.0.tgz -C /usr/lib/kafka;\
echo "export KAFKA_HOME=/usr/lib/kafka/kafka_2.12-2.7.0" >> /home/hadoop/.bashrc \
echo "export PATH=$PATH:$KAFKA_HOME/bin" >> /home/hadoop/.bashrc \
'
sudo sed -i 's/tmp\/kafka-logs/data\/kafka/g' /usr/lib/kafka/kafka_2.12-2.7.0/config/server.properties

v_dns=$(curl http://169.254.169.254/latest/meta-data/public-hostname) \
echo $v_dns \

sudo sed -i "/#advertised.listeners=PLAINTEXT:\/\/your.host.name:9092/c\advertised.listeners=PLAINTEXT:\/\/$v_dns:9092" \
/usr/lib/kafka/kafka_2.12-2.7.0/config/server.properties

sudo python3 -m pip install numpy matplotlib pandas seaborn pyspark kafka-python 

fi