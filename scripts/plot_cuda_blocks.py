import matplotlib.pyplot as plt
import numpy as np
import os

N = [256, 512, 1024, 2048]
time_cpu = [0.8, 6.2, 53.6, 420.0]
time_gpu = [0.002, 0.01, 0.05, 0.3]

os.makedirs('../lab4/pic', exist_ok=True)

plt.figure(figsize=(10, 6))
plt.plot(N, time_cpu, 'o-', color='red', label='CPU (Sequential)', markersize=8)
plt.plot(N, time_gpu, 's-', color='blue', label='GPU (CUDA)', markersize=8)

plt.xlabel('Размер матрицы N')
plt.ylabel('Время выполнения (сек)')
plt.title('Сравнение времени выполнения: CPU vs GPU')
plt.yscale('log')
plt.grid(True, which="both", ls="--")
plt.legend()
plt.savefig('../lab4/pic/cuda_vs_cpu_time.png', dpi=150)
plt.show()
print("График сохранён в ../lab4/pic/cuda_vs_cpu_time.png")