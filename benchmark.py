import math
import time
from concurrent.futures import ProcessPoolExecutor

# Вычислительно емкая функция (проверка простых чисел)
def count_primes(n):
    count = 0
    for i in range(2, n):
        is_prime = True
        for j in range(2, int(math.isqrt(i)) + 1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            count += 1
    return count

def run_workload(num_threads):
    limit = 1_500_000
    chunk = limit // num_threads
    tasks = [chunk] * num_threads
    
    with ProcessPoolExecutor(max_workers=num_threads) as executor:
        list(executor.map(count_primes, tasks))

if __name__ == "__main__":
    thread_counts = [1, 2, 4, 8, 16, 32]
    print("Language & Runtime: Python multiprocessing\n")
    print(f"{'Threads (N)':<12} | {'Run 1 (s)':<10} | {'Run 2 (s)':<10} | {'Run 3 (s)':<10} | {'Avg (s)':<10} | {'Speedup':<10} | {'Efficiency':<10}")
    print("-" * 85)
    
    t1_avg = 0.0
    for t in thread_counts:
        runs = []
        for _ in range(3):
            start = time.perf_counter()
            run_workload(t)
            end = time.perf_counter()
            runs.append(end - start)
            
        avg = sum(runs) / 3.0
        if t == 1:
            t1_avg = avg
            
        speedup = t1_avg / avg if avg > 0 else 0
        efficiency = (speedup / t) * 100.0
        
        print(f"N={t:<10} | {runs[0]:<10.3f} | {runs[1]:<10.3f} | {runs[2]:<10.3f} | {avg:<10.3f} | {speedup:<9.2f}x | {efficiency:<9.1f}%")