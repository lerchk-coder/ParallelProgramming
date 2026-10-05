import matplotlib.pyplot as plt

threads = [1, 2, 4, 8]
time_omp = [4.07453, 2.12493, 1.71671, 1.72752]


speedup = [time_omp[0] / t for t in time_omp]
efficiency = [s / th * 100 for s, th in zip(speedup, threads)]

plt.figure(figsize=(10, 6))
plt.plot(threads, time_omp, 'o-', color='green', markersize=10, linewidth=2)
plt.xlabel('Количество потоков')
plt.ylabel('Время выполнения (сек)')
plt.title('Зависимость времени от количества потоков (N=500)')
plt.grid(True)
plt.xticks(threads)
plt.savefig('../lab1/pic/measurements_omp_time.png', dpi=150)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(threads, speedup, 'o-', color='red', label='Реальное ускорение', markersize=10, linewidth=2)
plt.plot(threads, threads, '--', color='gray', label='Идеальное ускорение')
plt.xlabel('Количество потоков')
plt.ylabel('Ускорение (раз)')
plt.title('Ускорение от количества потоков (N=500)')
plt.grid(True)
plt.xticks(threads)
plt.legend()
plt.savefig('../lab1/pic/measurements_omp_speedup.png', dpi=150)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(threads, efficiency, 'o-', color='blue', markersize=10, linewidth=2)
plt.axhline(y=100, color='gray', linestyle='--', label='Идеальная эффективность (100%)')
plt.xlabel('Количество потоков')
plt.ylabel('Эффективность (%)')
plt.title('Эффективность распараллеливания (N=500)')
plt.grid(True)
plt.xticks(threads)
plt.legend()
plt.savefig('../lab1/pic/measurements_omp_efficiency.png', dpi=150)
plt.show()

print("Графики сохранены в ../pic/")
print("\nТаблица результатов:")
print(f"{'Потоки':<8}{'Время (с)':<12}{'Ускорение':<12}{'Эффективность':<15}")
for th, t, s, e in zip(threads, time_omp, speedup, efficiency):
    print(f"{th:<8}{t:<12.5f}{s:<12.2f}{e:<15.1f}")