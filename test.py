import time
from concurrent.futures import ThreadPoolExecutor


def write(num):
    while 1:
        print(num)
        time.sleep(1)


if __name__ == "__main__":
    write_pool = ThreadPoolExecutor(max_workers=5)
    write_pool.submit(write, 1)
    print(123)

    # while 1:
    #     print(time.time())
    #     time.sleep(0.01)
