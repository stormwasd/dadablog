from celery import Celery

# 初始化
app = Celery("gxn", broker='redis://:@127.0.0.1:6379/2')

# 定义具体的执行函数
@app.task
def task_test():
	print('task is running...')
