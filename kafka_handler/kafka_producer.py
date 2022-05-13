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
import json
from kafka import KafkaProducer

topic = 'sanford'
bootstrap_servers = 'localhost:9092'


def test_producer():
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                             key_serializer=lambda k: json.dumps(k).encode(),
                             value_serializer=lambda m: json.dumps(m).encode())

    data = {'name': 'jay', 'timestamp': int(time.time() * 1000)}

    try:
        future = producer.send(topic=topic, value=data)
        future.get(timeout=10)
    except Exception as e:
        print('生产者发送失败:{0}'.format(e))
    else:
        print('生产者发送成功')


if __name__ == '__main__':
    test_producer()
