"""
# 查看worker启动时的相关参数
celery worker --help

# 发布定时任务
celery -A celery_app beat

# 启动worker
# 指定4个进程数: -c 4
# windows系统加上: -P eventlet
# 指定要处理的队列消息,默认是全部队列: -Q queue_name
celery -A celery_app worker -l info -f "log/celery_app.log"

# 发布定时任务并且启动worker
celery -A celery_app worker -B --loglevel=info --logfile="log/celery_app.log"
"""
from celery import Celery

app = Celery('celery_app')
app.config_from_object('celery_app.config')
