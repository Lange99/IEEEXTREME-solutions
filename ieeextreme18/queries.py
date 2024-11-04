# Queries -> 33.33% of test cases passed.
# Time limit: 1500 ms
# Memory limit: 256 MB
#
# Given an array A of length N (initially all elements are 0) and a permutation P of the same length,
# the task involves processing Q queries/updates of different types:
#
# Update Types:
# - Type 0: Given l, r, c, add c to elements A[l], A[l+1], ..., A[r].
# - Type 1: Given l, r, c, add c to elements A[P[l]], A[P[l+1]], ..., A[P[r]].
#
# Query Types:
# - Type 2: Given l, r, calculate the sum A[l] + A[l+1] + ... + A[r].
# - Type 3: Given l, r, calculate the sum A[P[l]] + A[P[l+1]] + ... + A[P[r]].
#
# Standard Input:
# - The first line contains two integers, N (the array length) and Q (number of queries).
# - The second line contains N integers, representing the permutation P.
# - The next Q lines describe events:
#   - If Ti = 0 or Ti = 1, the event is followed by three integers l, r, c.
#   - If Ti = 2 or Ti = 3, the event is followed by two integers l, r.
#
# Standard Output:
# - For each query of type 2 or 3, output the result of the corresponding sum.
#
# Constraints:
# - 1 ≤ N, Q ≤ 10^5
# - 0 ≤ Ti ≤ 3
# - 1 ≤ l ≤ r ≤ N
# - 0 ≤ c ≤ 10^6
#
# Notes:
# - The array A is initially set to all zeros.
# - The permutation P contains unique indices for each position in the array.


import sys

def main():
    input = sys.stdin.read
    data = input().split()
    idx = 0

    N = int(data[idx])
    Q = int(data[idx + 1])
    idx += 2

    P = list(map(int, data[idx:idx + N]))
    idx += N

    A = [0] * N
    results = []

    for _ in range(Q):
        T = int(data[idx])
        l = int(data[idx + 1]) - 1
        r = int(data[idx + 2]) - 1
        idx += 3

        if T == 0:
            
            c = int(data[idx])
            idx += 1
            for i in range(l, r + 1):
                A[i] += c
        elif T == 1:
            c = int(data[idx])
            idx += 1
            for i in range(l, r + 1):
                A[P[i] - 1] += c
        elif T == 2:
            results.append(str(sum(A[l:r + 1])))
        elif T == 3:
            results.append(str(sum(A[P[i] - 1] for i in range(l, r + 1))))

    sys.stdout.write("\n".join(results) + "\n")

if __name__ == "__main__":
    main()
