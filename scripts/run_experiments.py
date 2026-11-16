import subprocess
import os
import csv
import re

LAB_DIR = r"C:\Users\user\Desktop\ParallelProgramming\labs\lab2"
EXECUTABLE = r"C:\Users\user\Desktop\ParallelProgramming\labs\lab2\out\build\x64-Debug\matrix_app.exe"

SIZES = [200, 400, 800, 1200, 1600, 2000]
THREADS = [1, 2, 4, 8]
ALGOS = ["naive", "cache"]

def generate_matrix(n, filename):
    if not os.path.exists(filename):
        print(f"Генерация матрицы {n}x{n}...")
        subprocess.run([EXECUTABLE, "--gen", str(n), filename, filename], check=True)

def run_test(fileA, fileB, threads, algo):
    result = subprocess.run([EXECUTABLE, fileA, fileB, os.path.join(LAB_DIR, "result.txt"), str(threads), algo], 
                            capture_output=True, text=True, check=True)
    
    match = re.search(r"Time=([0-9.]+)", result.stdout)
    if match:
        return float(match.group(1))
    return None

def main():
    data_dir = os.path.join(LAB_DIR, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    results = []

    print("Начинаем эксперименты...")
    for n in SIZES:
        fileA = os.path.join(data_dir, f"A_{n}.txt")
        fileB = os.path.join(data_dir, f"B_{n}.txt")
        
        generate_matrix(n, fileA)
        generate_matrix(n, fileB)

        for algo in ALGOS:
            print(f"\n--- Размер: {n}x{n} | Алгоритм: {algo} ---")
            for t in THREADS:
                print(f"  Потоков: {t}...", end=" ", flush=True)
                try:
                    exec_time = run_test(fileA, fileB, t, algo)
                    if exec_time is not None:
                        print(f"{exec_time:.4f} сек.")
                        results.append({
                            "Size": n,
                            "Threads": t,
                            "Algo": algo,
                            "Time": exec_time
                        })
                    else:
                        print("Ошибка парсинга!")
                except Exception as e:
                    print(f"Ошибка запуска: {e}")

    csv_file = os.path.join(LAB_DIR, "results.csv")
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Size", "Threads", "Algo", "Time"])
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\nВсе данные сохранены в {csv_file}")

if __name__ == "__main__":
    main()