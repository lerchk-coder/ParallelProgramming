import matplotlib.pyplot as plt
import os

block_sizes = [8, 16, 32]
time_gpu = [0.065, 0.048, 0.052]

os.makedirs('../lab4/pic', exist_ok=True)

plt.figure(figsize=(10, 6))
plt.plot(block_sizes, time_gpu, 'o-', color='purple', markersize=10, linewidth=2)

plt.xlabel('Размер блока (NxN)')
plt.ylabel('Время выполнения (сек)')
plt.title('Влияние конфигурации сетки блоков на время (N=1024)')
plt.grid(True)
plt.xticks(block_sizes)
plt.savefig('../lab4/pic/cuda_block_size.png', dpi=150)
plt.show()
print("График сохранён в ../lab4/pic/cuda_block_size.png")