# Halving -> 30% of the test cases
# Time limit: 1000 ms
# Memory limit: 64 MB
#
# Alice and Bob are playing a secret communication game. Alice writes down a permutation A of size 2*N,
# containing each integer from 1 to 2*N exactly once. Bob selects a binary array R of size N, known as the "ruleset".
#
# Using A and R, Alice creates an array B of size N based on the following rules:
# - If R[i] = 0, then B[i] = min(A[2*i - 1], A[2*i])
# - If R[i] = 1, then B[i] = max(A[2*i - 1], A[2*i])
#
# Unfortunately, some values in A have been obscured. You are given:
# - C, an array of size 2*N, where each C[i] is:
#   - C[i] = A[i] if the value is still readable,
#   - C[i] = -1 if the value is unreadable.
# - R, the ruleset array of size N.
# - B, the result array from Alice based on A and R.
#
# Your task is to calculate the number of possible initial arrays A consistent with the given data, modulo 998244353.
#
# Input:
# - First line: integer N (1 ≤ N ≤ 300).
# - Second line: array C of length 2*N with values in the range [-1, 1 to 2*N], where -1 represents an unreadable value.
# - Third line: binary array R of length N.
# - Fourth line: array B of length N with distinct values from 1 to 2*N.
#
# Output:
# - Output a single integer, the number of permutations of A consistent with the given data, modulo 998244353.
#
# Constraints and Notes:
# - 1 ≤ N ≤ 300
# - C[i] = -1 or 1 ≤ C[i] ≤ 2*N; all positive values in C are distinct.
# - Each R[i] is either 0 or 1.
# - Each B[i] is distinct and between 1 and 2*N.


MOD = 998244353

import sys
import threading
def main():
    import sys
    sys.setrecursionlimit(1 << 25)
    N = int(sys.stdin.readline())
    C = list(map(int, sys.stdin.readline().split()))
    R = list(map(int, sys.stdin.readline().split()))
    B = list(map(int, sys.stdin.readline().split()))

    fixed_numbers = set(c for c in C if c != -1)
    missing_numbers = set(range(1, 2*N +1)) - fixed_numbers
    missing_numbers = list(missing_numbers)
    num_to_idx = {num:i for i,num in enumerate(missing_numbers)}

    # For each position, store the possible numbers that can go into that position
    position_options = [set() for _ in range(2*N)]
    for i in range(2*N):
        if C[i] != -1:
            position_options[i].add(C[i])
        else:
            position_options[i] = set(missing_numbers)

    # For each pair, adjust the options based on R and B
    possible_pairs = []

    valid = True
    for i in range(N):
        p1 = 2*i
        p2 = 2*i +1
        R_i = R[i]
        B_i = B[i]

        A_p1_options = position_options[p1]
        A_p2_options = position_options[p2]

        fixed_p1 = len(A_p1_options) == 1
        fixed_p2 = len(A_p2_options) == 1

        if fixed_p1 and fixed_p2:
            a1 = next(iter(A_p1_options))
            a2 = next(iter(A_p2_options))
            if R_i == 0 and min(a1, a2) != B_i:
                valid = False
                break
            if R_i == 1 and max(a1, a2) != B_i:
                valid = False
                break
            possible_pairs.append([(a1, a2)])
            continue

        possible_assignments = []
        # Generate possible assignments for this pair
        for a1 in A_p1_options:
            for a2 in A_p2_options:
                if a1 == a2:
                    continue
                if R_i == 0 and min(a1, a2) != B_i:
                    continue
                if R_i == 1 and max(a1, a2) != B_i:
                    continue
                possible_assignments.append((a1, a2))
        if not possible_assignments:
            valid = False
            break
        possible_pairs.append(possible_assignments)

    if not valid:
        print(0)
        return

    # Now, we need to count the number of ways to select an assignment for each pair
    # such that the numbers used are unique across pairs.

    # Since the numbers range from 1 to 2N, and we have up to N pairs, we can represent
    # the used numbers with bitmasks. But since 2N can be up to 600, we cannot use bitmasks directly.

    # Instead, we'll use DP with memoization, where the state includes the index of the pair
    # and a tuple of used numbers.

    from functools import lru_cache

    @lru_cache(None)
    def dp(index, used_numbers):
        if index == N:
            return 1
        total = 0
        for a1, a2 in possible_pairs[index]:
            if a1 in used_numbers or a2 in used_numbers:
                continue
            new_used = used_numbers + (a1, a2)
            new_used = tuple(sorted(new_used))
            total = (total + dp(index+1, new_used)) % MOD
        return total

    result = dp(0, ())
    print(result % MOD)

threading.Thread(target=main).start()
