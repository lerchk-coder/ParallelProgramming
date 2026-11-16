import numpy as np
import sys
import os

def read_matrix(filename):
    if not os.path.exists(filename):
        print(f"Файл {filename} не найден.")
        sys.exit(1)
    with open(filename, 'r') as f:
        lines = f.readlines()
        n = int(lines[0].strip())
        matrix = []
        for i in range(1, n + 1):
            row = list(map(float, lines[i].strip().split()))
            matrix.append(row)
    return np.array(matrix)

def verify(file_a, file_b, file_res):
    print(f"Чтение матрицы A: {file_a}")
    A = read_matrix(file_a)
    
    print(f"Чтение матрицы B: {file_b}")
    B = read_matrix(file_b)
    
    print(f"Чтение результата C++ (CUDA): {file_res}")
    C_cpp = read_matrix(file_res)
    
    print("Вычисление эталона через NumPy...")
    C_python = np.dot(A, B)
    
    diff = np.abs(C_cpp - C_python)
    max_diff = np.max(diff)
    mean_diff = np.mean(diff)
    
    print("\n--- РЕЗУЛЬТАТЫ ПРОВЕРКИ ---")
    print(f"Максимальная абсолютная разница: {max_diff:.6e}")
    print(f"Средняя абсолютная разница:      {mean_diff:.6e}")
    
    if np.allclose(C_cpp, C_python, rtol=1e-5, atol=1e-5):
        print("✅ УСПЕХ: Результаты CUDA полностью совпадают с эталоном NumPy.")
    else:
        print("❌ ОШИБКА: Результаты не совпадают!")
        print("Возможные причины: ошибки индексации в CUDA-ядре, переполнение, или ошибки чтения/записи.")
        
        idx = np.unravel_index(np.argmax(diff), diff.shape)
        print(f"Худший элемент: строка {idx[0]}, столбец {idx[1]}")
        print(f"  C++:   {C_cpp[idx[0], idx[1]]}")
        print(f"  NumPy: {C_python[idx[0], idx[1]]}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python verify_cuda.py <file_A> <file_B> <file_result>")
        sys.exit(1)
    
    verify(sys.argv[1], sys.argv[2], sys.argv[3])