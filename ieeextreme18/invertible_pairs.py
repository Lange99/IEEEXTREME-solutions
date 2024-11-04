# Invertible Pairs -> 45% of test 
# Time limit: 1500 ms
# Memory limit: 512 MB
#
# Given an integer array A (1-indexed) of even length n, you can perform the following operation as many times as needed:
# - Choose a pair of positions 2k-1 and 2k, and multiply both A[2k-1] and A[2k] by -1.
# The goal is to maximize the maximum subarray sum of the resulting array after performing the operations.
#
# Input:
# - The first line contains an integer T, the number of test cases.
# - For each test case:
#   - The first line contains an even integer N (length of the array).
#   - The second line contains N integers representing the array A.
#
# Output:
# - Print t lines, where each line contains the answer for the i-th test case, which is the maximum possible subarray sum.
#
# Constraints and Notes:
# - 1 ≤ T ≤ 10^5
# - 1 ≤ sum of all N[i] ≤ 4 * 10^5
# - 2 ≤ N[i] ≤ 2 * 10^5, and N[i] is even for every i.
# - |A[j]| ≤ 10^4 for every valid j.
#
# The task is to determine the maximum possible subarray sum of the resulting array by optimally flipping pairs of elements.


def maximize_subarray_sum(T, test_cases):
    results = []
    
    for i in range(T):
        n = test_cases[i][0]
        arr = test_cases[i][1]
        
        # Array ottimizzato per la massima somma possibile
        optimized_arr = []
        for j in range(0, n, 2):
            # Aggiungi coppia invertita o non invertita in base alla somma maggiore
            if arr[j] + arr[j + 1] < -arr[j] - arr[j + 1]:
                optimized_arr.extend([-arr[j], -arr[j + 1]])
            else:
                optimized_arr.extend([arr[j], arr[j + 1]])

        # Calcola la somma massima della sottoarray ottimizzata
        max_sum = max_subarray_sum(optimized_arr)
        results.append(max_sum)
    
    return results

def max_subarray_sum(arr):
    # Algoritmo di Kadane per la somma massima della sottoarray
    max_so_far = arr[0]
    max_ending_here = arr[0]
    
    for x in arr[1:]:
        max_ending_here = max(x, max_ending_here + x)
        max_so_far = max(max_so_far, max_ending_here)
        
    return max_so_far

# Lettura dell'input
import sys
input = sys.stdin.read
data = input().splitlines()

# Numero di test case
T = int(data[0])

# Preparazione dei test case
test_cases = []
index = 1
for _ in range(T):
    n = int(data[index])
    arr = list(map(int, data[index + 1].split()))
    test_cases.append((n, arr))
    index += 2

# Calcolo dei risultati
output = maximize_subarray_sum(T, test_cases)
for result in output:
    print(result)
    
