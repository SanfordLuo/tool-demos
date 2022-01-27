from celery_app import app


@app.task
def add(x, y):
    return x + y


@app.task
def cheng(x, y):
    return x * y


@app.task
def timing(*args):
    return args
