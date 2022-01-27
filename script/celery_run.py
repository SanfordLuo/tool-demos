from celery_app.tasks import add, cheng


def run():
    ret = add.delay(2, 3)
    result, status, task_id = None, None, None

    # 获取任务结果
    # result = ret.get()
    # status = ret.status
    # task_id = ret.task_id

    return result, status, task_id


if __name__ == '__main__':
    _ret = run()
    print(_ret)
