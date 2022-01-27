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
from celery.backends.redis import RedisBackend
from datetime import datetime
from kombu.utils.encoding import ensure_bytes


class NewRedisBackend(RedisBackend):
    """
    继承Backend重写 _get_result_meta 用于修改 date_done 时区不一致问题
    """
    def _get_result_meta(self, result,
                         state, traceback, request, format_date=True,
                         encode=False):
        if state in self.READY_STATES:
            date_done = datetime.now()
            if format_date:
                date_done = date_done.isoformat()
        else:
            date_done = None

        meta = {
            'status': state,
            'result': result,
            'traceback': traceback,
            'children': self.current_task_children(request),
            'date_done': date_done,
        }

        if request and getattr(request, 'group', None):
            meta['group_id'] = request.group
        if request and getattr(request, 'parent_id', None):
            meta['parent_id'] = request.parent_id

        if self.app.conf.find_value_for_key('extended', 'result'):
            if request:
                request_meta = {
                    'name': getattr(request, 'task', None),
                    'args': getattr(request, 'args', None),
                    'kwargs': getattr(request, 'kwargs', None),
                    'worker': getattr(request, 'hostname', None),
                    'retries': getattr(request, 'retries', None),
                    'queue': request.delivery_info.get('routing_key')
                    if hasattr(request, 'delivery_info') and
                       request.delivery_info else None
                }

                if encode:
                    # args and kwargs need to be encoded properly before saving
                    encode_needed_fields = {"args", "kwargs"}
                    for field in encode_needed_fields:
                        value = request_meta[field]
                        encoded_value = self.encode(value)
                        request_meta[field] = ensure_bytes(encoded_value)

                meta.update(request_meta)

        return meta


app = Celery('celery_app', backend='celery_app.NewRedisBackend')
app.config_from_object('celery_app.config')
