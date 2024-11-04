# Triumvirates -> 18.8 of test cases passed
# Time limit: 1000 ms
# Memory limit: 512 MB
#
# You have a group of N friends, where N is a multiple of 3. Each friend is located at a 2D position
# given by their coordinates. The goal is to group them into triumvirates (groups of three friends).
# 
# We define the stability of a triumvirate as the difference between the longest and shortest 
# distances between any two members of the group.
#
# Standard Input:
# - The first line contains the integer N, the number of friends.
# - The next N lines contain two integers representing the coordinates of each friend,
#   listed from index 0 to index N-1.
#
# Standard Output:
# - The output should contain N/3 lines, each containing the indices of the points that form a group.
# - Each index from 0 to N-1 must be included in exactly one line.
#
# Scoring:
# - Your score for a test case is the sum of all the stabilities for all triumvirates.
# - The objective is to minimize the score, which represents the instability in the groupings.
# - Your performance on each test case will be evaluated relative to the best solution for that test case:
#   TestValue * (BestScore / YourScore), where BestScore is the lowest score achieved by any contestant.
#
# Constraints and Notes:
# - N ≤ 99,999.
# - Coordinates fit within signed 32-bit integers.
# - The best score for each test case is strictly greater than 0.
# - The time limit is the same for all programming languages.

import sys

def hilbert_order(x, y, bits=16):
    """Compute the Hilbert order of a point (x, y) for a given number of bits."""
    # Mask to extract bits
    mask = 1 << (bits - 1)
    h = 0
    for i in range(bits):
        rx = (x & mask) > 0
        ry = (y & mask) > 0
        h <<= 2
        h |= (rx * 3) ^ int(ry)
        x <<= 1
        y <<= 1
    return h

def main():
    # Read input 
    N = int(sys.stdin.readline())
    data = sys.stdin.read().split()
    x_values = list(map(int, data[::2]))
    y_values = list(map(int, data[1::2]))
    
    # Normalize coordinates to non-negative integers
    min_x = min(x_values)
    min_y = min(y_values)
    x_values = [x - min_x for x in x_values]
    y_values = [y - min_y for y in y_values]
    
    # Determine the number of bits required to represent the coordinates
    max_coord = max(max(x_values), max(y_values))
    bits = max_coord.bit_length()
    if bits == 0:
        bits = 1  # Handle the case where all coordinates are zero

    # Compute Hilbert indices
    points = []
    for idx, (x, y) in enumerate(zip(x_values, y_values)):
        h_order = hilbert_order(x, y, bits)
        points.append((h_order, idx))
    
    # Sort points based on Hilbert order
    points.sort()
    
    
    # Group points into triumvirates and print indices
    for i in range(0, N, 3):
        indices = [str(points[i + j][1]) for j in range(3)]
        print(' '.join(indices))

if __name__ == '__main__':
    main()
