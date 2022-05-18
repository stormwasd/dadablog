from celery import Celery

# 初始化
app = Celery("gxn_result", broker='redis://:@127.0.0.1:6379/2', backend='redis://:@127.0.0.1:6379/3')

# 定义具体的执行函数
@app.task
def task_test(a, b):
	print('task is running...')
	return a + b
