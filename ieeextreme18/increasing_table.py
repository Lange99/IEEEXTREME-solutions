
# Increasing Table -> 58% of test cases passed
# Time limit: 2000 ms
# Memory limit: 256 MB
#
# Alice has a number N and she wants to build a table T with 2 rows and N columns. 
# The table T should respect the following constraints:
# - Each number from 1 to 2*N appears in T exactly once.
# - The numbers in each row should be in increasing order: T[i, j] < T[i, j+1] for all 1 ≤ i ≤ 2, 1 ≤ j < N.
# - The numbers in each column should also be in increasing order: T[1, j] < T[2, j] for all 1 ≤ j ≤ N.
#
# Additionally, for each number from 1 to 2*N, Alice knows whether she wants to use that particular 
# number on the first row of T, on the second row of T, or both. Alice has two disjoint arrays A and B, where:
# - The numbers from A should only be used on the first row.
# - The numbers from B should only be used on the second row.
# - The numbers that don't appear in either A or B have no restrictions.
#
# Print the number of valid ways to fill the table T modulo 998244353.
#
# Standard Input:
# - The first line of input contains an integer N.
# - The second line contains an integer X and then X distinct integers representing the elements of A.
# - The third line contains an integer Y and then Y distinct integers representing the elements of B.
#
# Standard Output:
# - Output one integer — the number of valid ways to fill the 2×N table modulo 998244353.
#
# Constraints and Notes:
# - 1 ≤ N ≤ 2000
# - 0 ≤ X, Y ≤ N
# - Sets A and B are disjoint and contain distinct integers from 1 to 2*N.

MOD = 998244353

def modinv(a):
    # Modular inverse using Fermat's little theorem
    return pow(a, MOD - 2, MOD)

def nCr_mod(n, r):
    # Compute nCr modulo MOD
    if r < 0 or r > n:
        return 0
    return (fact[n] * inv_fact[r] % MOD) * inv_fact[n - r] % MOD

# Precompute factorials and inverse factorials
MAXN = 2 * 10**5 + 10
fact = [1] * MAXN
inv_fact = [1] * MAXN
for i in range(1, MAXN):
    fact[i] = fact[i - 1] * i % MOD
inv_fact[MAXN - 1] = modinv(fact[MAXN - 1])
for i in range(MAXN - 2, -1, -1):
    inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD

def solve(N, A, B):
    total_numbers = set(range(1, 2*N + 1))
    A_set = set(A)
    B_set = set(B)
    S = sorted(total_numbers - A_set - B_set)  # Unrestricted numbers

    K = len(S)
    K1 = N - len(A)
    K2 = N - len(B)

    if K1 < 0 or K2 < 0:
        return 0  # Impossible to fill the rows

    # Check ordering constraints between A and B
    max_A = max(A) if A else -float('inf')
    min_B = min(B) if B else float('inf')
    if max_A > min_B:
        return 0  # Ordering constraint violated

    # Number of valid mergings (generalized Catalan number)
    if K1 >= K2:
        numerator = K1 - K2 + 1
        denominator = K1 + 1
        n = K1 + K2
        ways = nCr_mod(n, K1) * numerator % MOD * modinv(denominator) % MOD
    else:
        return 0  # No valid mergings if K1 < K2

    return ways

# Reading input
N = int(input())
A_input = list(map(int, input().split()))
X = A_input[0]
A = A_input[1:]
B_input = list(map(int, input().split()))
Y = B_input[0]
B = B_input[1:]

# Solving the problem
result = solve(N, A, B)
print(result)
