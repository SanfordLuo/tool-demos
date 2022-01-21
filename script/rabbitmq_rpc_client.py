import pika
import uuid
import json


class BubbleSortRpcClient(object):
    def __init__(self):
        self.username = 'sanford'
        self.password = '123456'
        self.host = 'localhost'
        self.port = 5672
        self.virtual_host = 'sanford_host'

        credentials = pika.PlainCredentials(username=self.username, password=self.password)
        params = pika.ConnectionParameters(host=self.host,
                                           port=self.port,
                                           virtual_host=self.virtual_host,
                                           credentials=credentials)

        # 创建连接
        self.connection = pika.BlockingConnection(params)

        # 创建信道
        self.channel = self.connection.channel()

        # 声明一个队列用于接收服务端返回结果, exclusive=True 只允许当前连接访问
        result = self.channel.queue_declare(queue='', exclusive=True, durable=True)
        self.callback_queue = result.method.queue

        # 接收服务端返回的结果进行消费
        self.channel.basic_consume(queue=self.callback_queue,
                                   on_message_callback=self.on_response)

    def on_response(self, ch, method, props, body):
        """
        接收到服务端返回的结果的回调函数
        """
        if self.corr_id == props.correlation_id:
            if isinstance(body, str):
                self.response = body
            else:
                self.response = json.loads(body)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self, ls):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        # 请求消息属性设置 reply_to:接收服务端消息的队列
        properties = pika.BasicProperties(delivery_mode=2,
                                          reply_to=self.callback_queue,
                                          correlation_id=self.corr_id)
        # 发送请求消息
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   body=json.dumps(ls),
                                   properties=properties)

        while self.response is None:
            # 保持连接 检查是否有回调
            self.connection.process_data_events()
        return self.response


if __name__ == '__main__':
    bubble_sort = BubbleSortRpcClient()

    ls = [1, 22, 3, 7, 4, 77, 34, 66, 5, 4, 8, 15]
    # ls = '2223'
    print("客户端开始发起请求......")
    response = bubble_sort.call(ls)
    print("服务端计算结果 response: {0}".format(response))
