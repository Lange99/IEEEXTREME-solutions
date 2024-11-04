# Brick Stacks -> 100% of the test cases
# Time limit: 2000 ms
# Memory limit: 256 MB
#
# You are given N bricks of lengths A1, A2, ..., AN and an integer x. You can place brick i on top of brick j
# (for any i ≠ j) if and only if the condition A[i] + x ≤ A[j] is satisfied.
# The task is to arrange the bricks into the minimum number of stacks such that this condition holds for each stack.
#
# Input:
# - The first line contains two integers N (number of bricks) and x (minimum difference required to stack one brick on another).
# - The second line contains N integers representing the lengths of the bricks A1, A2, ..., AN.
#
# Output:
# - Output a single integer, representing the minimum number of stacks required.
# - Then, for each stack, output the number of bricks in the stack followed by the lengths of the bricks in that stack,
#   listed from the largest brick to the smallest.
# - If multiple arrangements result in the minimum number of stacks, any valid arrangement can be printed.
#
# Constraints:
# - 1 ≤ N ≤ 10^6
# - 1 ≤ x ≤ 10^9
# - 1 ≤ A[i] ≤ 10^9
#
# Notes:
# - The tests are grouped, and all tests in a group must pass to score points.

import heapq

def minimum_stacks(N, x, A):
    # Sort the bricks in ascending order
    A.sort()
    
    # Min-heap to store available stacks based on top brick sizes
    heap = []
    stack_counter = 0
    positions = []  # List to keep track of which stack each brick goes to
    
    for brick in A:
        if heap and heap[0][0] + x <= brick:
            # Place the brick on the stack with the smallest top brick
            top_brick_size, stack_idx = heapq.heappop(heap)
            positions.append(stack_idx)
        else:
            # Create a new stack
            stack_idx = stack_counter
            stack_counter += 1
            positions.append(stack_idx)
        # Push the current brick onto the heap as the new top of its stack
        heapq.heappush(heap, (brick, stack_idx))
    
    # Reconstruct the stacks using the positions list
    num_stacks = stack_counter
    stacks = [[] for _ in range(num_stacks)]
    for brick, stack_idx in zip(A, positions):
        stacks[stack_idx].append(brick)
    
    # Prepare the output
    print(num_stacks)
    for stack in stacks:
        print(len(stack), " ".join(map(str, reversed(stack))))

# Read input
N, x = map(int, input().split())
A = list(map(int, input().split()))

# Solve the problem
minimum_stacks(N, x, A)
