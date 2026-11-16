import pandas as pd
import matplotlib.pyplot as plt
import os

LAB_DIR = r"C:\Users\user\Desktop\ParallelProgramming\labs\lab2"
PIC_DIR = os.path.join(LAB_DIR, "pic")
CSV_FILE = os.path.join(LAB_DIR, "results.csv")

if not os.path.exists(PIC_DIR):
    os.makedirs(PIC_DIR)

if not os.path.exists(CSV_FILE):
    print(f"Ошибка: файл {CSV_FILE} не найден. Сначала запусти run_experiments.py!")
    exit(1)

df = pd.read_csv(CSV_FILE)

plt.figure(figsize=(10, 6))
df_seq_cache = df[(df['Threads'] == 1) & (df['Algo'] == 'cache')]
df_seq_naive = df[(df['Threads'] == 1) & (df['Algo'] == 'naive')]

plt.plot(df_seq_cache['Size'], df_seq_cache['Time'], marker='o', markersize=8, color='blue', label='Оптимизированный (i-k-j)')
plt.plot(df_seq_naive['Size'], df_seq_naive['Time'], marker='s', markersize=8, color='orange', label='Наивный (i-j-k)')

plt.title('Влияние работы с памятью на время (1 поток)')
plt.xlabel('Размер матрицы N')
plt.ylabel('Время выполнения (сек)')
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(PIC_DIR, 'memory_comparison.png'))

target_size = 800
if target_size in df['Size'].values:
    df_fixed = df[df['Size'] == target_size]
else:
    target_size = df['Size'].max()
    df_fixed = df[df['Size'] == target_size]

plt.figure(figsize=(10, 6))
for algo, color, marker in [('naive', 'orange', 's'), ('cache', 'blue', 'o')]:
    df_algo = df_fixed[df_fixed['Algo'] == algo].sort_values('Threads')
    plt.plot(df_algo['Threads'], df_algo['Time'], marker=marker, markersize=8, color=color, label=f'Алгоритм: {algo}')

plt.title(f'Время от количества потоков (N={target_size})')
plt.xlabel('Количество потоков')
plt.ylabel('Время (сек)')
plt.grid(True)
plt.xticks(df_fixed['Threads'].unique())
plt.legend()
plt.savefig(os.path.join(PIC_DIR, 'time_vs_threads.png'))

plt.figure(figsize=(10, 6))
for algo, color, marker in [('naive', 'orange', 's'), ('cache', 'blue', 'o')]:
    df_algo = df_fixed[df_fixed['Algo'] == algo].sort_values('Threads')
    base_time = df_algo['Time'].iloc[0]
    speedup = base_time / df_algo['Time']
    plt.plot(df_algo['Threads'], speedup, marker=marker, markersize=8, color=color, label=f'Ускорение ({algo})')

plt.plot(df_fixed['Threads'].unique(), df_fixed['Threads'].unique(), '--', color='gray', label='Идеальное ускорение')
plt.title(f'Ускорение от количества потоков (N={target_size})')
plt.xlabel('Количество потоков')
plt.ylabel('Ускорение (раз)')
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(PIC_DIR, 'speedup_comparison.png'))

plt.figure(figsize=(10, 6))
for algo, color, marker in [('naive', 'orange', 's'), ('cache', 'blue', 'o')]:
    df_algo = df_fixed[df_fixed['Algo'] == algo].sort_values('Threads')
    base_time = df_algo['Time'].iloc[0]
    speedup = base_time / df_algo['Time']
    efficiency = (speedup / df_algo['Threads']) * 100
    plt.plot(df_algo['Threads'], efficiency, marker=marker, markersize=8, color=color, label=f'Эффективность ({algo})')

plt.axhline(y=100, color='gray', linestyle='--', label='Идеал (100%)')
plt.title(f'Эффективность распараллеливания (N={target_size})')
plt.xlabel('Количество потоков')
plt.ylabel('Эффективность (%)')
plt.grid(True)
plt.legend()
plt.savefig(os.path.join(PIC_DIR, 'efficiency_comparison.png'))

print("Все графики успешно сохранены в папку pic!")