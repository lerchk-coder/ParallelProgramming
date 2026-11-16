#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <iomanip>
#include <random>
#include <omp.h>
#include <windows.h>

using namespace std;

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
}

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

vector<vector<double>> multiplyMatrices(const vector<vector<double>>& A, const vector<vector<double>>& B, const string& algo) {
    int N = A.size();
    vector<vector<double>> C(N, vector<double>(N, 0.0));

    if (algo == "naive") {
#pragma omp parallel for
        for (int i = 0; i < N; ++i) {
            for (int j = 0; j < N; ++j) {
                for (int k = 0; k < N; ++k) {
                    C[i][j] += A[i][k] * B[k][j];
                }
            }
        }
    }
    else if (algo == "cache") {
#pragma omp parallel for
        for (int i = 0; i < N; ++i) {
            for (int k = 0; k < N; ++k) {
                double a_ik = A[i][k];
                for (int j = 0; j < N; ++j) {
                    C[i][j] += a_ik * B[k][j];
                }
            }
        }
    }
    return C;
}

int main(int argc, char* argv[]) {
    SetConsoleCP(65001);
    SetConsoleOutputCP(65001);

    if (argc == 5 && string(argv[1]) == "--gen") {
        int N = stoi(argv[2]);
        generateRandomMatrix(argv[3], N);
        generateRandomMatrix(argv[4], N);
        return 0;
    }

    if (argc < 6) {
        cerr << "Использование: " << argv[0] << " <file_A> <file_B> <file_result> <threads> <algo>" << endl;
        cerr << "Или для генерации: " << argv[0] << " --gen <N> <file_A> <file_B>" << endl;
        return 1;
    }

    string fileA = argv[1];
    string fileB = argv[2];
    string fileRes = argv[3];
    int num_threads = stoi(argv[4]);
    string algo = argv[5];

    omp_set_num_threads(num_threads);

    int N = 0;
    vector<vector<double>> A = readMatrix(fileA, N);
    int N_B = 0;
    vector<vector<double>> B = readMatrix(fileB, N_B);

    if (N != N_B) {
        cerr << "Ошибка: Размеры матриц не совпадают!" << endl;
        return 1;
    }

    double start_time = omp_get_wtime();
    vector<vector<double>> C = multiplyMatrices(A, B, algo);
    double end_time = omp_get_wtime();

    double duration = end_time - start_time;

    cout << "N=" << N << "; Threads=" << num_threads << "; Algo=" << algo << "; Time=" << duration << endl;

    return 0;
}