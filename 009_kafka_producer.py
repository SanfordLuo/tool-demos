"""
/usr/local/Cellar/kafka/2.8.0/bin/zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties &
ps aux | grep zookeeper
/usr/local/Cellar/kafka/2.8.0/bin/kafka-server-start /usr/local/etc/kafka/server.properties &
ps aux | grep kafka
kafka-topics --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic sanford
kafka-topics --list --zookeeper localhost:2181
kafka-topics --describe --zookeeper localhost:2181 --topic sanford
kafka-topics --delete --zookeeper localhost:2181 --topic sanford
/usr/local/Cellar/kafka/2.8.0/bin/kafka-server-stop
/usr/local/Cellar/kafka/2.8.0/bin/zookeeper-server-stop

kafka-console-producer --topic sanford --broker-list localhost:9092

jps
"""
import time
from kafka import KafkaProducer

topic = 'sanford'
bootstrap_servers = ['localhost:9092']


def test_producer():
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    print('===== 生产者 begin =====')
    for i in range(1000):
        msg = "msg: %d" % i
        producer.send(topic, msg.encode())
        print(msg)
        time.sleep(0.5)

    producer.close()
    print('===== 生产者 end =====')


if __name__ == '__main__':
    test_producer()
