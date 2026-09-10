import threading
import time

counter = 0

def increment():
    global counter
    for _ in range(1_000_000):
        counter += 1

def run_race():
    global counter
    counter = 0
    threads = [threading.Thread(target=increment) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    return counter

print("--- TASK 3: Race Condition Runs ---")
for i in range(1, 11):
    val = run_race()
    err = 10_000_000 - val
    print(f"Run #{i}: Measured = {val}, Error = {err}")

# Lock test
lock = threading.Lock()
locked_counter = 0

def increment_locked():
    global locked_counter
    for _ in range(1_000_000):
        with lock:
            locked_counter += 1

start = time.perf_counter()
run_race()
unlocked_time = (time.perf_counter() - start) * 1000

start = time.perf_counter()
threads = [threading.Thread(target=increment_locked) for _ in range(10)]
for t in threads: t.start()
for t in threads: t.join()
locked_time = (time.perf_counter() - start) * 1000

print(f"\nUnlocked Time: {unlocked_time:.2f} ms")
print(f"Locked Time: {locked_time:.2f} ms")