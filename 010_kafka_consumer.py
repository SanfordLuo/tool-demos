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

kafka-console-consumer --topic sanford -group demo_00 --bootstrap-server localhost:9092
(--from-beginning)

jps
"""
from kafka import KafkaConsumer

topic = 'sanford'
bootstrap_servers = ['localhost:9092']
group_id = 'demo_00'


def test_consumer():
    print("===== 消费者 begin =====")
    consumer = KafkaConsumer(topic, group_id=group_id, bootstrap_servers=bootstrap_servers)
    for msg in consumer:
        print("{}:{}:{}: key={} value={}".format(msg.topic, msg.partition, msg.offset, msg.key, msg.value))

    print('===== 消费者 end =====')


if __name__ == '__main__':
    test_consumer()
