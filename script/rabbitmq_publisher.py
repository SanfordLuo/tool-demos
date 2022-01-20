"""
AMQP协议: 高级消息队列协议, 进程间传递异步消息的一个网络协议, rabbitmq是基于AMQP协议开发的.
大致工作流程: 生产者(Publisher) ---> 交换机(Exchange) ---> 队列(Queue) ---> 消费者(Consumer)
Broker: 代理, 由Exchange和Queue组成. 连接生产者消费者, 实现AMPQ协议中消息队列和路由功能的进程.
Virtual Host: 虚拟主机, 一个虚拟主机里可以有多个Exchange和Queue, 用于权限控制.
Exchange: 交换机, 接收生产者发送的消息, 并且根据routing_key把消息路由到指定的Queue中去.
Queue: 消息队列, 存储待消费的消息. 由headers和body组成, headers包含生产者添加的消息的各种属性参数, body是真正发送的数据内容.
Binding: 通过routing_key将Exchange与Queue绑定. routing_key不能使任意的字符串,一般用"."分割开,
        例如 "register.shanghai", "register.beijing", "register.#"正则时 *(星号)代表任意一个单词; #(hash)代表0个或者多个单词
Channel: 信道, 消费者与Broker通信的渠道, 建立在TCP连接上的虚拟连接. 一个TCP连接上可以建立好多信道, 减少系统开销提高性能.
1. 简单模式: 最简单的一对一.
2. 工作队列模式: 一对多. 一个生产者对应多个消费者, 但每条消息只能被其中的一个消费者消费.
    轮询分发: 将消息轮流发给每个消费者, 一个消费者处理完才会发送下一个. 例: A消费第1,4,7...条消息, B消费第2,5,8...条消息, C消费第3,6,9...条消息.
    公平分发: 只要有空闲的消费者就给发待处理的消息. 相对于轮询分发提高效率.
3. 发布/订阅模式: 一个生产者产生的消息, 可以同时被多个消费者消费. 生产者将消息发送给broker, 由Exchange将消息转发到绑定在此交换机的每一个Queue中, 消费者监听自己的Queue进行消费.
4. 路由模式: 生产者将消息发送给broker, 由Exchange根据routing_key分发到不同的Queue中, 消费者也根据routing_key找到对应的Queue进行消费.
5. 主题模式: 在路由模式的基础上, routing_key支持正则匹配
6. RPC模式: 通过消息队列实现RPC功能, 客户端发送消息到消费队列, 服务端消费消息执行程序将结果再返回给客户端, 就是把结果发送消息到回调队列.
"""
import pika
import json
import datetime
import time
import random


class TestPublisher(object):

    def __init__(self):
        self.username = 'sanford'
        self.password = '123456'
        self.host = 'localhost'
        self.port = 5672
        self.virtual_host = 'sanford_host'

    def publisher_00(self, msg_type, data):
        """
        简单模式/工作队列模式
        """
        # 创建连接时的登录凭证
        credentials = pika.PlainCredentials(username=self.username, password=self.password)

        # 参数设置
        params = pika.ConnectionParameters(host=self.host,
                                           port=self.port,
                                           virtual_host=self.virtual_host,
                                           credentials=credentials)

        # 创建阻塞式连接
        connection = pika.BlockingConnection(params)

        # 创建信道
        channel = connection.channel()

        # 声明队列 队列持久化: durable=True, 服务重启后队列依然存在
        channel.queue_declare(queue='queue_00', durable=True)

        # 消息属性设置 消息持久化: delivery_mode=2
        properties = pika.BasicProperties(headers={'msg-type': msg_type},
                                          delivery_mode=2)

        # exchange为默认''时routing_key为queue
        channel.basic_publish(exchange='',
                              routing_key='queue_00',
                              body=json.dumps(data),
                              properties=properties)

        connection.close()

    def publisher_01(self, msg_type, data):
        """
        发布/订阅模式(fanout)
        """
        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        params = pika.ConnectionParameters(host=self.host,
                                           port=self.port,
                                           virtual_host=self.virtual_host,
                                           credentials=credentials)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        # 声明交换机指定类型 交换机持久化: durable=True, 服务重启后交换机依然存在
        channel.exchange_declare(exchange='exchange_01', exchange_type='fanout', durable=True)

        properties = pika.BasicProperties(headers={'msg-type': msg_type},
                                          delivery_mode=2)

        # 此模式不需要routing_key进行消费 可以设置为''
        channel.basic_publish(exchange='exchange_01',
                              routing_key='',
                              body=json.dumps(data),
                              properties=properties)

        connection.close()

    def publisher_02(self, msg_type, data):
        """
        路由模式(direct)
        """
        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        params = pika.ConnectionParameters(host=self.host,
                                           port=self.port,
                                           virtual_host=self.virtual_host,
                                           credentials=credentials)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        # 声明交换机指定类型 交换机持久化: durable=True, 服务重启后交换机依然存在
        channel.exchange_declare(exchange='exchange_02', exchange_type='direct', durable=True)

        properties = pika.BasicProperties(headers={'msg-type': msg_type},
                                          delivery_mode=2)

        # 指定routing_key
        channel.basic_publish(exchange='exchange_02',
                              routing_key='routing_key_02',
                              body=json.dumps(data),
                              properties=properties)

        connection.close()

    def publisher_03(self, msg_type, data):
        """
        主题模式(topic),实现分发,
        """
        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        params = pika.ConnectionParameters(host=self.host,
                                           port=self.port,
                                           virtual_host=self.virtual_host,
                                           credentials=credentials)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        # 声明交换机指定类型 交换机持久化: durable=True, 服务重启后交换机依然存在
        channel.exchange_declare(exchange='exchange_03', exchange_type='topic', durable=True)

        properties = pika.BasicProperties(headers={'msg-type': msg_type},
                                          delivery_mode=2)

        # 拼接routing_key
        channel.basic_publish(exchange='exchange_03',
                              routing_key='routing_key.{0}'.format(msg_type),
                              body=json.dumps(data),
                              properties=properties)

        connection.close()


if __name__ == '__main__':
    test_publisher = TestPublisher()

    # 简单模式/工作队列模式
    # msg_type_00 = 'msg_type_00'
    # for i in range(20):
    #     time.sleep(1)
    #     data_00 = {'id': i, 'name': 'jay', 'send_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    #     test_publisher.publisher_00(msg_type_00, data_00)

    # 发布/订阅模式(fanout)
    # msg_type_01 = 'msg_type_01'
    # for i in range(20):
    #     time.sleep(1)
    #     data_01 = {'id': i, 'name': 'jay', 'send_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    #     test_publisher.publisher_01(msg_type_01, data_01)

    # 路由模式(direct)
    # msg_type_02 = 'msg_type_02'
    # for i in range(20):
    #     time.sleep(1)
    #     data_02 = {'id': i, 'name': 'jay', 'send_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    #     test_publisher.publisher_02(msg_type_02, data_02)

    # 主题模式(topic),实现分发
    msg_type_list = ['msg_type_03.0', 'msg_type_03.1', 'msg_type_03.2']
    for i in range(20):
        msg_type_03 = random.choice(msg_type_list)
        time.sleep(1)
        data_03 = {'id': i, 'name': 'jay', 'send_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        test_publisher.publisher_03(msg_type_03, data_03)
