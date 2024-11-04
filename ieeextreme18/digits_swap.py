# Digits Swap -> 92% of test cases passed
# Time limit: 500 ms
# Memory limit: 256 MB
#
# Given an integer N and another integer K, you can perform up to K operations to maximize the value of N.
# Each operation allows you to pick any two digits in N and swap them.
# - After each swap, the resulting number must not have leading zeroes.
# - The task is to find the maximum possible value of N after performing at most K swaps.
#
# Input:
# - The first line contains two integers, N (the initial number) and K (the maximum number of swaps allowed).
#
# Output:
# - Output a single integer, representing the largest possible value of N after performing up to K swaps.
#
# Constraints:
# - 1 ≤ N < 10^15
# - 1 ≤ K ≤ 25
# - The result of a swap must not start with a zero, as this would invalidate the number.

from sys import stdin
import heapq

def maximize_number(N, K):
    num = str(N)
    n = len(num)
    max_num = N

    # Use a max heap (priority queue)
    heap = []
    heapq.heappush(heap, (-int(num), num, 0))
    visited = set()

    while heap:
        # Limit the size of the priority queue to 50 elements
        if len(heap) > 50:
            heap = heap[:50]
            heapq.heapify(heap)

        neg_current_value, current_num, k = heapq.heappop(heap)
        current_value = -neg_current_value

        if k > K:
            continue

        # If we've already visited this number, skip it
        if current_num in visited:
            continue
        visited.add(current_num)

        # Update max_num if we found a larger number
        if current_value > max_num:
            max_num = current_value

        if k == K:
            continue

        num_list = list(current_num)

        for i in range(n - 1):
            # Find the maximum digit to the right of the current position
            max_digit = max(num_list[i + 1:])
            # Only consider swapping if there's a larger digit ahead
            if num_list[i] >= max_digit:
                continue
            # Track the best swap to ensure the largest possible outcome
            best_j = -1
            for j in range(n - 1, i, -1):
                if num_list[j] == max_digit:
                    # Skip swapping a zero into the first position
                    if i == 0 and num_list[j] == '0':
                        continue
                    best_j = j
                    break
            # Perform the swap if a valid position was found
            if best_j != -1:
                num_list[i], num_list[best_j] = num_list[best_j], num_list[i]
                next_num_str = ''.join(num_list)
                next_num_int = int(next_num_str)
                # If we haven't visited this number
                if next_num_str not in visited:
                    heapq.heappush(heap, (-next_num_int, next_num_str, k + 1))
                # Swap back to restore the original number
                num_list[i], num_list[best_j] = num_list[best_j], num_list[i]
    return max_num

# Read inputs
N, K = map(int, stdin.readline().split())
# Get the largest possible value after K swaps
result = maximize_number(N, K)
# Output the result
print(result)
