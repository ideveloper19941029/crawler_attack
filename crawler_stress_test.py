import requests
import threading

success_count = 0
fail_count = 0
lock = threading.Lock()  # Counter lock under multithreading

def crawler_access(url, timeout):
    global success_count, fail_count
    try:
        res = requests.get(url, timeout=timeout)
        with lock:
            if res.status_code == 200:
                success_count += 1
                print(f"[OK] Request successful: Status code {res.status_code}")
            else:
                fail_count += 1
                print(f"[E] The request returns an abnormal status code: {res.status_code}")
    except Exception as e:
        with lock:
            fail_count += 1
            print(f"[E] Request failed: {e}")

def attack(url, times, timeout=1000):

    # Starting a Thread
    threads = []
    for i in range(times):
        t = threading.Thread(target=crawler_access, args=(url, timeout))
        t.start()
        threads.append(t)

    # Wait for all threads to complete
    for t in threads:
        t.join()

    # Print statistics results
    print("\n* Stress test results:")
    print(f"[OK] Total successful requests: {success_count}")
    print(f"[E] Total failed requests: {fail_count}")


attack("https://musicalmoon.com/", 10)
