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
import time
import random
import datetime
import sys


class TestConsumer(object):

    def __init__(self):
        self.username = 'sanford'
        self.password = '123456'
        self.host = 'localhost'
        self.port = 5672
        self.virtual_host = 'sanford_host'

    @staticmethod
    def callback_00(channel, method, properties, body):
        """
        回调函数
        """
        time.sleep(random.randint(1, 10))
        headers = properties.headers
        data = json.loads(body)
        data['end_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(headers, data)
        # 手动确认已经消费成功 当auto_ack=False时
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def consumer_00(self):
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

        # 公平分发(没有这行时为轮询分发) prefetch_count=1如果消费者中有一条消息没处理完就不会继续给这个消费者继续发消息
        channel.basic_qos(prefetch_count=1)

        # auto_ack=True 自动确认已经消费成功
        channel.basic_consume(queue='queue_00',
                              on_message_callback=self.callback_00)

        channel.start_consuming()

    def consumer_01(self):
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

        # 声明队列, queue为空字符串时会创建唯一的队列名. exclusive=True, 仅允许当前的连接访问
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # 通过路由键将队列和交换器绑定, 此模式不需要routing_key进行消费 可以默认为None
        channel.queue_bind(exchange='exchange_01', queue=queue_name)

        channel.basic_consume(queue=queue_name,
                              on_message_callback=self.callback_00)

        channel.start_consuming()

    def consumer_02(self):
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

        # 声明队列, queue为空字符串时会创建唯一的队列名. exclusive=True, 仅允许当前的连接访问
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # 通过路由键将队列和交换器绑定, 此模式需要routing_key进行消费
        channel.queue_bind(exchange='exchange_02', queue=queue_name, routing_key='routing_key_02')

        channel.basic_consume(queue=queue_name,
                              on_message_callback=self.callback_00)

        channel.start_consuming()

    def consumer_03_0(self):
        """
        主题模式(topic),实现分发 routing_key.msg_type_03.0
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

        # 声明队列, queue为空字符串时会创建唯一的队列名. exclusive=True, 仅允许当前的连接访问
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # 通过路由键将队列和交换器绑定, 此模式需要routing_key进行消费
        channel.queue_bind(exchange='exchange_03', queue=queue_name, routing_key='routing_key.msg_type_03.0')

        channel.basic_consume(queue=queue_name,
                              on_message_callback=self.callback_00)

        channel.start_consuming()

    def consumer_03_1(self):
        """
        主题模式(topic),实现分发 routing_key.msg_type_03.1
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

        # 声明队列, queue为空字符串时会创建唯一的队列名. exclusive=True, 仅允许当前的连接访问
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # 通过路由键将队列和交换器绑定, 此模式需要routing_key进行消费
        channel.queue_bind(exchange='exchange_03', queue=queue_name, routing_key='routing_key.msg_type_03.1')

        channel.basic_consume(queue=queue_name,
                              on_message_callback=self.callback_00)

        channel.start_consuming()

    def consumer_03_2(self):
        """
        主题模式(topic),实现分发 routing_key.msg_type_03.#
        * (星号) 代表任意 一个单词
        # (hash) 0个或者多个单词
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

        # 声明队列, queue为空字符串时会创建唯一的队列名. exclusive=True, 仅允许当前的连接访问
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue

        # 通过路由键将队列和交换器绑定, 此模式需要routing_key进行消费
        channel.queue_bind(exchange='exchange_03', queue=queue_name, routing_key='routing_key.msg_type_03.#')

        channel.basic_consume(queue=queue_name,
                              on_message_callback=self.callback_00)

        channel.start_consuming()


if __name__ == '__main__':
    test_consumer = TestConsumer()

    # 简单模式/工作队列模式
    # test_consumer.consumer_00()

    # 发布/订阅模式(fanout)
    # test_consumer.consumer_01()

    # 路由模式(direct)
    # test_consumer.consumer_02()

    # 主题模式(topic),实现分发
    if sys.argv[1] == '0':
        test_consumer.consumer_03_0()
    elif sys.argv[1] == '1':
        test_consumer.consumer_03_1()
    elif sys.argv[1] == '2':
        test_consumer.consumer_03_2()
