import numpy as np
import sys
import os

def load_matrix(filename):
    if not os.path.exists(filename):
        print(f"File {filename} not found!")
        return None
    
    with open(filename, 'r') as f:
        n = int(f.readline().strip())
        matrix = []
        for line in f:
            if line.strip():
                row = [float(x) for x in line.split()]
                matrix.append(row)
    
    return np.array(matrix)

def main():
    A = load_matrix('data/matrixA.txt')
    B = load_matrix('data/matrixB.txt')
    C_cpp = load_matrix('data/matrixC.txt')
    
    if A is None or B is None or C_cpp is None:
        print("FAILED")
        return 1
    
    C_correct = np.dot(A, B)
    
    if np.allclose(C_cpp, C_correct, rtol=1e-5, atol=1e-8):
        print("PASSED")
        return 0
    else:
        print("FAILED")
        diff = np.abs(C_cpp - C_correct)
        print(f"Max error: {np.max(diff)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
