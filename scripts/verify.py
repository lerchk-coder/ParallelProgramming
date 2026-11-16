import numpy as np
import sys
import os

def read_matrix(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        n = int(lines[0].strip())
        matrix = []
        for i in range(1, n + 1):
            row = list(map(float, lines[i].strip().split()))
            matrix.append(row)
    return np.array(matrix)

def verify(file_a, file_b, file_res):
    if not os.path.exists(file_res):
        print(f"❌ Файл {file_res} не найден.")
        return False
    print("Чтение файлов...")
    A = read_matrix(file_a)
    B = read_matrix(file_b)
    C_cpp = read_matrix(file_res)
    print("Вычисление эталона через NumPy...")
    C_python = np.dot(A, B)
    if np.allclose(C_cpp, C_python, rtol=1e-4, atol=1e-4):
        print("✅ УСПЕХ: Результаты совпадают!")
        return True
    else:
        print("❌ ОШИБКА: Результаты не совпадают!")
        print(f"Макс. расхождение: {np.max(np.abs(C_cpp - C_python))}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python verify.py <file_A> <file_B> <file_result>")
        sys.exit(1)
    verify(sys.argv[1], sys.argv[2], sys.argv[3])