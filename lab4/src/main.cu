#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <string>
#include <iomanip>
#include <random>
#include <cmath>
#include <clocale>
#include <cuda_runtime.h>

using namespace std;
using namespace std::chrono;

inline void checkCuda(cudaError_t err, int line) {
    if (err != cudaSuccess) {
        std::cerr << "CUDA Error: " << cudaGetErrorString(err) << " at line " << line << std::endl;
        exit(1);
    }
}
#define CUDA_CHECK(call) checkCuda(call, __LINE__)

static double* readFlatMatrix(const string& filename, int& N) {
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Ошибка: не удалось открыть файл " << filename << endl;
        exit(1);
    }
    file >> N;
    double* matrix = new double[(size_t)N * N];
    for (int i = 0; i < N; ++i)
        for (int j = 0; j < N; ++j)
            file >> matrix[(size_t)i * N + j];
    file.close();
    return matrix;
}

static void writeFlatMatrix(const string& filename, const double* matrix, int N) {
    ofstream file(filename);
    if (!file.is_open()) {
        cerr << "Ошибка: не удалось создать файл " << filename << endl;
        exit(1);
    }
    file << N << "\n";
    file << fixed << setprecision(4);
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j)
            file << matrix[(size_t)i * N + j] << " ";
        file << "\n";
    }
    file.close();
}

static void generateRandomMatrix(const string& filename, int N) {
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

__global__ void matrixMultiplyKernel(const double* A, const double* B, double* C, int N) {
    int row = blockIdx.y * blockDim.y + threadIdx.y;
    int col = blockIdx.x * blockDim.x + threadIdx.x;

    if (row < N && col < N) {
        double sum = 0.0;
        for (int k = 0; k < N; ++k) {
            sum += A[(size_t)row * N + k] * B[(size_t)k * N + col];
        }
        C[(size_t)row * N + col] = sum;
    }
}

int main(int argc, char* argv[]) {
    setlocale(LC_ALL, "Russian");

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

    int N = 0, N_B = 0;
    cout << "Чтение матриц..." << endl;
    double* h_A = readFlatMatrix(fileA, N);
    double* h_B = readFlatMatrix(fileB, N_B);

    if (N != N_B) {
        cerr << "Ошибка: Размеры матриц не совпадают!" << endl;
        return 1;
    }

    cout << "Размер задачи (N): " << N << endl;

    double* d_A, * d_B, * d_C;
    size_t bytes = (size_t)N * N * sizeof(double);

    CUDA_CHECK(cudaMalloc(&d_A, bytes));
    CUDA_CHECK(cudaMalloc(&d_B, bytes));
    CUDA_CHECK(cudaMalloc(&d_C, bytes));

    CUDA_CHECK(cudaMemcpy(d_A, h_A, bytes, cudaMemcpyHostToDevice));
    CUDA_CHECK(cudaMemcpy(d_B, h_B, bytes, cudaMemcpyHostToDevice));

    int BLOCK_SIZE = 16;
    dim3 block(BLOCK_SIZE, BLOCK_SIZE);
    dim3 grid((N + BLOCK_SIZE - 1) / BLOCK_SIZE, (N + BLOCK_SIZE - 1) / BLOCK_SIZE);

    cout << "Запуск CUDA ядра (Grid: " << grid.x << "x" << grid.y
        << ", Block: " << block.x << "x" << block.y << ")..." << endl;

    cudaEvent_t start, stop;
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));
    CUDA_CHECK(cudaEventRecord(start));

    matrixMultiplyKernel << <grid, block >> > (d_A, d_B, d_C, N);

    cudaError_t err = cudaGetLastError();
    if (err != cudaSuccess) {
        std::cerr << "Ошибка запуска ядра: " << cudaGetErrorString(err) << std::endl;
        return 1;
    }

    err = cudaDeviceSynchronize();
    if (err != cudaSuccess) {
        std::cerr << "Ошибка выполнения ядра: " << cudaGetErrorString(err) << std::endl;
        return 1;
    }

    CUDA_CHECK(cudaEventRecord(stop));
    CUDA_CHECK(cudaEventSynchronize(stop));

    float milliseconds = 0;
    CUDA_CHECK(cudaEventElapsedTime(&milliseconds, start, stop));
    cout << "Время выполнения на GPU: " << milliseconds / 1000.0 << " сек." << endl;

    double* h_C = new double[(size_t)N * N];
    CUDA_CHECK(cudaMemcpy(h_C, d_C, bytes, cudaMemcpyDeviceToHost));
    cudaError_t err1 = cudaGetLastError();
    if (err1 != cudaSuccess) {
        cerr << "Ошибка после cudaMemcpy: " << cudaGetErrorString(err1) << endl;
    }

    cudaError_t err2 = cudaDeviceSynchronize();
    if (err2 != cudaSuccess) {
        cerr << "Ошибка после cudaDeviceSynchronize: " << cudaGetErrorString(err2) << endl;
    }

    writeFlatMatrix(fileRes, h_C, N);
    cout << "Результат сохранен в " << fileRes << endl;

    cudaFree(d_A);
    cudaFree(d_B);
    cudaFree(d_C);
    delete[] h_A;
    delete[] h_B;
    delete[] h_C;

    return 0;
}