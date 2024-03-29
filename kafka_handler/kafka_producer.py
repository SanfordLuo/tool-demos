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

# kafka自带的zookeeper启动
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
bin/kafka-topics.sh --list --bootstrap-server  localhost:9092
bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 --topic sanford
bin/kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic sanford

jps
"""
import time
import json
import random
from kafka import KafkaProducer

topic = 'databus'
bootstrap_servers = '10.60.0.163:9092'


def test_producer(teacher_id):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                             key_serializer=lambda k: json.dumps(k).encode(),
                             value_serializer=lambda m: json.dumps(m).encode())

    data = {
        "subject_id": 777,
        "intelligent": 888,
        "type": 1,
        "reqId": "new_20220914_04",
        "exerciseSource": 7,
        "resourceId": 560968,
        "key": "560968",
        "studentExerciseList": [
            {
                "id": 1268011,
                "studentId": 82952857479,
                "classId": 78790,
                "year": 2021,
                "result": "1",
                "correctorRole": "student",
                "question_id": 16994302,
                "parent_id": 0,
                "minicourse_id": 334823,
                "node_index": 4,
                "content_index": 2,
                "history_result": None,
                "correctStatus": None
            }
        ],
        "kid": -1,
        "ktype": -1
    }

    try:
        future = producer.send(topic=topic, value=data, key=teacher_id)
        future.get(timeout=10)
    except Exception as e:
        print('生产者发送失败:{0}'.format(e))
    else:
        print('生产者发送成功')


if __name__ == '__main__':
    test_producer(1)
