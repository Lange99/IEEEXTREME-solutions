# Stick -> 100% of the test cases
# Time limit: 1000 ms
# Memory limit: 256 MB
#
# There are N squares on a cartesian plane. The i-th square has its bottom-left corner at 
# (i * K - L, i * K - L) and top-right corner at (i * K + L, i * K + L).
# The task is to calculate the area of the union of these squares.
#
# Standard Input:
# - The input consists of a single line containing three integers N, K, and L:
#   - N: the number of squares.
#   - K: the distance between the centers of consecutive squares.
#   - L: half the side length of each square.
#
# Standard Output:
# - Output a single integer representing the area of the union of the squares.
#
# Constraints and Notes:
# - 1 ≤ N, K ≤ 10^9
# - 1 ≤ L ≤ 5 × 10^4

def calculate_union_area(N, K, L):
    # Case for N = 1
    if N == 1:
        return 4 * L * L

    # Disjoint case
    if K >= 2 * L:
        return N * 4 * L * L
    
    # Overlapping case
    overlap = max(0, 2 * L - K)  # Calculate the overlapping length
    overlap_area = overlap * overlap  # Area of overlap between consecutive squares
    total_area = N * 4 * L * L - (N - 1) * overlap_area  # Optimized calculation for total area
    
    return total_area

# Read input
N, K, L = map(int, input().split())

# Calculate and print the result
print(calculate_union_area(N, K, L))
