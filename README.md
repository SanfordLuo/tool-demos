### 目录说明
```
.
├── README.md
├── celery_app  // celery应用
│   ├── __init__.py
│   ├── config.py
│   └── tasks.py
├── img    // 测试图片目录
├── log    // 日志存放目录
├── requirements.txt
├── script    // 脚本目录
│   ├── __init__.py
│   ├── celery_run.py  // celery任务测试脚本
│   ├── get_ryg.py    // 图片降维处理,获取RYG值
│   ├── get_word_path.py    // 查找关键字并返回所在文件
│   ├── hsv_color.py    // hsv区分颜色应用
│   ├── kafka_consumer.py    // kafka消费者
│   ├── kafka_producer.py    // kafka生产者
│   ├── log_handler.py    // 日志处理器
│   ├── pressure_by_threading.py    // 接口压力测试
│   ├── rabbitmq_consumer.py    // rabbitmq消费者
│   ├── rabbitmq_publisher.py    // rabbitmq生产者
│   ├── rabbitmq_rpc_client.py    // rabbitmq rpc 客户端
│   ├── rabbitmq_rpc_service.py    // rabbitmq rpc 服务端
│   ├── singleton.py    // 单例
│   ├── thread_process.py    // 线程池 进程池
│   └── zixing.py    // 自省函数
├── test    // 测试文件目录
└── tree.txt    // 项目结构 tree > tree.txt 
```
