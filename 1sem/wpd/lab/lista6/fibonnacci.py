import time
import tracemalloc
import matplotlib.pyplot as plt


def fibonnacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonnacci(n - 1) + fibonnacci(n - 2)


def fibonnaci_with_memory(n, memory=None):
    if memory is None:
        memory = {}

    if n in memory:
        return memory[n]

    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        memory[n] = (
            fibonnaci_with_memory(n - 1, memory)
            + fibonnaci_with_memory(n - 2, memory)
        )
        return memory[n]


def fibonacci_bottom_up(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1

    dp = [0] * (n + 1)
    dp[1] = 1

    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]


def measure(func, n):
    tracemalloc.start()

    start = time.perf_counter()
    result = func(n)
    end = time.perf_counter()

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    execution_time = end - start
    memory_used = peak / 1024

    return (result, execution_time, memory_used)


n_values = [1, 2, 5, 35, 100]

functions = {
    # "Rekurencyjnie": fibonnacci,
    "Memoizacja": fibonnaci_with_memory,
    "Bottom-up": fibonacci_bottom_up,
}

times_data = {}
memory_data = {}

for name, func in functions.items():
    times = []
    memories = []

    print(f"\n{name}")

    for n in n_values:
        result, exec_time, memory = measure(func, n)

        print(
            f"n={n:<2} | wynik={result:<8} | "
            f"czas={exec_time:.6f}s | pamięć={memory:.2f}KB"
        )

        times.append(exec_time)
        memories.append(memory)

    times_data[name] = times
    memory_data[name] = memories


plt.figure(figsize=(10, 6))

for name, times in times_data.items():
    plt.plot(n_values, times, marker='o', label=name)

plt.title("Porównanie czasu wykonania")
plt.xlabel("n")
plt.ylabel("Czas [s]")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 6))

for name, memories in memory_data.items():
    plt.plot(n_values, memories, marker='o', label=name)

plt.title("Porównanie zużycia pamięci")
plt.xlabel("n")
plt.ylabel("Pamięć [KB]")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()