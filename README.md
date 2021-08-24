### 目录说明
```
.
├── README.md
├── img    // 测试图片目录
│   ├── img_000.jpg
│   ├── img_001.jpg
│   └── img_002.jpg
├── requirements.txt
├── script    // 脚本目录
│   ├── 000_get_ryg.py    // 图片降维处理,获取RYG值
│   ├── 001_get_word_path.py    // 查找关键字并返回所在文件
│   ├── 002_hsv_color.py    // 
│   ├── 003_img_black_white.py    // 判断图片是否为全黑或者全白
│   ├── 004_img_computer.py    // 判断待测图片是否和模版图片相似
│   ├── 005_log_demo.py    // log模版
│   ├── 006_make_model.py    // 根据像素点获取图片中的数字模板
│   ├── 007_singleton.py    // 单例
│   ├── 008_test_futures.py    // ProcessPoolExecutor进程池模版
│   ├── 009_kafka_producer.py    // kafka生产者
│   ├── 010_kafka_consumer.py    // kafka消费者
│   └── __init__.py
├── test    // 测试文件目录
│   ├── test
│   │   └── test_get_word_path.py
│   ├── test_get_word_path.py
│   └── test_get_word_path.txt
└── tree.txt    // 项目结构 tree > tree.txt 
```
