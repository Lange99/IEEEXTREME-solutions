# Another Sliding Window Problem -> 25% of the test cases passed
# Time limit: 500 ms
# Memory limit: 64 MB
#
# Given a sequence t1, t2, ..., tk, we are interested in grouping the elements into ⌈k/2⌉ groups.
# Each group will contain exactly 2 elements, and if k is odd, there will be exactly one group 
# with just one element. For each group, we compute the sum of its elements. The maximum of these 
# sums is called the matching cost.
#
# Out of all possible ways of grouping the elements, we are interested in the one that has the 
# smallest matching cost, which we call the optimal cost.
#
# For example, the optimal cost for (5, 1, 3, 4) is 7, obtained by grouping the elements as {{5,1},{3,4}}.
# Any other grouping results in a larger matching cost.
#
# You are given a sorted array A and need to answer Q queries:
# - Each query consists of a single integer x.
# - For each subarray of A with an optimal cost ≤ x, add the difference between the rightmost 
#   and the leftmost elements of the subarray. Formally, calculate:
#   ∑ 1 ≤ l ≤ r ≤ N, optimal_cost(A[l], ..., A[r]) ≤ x (A[r] - A[l])
#
# Standard Input:
# - The first line contains the integers N and Q, the number of elements in the sequence and the number of queries.
# - The second line contains the sequence of integers A1, A2, ..., AN separated by spaces.
# - The next Q lines each contain an integer x_i, the value of x for the i-th query.
#
# Standard Output:
# - For each query, return the value of the indicated summation.
#
# Constraints and Notes:
# - 1 ≤ N ≤ 10^5
# - 1 ≤ Q ≤ 100
# - 0 ≤ A[i] ≤ 10^9 for 1 ≤ i ≤ N
# - 0 ≤ x_i ≤ 2 × 10^9 for 1 ≤ i ≤ Q


def find_min_matching_cost(arr):
    matching_cost = 0
    lenght = len(arr)
    if lenght % 2 == 1:
        for i in range(int(lenght/2)):
            matching_cost = max(matching_cost, arr[i] + arr[-2-i])
    else:
        for i in range(int(lenght/2)):
            matching_cost = max(matching_cost, arr[i] + arr[-1-i])

    return matching_cost

def calculate_sum_of_matching_costs(arr, max_matching_costs):
    n = len(arr)
    sum = 0

    for i in range(n):
        for j in range(i + 1, n):
            subarray = arr[i:j+1]
            if subarray[0] < max_matching_costs:
                if find_min_matching_cost(subarray) <= max_matching_costs:
                    sum += subarray[-1] - subarray[0]
            else:
                return sum;
    return sum

N, Q = map(int, input().split())
A = list(map(int, input().split()))
for _ in range(Q):
    max_matching_costs = int(input())
    result = calculate_sum_of_matching_costs(A, max_matching_costs)
    print(result)
