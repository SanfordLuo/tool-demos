"""
rabbitmq 生产者demo
1.单生产单消费模型：即完成基本的一对一消息转发。
2.消息分发模型：多个收听者监听一个队列。
3.fanout消息订阅模式：生产者将消息发送到Exchange，Exchange再转发到与之绑定的Queue中，每个消费者再到自己的Queue中取消息。
4.direct路由模式：此时生产者发送消息时需要指定RoutingKey，即路由Key，Exchange接收到消息时转发到与RoutingKey相匹配的队列中。
5.topic匹配模式：更细致的分组，允许在RoutingKey中使用匹配符。
6.RPC远程过程调用：客户端与服务器之间是完全解耦的，即两端既是消息的发送者也是接受者。

channel： 信道是生产者，消费者和 RabbitMQ 通信的渠道，是建立在 TCP 连接上的虚拟连接。一个 TCP 连接上可以建立成百上千个信道，通过这种方式，可以减少系统开销，提高性能。
Broker： 接收客户端连接，实现 AMQP 协议的消息队列和路由功能的进程。
Virtual Host： 虚拟主机的概念，类似权限控制组，一个 Virtual Host 里可以有多个 Exchange 和 Queue，权限控制的最小粒度是 Virtual Host。
Exchange： 交换机，接收生产者发送的消息，并根据 Routing Key 将消息路由到服务器中的队列 Queue。
ExchangeType： 交换机类型决定了路由消息的行为，RabbitMQ 中有三种 Exchange 类型，分别是 direct、fanout、topic。
Message Queue： 消息队列，用于存储还未被消费者消费的消息，由 Header 和 body 组成。
        Header 是由生产者添加的各种属性的集合，包括 Message 是否被持久化、优先级是多少、由哪个 Message Queue 接收等，body 是真正需要发送的数据内容。
BindingKey： 绑定关键字，将一个特定的 Exchange 和一个特定的 Queue 绑定起来。
"""
import pika
import json
import time


def test_publish_01(data):
    credentials = pika.PlainCredentials(username='sanford', password='123456')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
                                                                   port=5672,
                                                                   virtual_host='sanford_host',
                                                                   credentials=credentials))

    channel = connection.channel()
    channel.exchange_declare(exchange='sanford_exchange',
                             durable=True,
                             exchange_type='topic')

    channel.queue_declare(queue='sanford_topic_queue', durable=True)

    channel.basic_publish(exchange='sanford_exchange',
                          routing_key='sanford_routing_key',
                          body=json.dumps(data),
                          properties=pika.BasicProperties(headers={'msg-type': 'sanford_test'}))

    connection.close()


if __name__ == '__main__':
    data = {'name': 'jay', 'timestamp': int(time.time() * 1000)}

    test_publish_01(data)
