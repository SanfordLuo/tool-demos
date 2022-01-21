import pika
import json


def bubble_sort(ls):
    """
    冒泡排序
    """
    for i in range(len(ls) - 1):
        for j in range(len(ls) - i - 1):
            if ls[j] > ls[j + 1]:
                ls[j], ls[j + 1] = ls[j + 1], ls[j]
    return ls


def on_request(ch, method, props, body):
    ls = json.loads(body)

    print("客户端请求参数 ls:{0}".format(ls))

    if isinstance(ls, list):
        response = bubble_sort(ls)
    else:
        response = '客户端请求参数类型不对 type:{0}'.format(type(ls))
    print("服务端计算结果 response:{0}".format(response))

    # 服务端发送消息的属性设置
    properties = pika.BasicProperties(delivery_mode=2,
                                      correlation_id=props.correlation_id)

    # 服务端发送计算后的结果, routing_key为客户端传来的reply_to
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=properties,
                     body=json.dumps(response))

    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    username = 'sanford'
    password = '123456'
    host = 'localhost'
    port = 5672
    virtual_host = 'sanford_host'

    credentials = pika.PlainCredentials(username=username, password=password)
    params = pika.ConnectionParameters(host=host,
                                       port=port,
                                       virtual_host=virtual_host,
                                       credentials=credentials)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='rpc_queue', durable=True)

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

    print("正在等待客户端请求......")
    channel.start_consuming()
