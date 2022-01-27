from celery.schedules import crontab
from kombu import Exchange, Queue

# 指定broker, 这里使用rabbitmq: 'amqp://username:password@host:port/virtual_host'
broker_url = 'amqp://sanford:123456@localhost:5672/sanford_host'

# 指定backend, 这里使用redis: 'redis://host:port/db'
result_backend = 'redis://localhost:6379/0'

# 指定任务序列化方式 json, msgpack
task_serializer = 'json'

# 指定结果序列化方式 json, msgpack
result_serializer = 'json'

# 任务过期时间 秒
result_expires = 60 * 60 * 24

# 指定任务接受的序列化类型.
accept_content = ['json', 'msgpack']

# 时区
timezone = 'Asia/Shanghai'

# 导入任务
imports = (
    'celery_app.tasks'
)

# 定时任务 celery_app.tasks.timing
beat_schedule = {
    'test_timing': {
        'task': 'celery_app.tasks.timing',
        'schedule': crontab(minute='*/1'),
        'args': ('jay', 'chou')  # 对应任务的入参
    }
}

# 设置队列, 这里设置了两个队列 timing_queue用于处理定时任务, default用于处理其他
task_queues = (
    Queue('default', exchange=Exchange(name='default', type='direct'), routing_key='default'),
    Queue('timing_queue', exchange=Exchange(name='timing_exchange', type='direct'), routing_key='routing.timing'),
)

# 设置任务对应的路由 celery_app.tasks.timing
task_routes = {
    'celery_app.tasks.timing': {
        'queue': 'timing_queue',
        'routing_key': 'routing.timing',
    },
    '*': {
        'queue': 'default',
        'routing_key': 'default'
    },
}

# 指定默认的队列, 如果一个消息设置的路由不符合, 则会进入这个队列
task_default_queue = 'default'
