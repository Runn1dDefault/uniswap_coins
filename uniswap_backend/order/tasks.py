from uniswap_backend.celery import app


@app.task
def celery_test():
    x = 0
    while True:
        print('++++++++++')
        x += 1
        print(x)
        if x == 1100:
            break