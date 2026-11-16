#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>
#include <iomanip>
#include <random>
#include <windows.h>
#include <omp.h>

using namespace std;
using namespace std::chrono;

vector<vector<double>> readMatrix(const string& filename, int& N) {
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Ошибка: не удалось открыть файл " << filename << endl;
        exit(1);
    }
    file >> N;
    vector<vector<double>> matrix(N, vector<double>(N));
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j)
            file >> matrix[i][j];
    file.close();
    return matrix;
}

void writeMatrix(const string& filename, const vector<vector<double>>& matrix) {
    ofstream file(filename);
    if (!file.is_open()) {
        cerr << "Ошибка: не удалось создать файл " << filename << endl;
        exit(1);
    }
    int N = matrix.size();
    file << N << "\n";
    file << fixed << setprecision(4);
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j)
            file << matrix[i][j] << " ";
        file << "\n";
    }
    file.close();
}

void generateRandomMatrix(const string& filename, int N) {
    ofstream file(filename);
    if (!file.is_open()) {
        cerr << "Ошибка: не удалось создать файл " << filename << endl;
        exit(1);
    }
    file << N << "\n";
    random_device rd;
    mt19937 gen(rd());
    uniform_real_distribution<> dis(1.0, 10.0);

    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            file << dis(gen) << " ";
        }
        file << "\n";
    }
    file.close();
    cout << "Сгенерирована матрица " << N << "x" << N << " -> " << filename << endl;
}

vector<vector<double>> multiplyMatrices(const vector<vector<double>>& A, const vector<vector<double>>& B) {
    int N = A.size();
    vector<vector<double>> C(N, vector<double>(N, 0.0));

#pragma omp parallel for
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            double sum = 0.0;
            for (int k = 0; k < N; ++k)
                sum += A[i][k] * B[k][j];
            C[i][j] = sum;
        }
    }
    return C;
}

int main(int argc, char* argv[]) {
    SetConsoleOutputCP(CP_UTF8);
    if (argc == 5 && string(argv[1]) == "--gen") {
        int N = stoi(argv[2]);
        generateRandomMatrix(argv[3], N);
        generateRandomMatrix(argv[4], N);
        return 0;
    }


    if (argc < 4) {
        cerr << "Использование:" << endl;
        cerr << "  " << argv[0] << " <file_A> <file_B> <file_result>" << endl;
        cerr << "  " << argv[0] << " --gen <N> <file_A> <file_B>" << endl;
        return 1;
    }

    string fileA = argv[1];
    string fileB = argv[2];
    string fileRes = argv[3];

    cout << "Потоков: " << omp_get_max_threads() << endl;

    int N = 0;
    cout << "Чтение матриц..." << endl;
    vector<vector<double>> A = readMatrix(fileA, N);
    int N_B = 0;
    vector<vector<double>> B = readMatrix(fileB, N_B);

    if (N != N_B) {
        cerr << "Ошибка: Размеры матриц не совпадают!" << endl;
        return 1;
    }

    cout << "Размер задачи (N): " << N << endl;
    cout << "Начало вычислений..." << endl;

    auto start = high_resolution_clock::now();
    vector<vector<double>> C = multiplyMatrices(A, B);
    auto end = high_resolution_clock::now();
    duration<double> duration = end - start;

    cout << "Время выполнения: " << duration.count() << " сек." << endl;

    writeMatrix(fileRes, C);
    cout << "Результат сохранен в " << fileRes << endl;

    return 0;
}