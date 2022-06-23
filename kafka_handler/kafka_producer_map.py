import time
import json
import random
from kafka import KafkaProducer
from multiprocessing import Pool

topic = 'sanford'
bootstrap_servers = 'localhost:9092'


def test_producer(teacher_id):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                             key_serializer=lambda k: json.dumps(k).encode(),
                             value_serializer=lambda m: json.dumps(m).encode())

    data = {
        "create_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "request_id": 'test_' + str(int(time.time() * 1000)),
        "data": {
            "minicourse_id": 902937,
            "teacher_ids": [
                teacher_id
            ]
        }
    }

    for i in range(random.randint(1, 2)):
        try:
            future = producer.send(topic=topic, value=data, key=teacher_id)
        except Exception as e:
            print('生产者发送失败:{0}'.format(e))
        else:
            print('生产者发送成功')


if __name__ == '__main__':
    start = int(time.time() * 1000)
    with Pool(processes=10) as pool:
        pool.map(test_producer, [i for i in range(1, 600)])
    end = int(time.time() * 1000)
    print(end - start)
