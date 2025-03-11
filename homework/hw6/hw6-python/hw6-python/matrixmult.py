# This function takes 2 matricies (as lists of lists)
# and performs matrix multiplication on them.
# Note: you may not use any matrix multiplication libraries.
# You need to do the multiplication yourself.
# For example, if you have
#     a=[[1,2,3],
#        [4,5,6],
#        [7,8,9],
#        [4,0,7]]
#     b=[[1,2],
#        [3,4],
#        [5,6]]
#  Then a has 4 rows and 3 columns.
#  b has 3 rows and 2 columns.
#  Multiplying a * b results in a 4 row, 2 column matrix:
#  [[22, 28],
#   [49, 64],
#   [76, 100],
#   [39, 50]]

from datetime import datetime
import random
import time


# Function to generate a matrix with random integers
# szr: number of rows, szc: number of columns, num: max random integer
def generateMatrix(szr, szc, num):
    data = []
    for i in range(szr):
        data.append([])  # Append a new row
        for j in range(szc):
            data[i].append(random.randint(0, num))  # Fill row with random integers
    return data


# Function to print a list of integers, formatted with fixed width
def printInt(data):
    for i in data:
        print("%7d" % i, ",", sep="", end="")


# Function to print a list of floats, formatted to 5 decimal places
def printFloat(data):
    for i in data:
        print("%2.5f" % i, ",", sep="", end="")


# Function to perform matrix multiplication between matrices 'a' and 'b'
# Assumes len(a[0]) == len(b), so matrix multiplication is possible
def matrix_mul(a, b):
    assert (len(a[0]) == len(b))  # Ensure matrix dimensions are compatible
    # Initialize result matrix with zeros, dimensions: len(a) x len(b[0])
    res = [[0] * len(b[0]) for i in range(len(a))]
    # Perform matrix multiplication
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(a[0])):
                res[i][j] += a[i][k] * b[k][j]  # Accumulate product in res[i][j]
    return res


if __name__ == '__main__':
    # Initialize base matrix size
    size = 4
    size_rec = []
    cnt = 1
    while (cnt * size <= 512):
        size_rec.append(cnt * size)
        cnt *= 2
    printInt(size_rec)
    print()

    # Initialize lists to store timing data for each matrix size case
    data_many, data_square, data_few = [], [], []

    # Case 1: "Many" - Multiplying a wide matrix by a narrow one
    for sz in size_rec:
        arr_many = generateMatrix(4 * sz, sz, 10)  # Matrix with more rows than columns
        arr_many2 = generateMatrix(sz, sz // 4, 10)  # Matrix with fewer rows than columns
        start = time.perf_counter()
        ans = matrix_mul(arr_many, arr_many2)  # Multiply matrices
        end = time.perf_counter()
        data_many.append(end - start)  # Record time taken for multiplication
    printFloat(data_many)
    print()

    # Case 2: "Square" - Multiplying two square matrices of equal size
    for sz in size_rec:
        arr_moderate = generateMatrix(sz, sz, 10)  # First square matrix
        arr_moderate2 = generateMatrix(sz, sz, 10)  # Second square matrix
        start = time.perf_counter()
        ans = matrix_mul(arr_moderate, arr_moderate2)
        end = time.perf_counter()
        data_square.append(end - start)  # Record time taken for multiplication
    printFloat(data_square)
    print()

    # Case 3: "Few" - Multiplying a tall matrix by a wide one
    for sz in size_rec:
        arr_rare = generateMatrix(sz // 4, sz, 10)  # Matrix with fewer rows than columns
        arr_rare2 = generateMatrix(sz, sz * 4, 10)  # Matrix with more columns than rows
        start = time.perf_counter()
        ans = matrix_mul(arr_rare, arr_rare2)
        end = time.perf_counter()
        data_few.append(end - start)  # Record time taken for multiplication
    printFloat(data_few)
    print()

