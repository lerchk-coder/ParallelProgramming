import matplotlib.pyplot as plt
import numpy as np
import os

N = [100, 200, 300, 500, 1000]
time = [0.0541271, 0.391575, 1.34515, 6.26874, 53.6745]

os.makedirs('../pic', exist_ok=True)

plt.figure(figsize=(10, 6))
plt.plot(N, time, 'o-', color='blue', label='Измерения', markersize=8)

N_theory = np.linspace(100, 1000, 100)
time_theory = time[0] * (N_theory / N[0])**3
plt.plot(N_theory, time_theory, '--', color='red', label='O(N³) теоретически')

plt.xlabel('Размер матрицы N')
plt.ylabel('Время выполнения (сек)')
plt.title('Зависимость времени от размера задачи (последовательная версия)')
plt.grid(True)
plt.legend()
plt.savefig('../pic/measurements_seq.png', dpi=150)
plt.show()
print("График сохранён в ../pic/measurements_seq.png")