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
import json
from kafka import KafkaConsumer

topic = 'KAFKA_COURSE_TOPIC'
group_id = 'sanford'
bootstrap_servers = 'localhost:9092'
# auto_offset_reset = 'earliest'  # 从未消费的开始消费
auto_offset_reset = 'latest'  # 从最新生产的开始的消费


def test_consumer():
    try:
        consumer = KafkaConsumer(
            topic,
            group_id=group_id,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset=auto_offset_reset)
        for msg in consumer:
            print(msg.value)
            # print('data:{0}'.format(json.loads(msg.value)))
            consumer.commit()
    except Exception as e:
        print('消费者接收失败:{0}'.format(e))


if __name__ == '__main__':
    test_consumer()
