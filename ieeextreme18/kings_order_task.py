import heapq
from collections import defaultdict, deque
import sys

"""
### King's Order Task -> 100% of the test cases passed

In the kingdom of Lexiconia, King Algorithmus has assigned his loyal knights an important mission: to complete a series of significant projects. These projects are organized into different groups, each with a unique group ID. However, there are dependencies between projects, meaning that some must be completed before others can start. Additionally, King Algorithmus decreed that the projects must be completed in a specific order following the kingdom's ancient rules.

#### Rules for Ordering Projects:
1. Projects can only be executed if all their dependencies have already been completed.
2. If there are multiple projects ready to be executed (i.e., no pending dependencies):
   - Choose the project with the lowest group ID.
   - If multiple projects share the same group ID, choose the one with the lowest project ID.

Your goal as the royal advisor is to help the knights determine a valid order to complete all the projects while respecting all dependencies and the kingdom's rules. If no valid order exists due to cyclic dependencies, you must declare that it is impossible.

#### Input
The input consists of the following:
1. The first line contains two integers, `N` and `M`:
   - `N`: Number of projects (≤ 1000).
   - `M`: Number of dependencies (≤ 10000).
2. The second line contains `N` integers representing the group IDs of the projects, where the `i`-th integer indicates the group ID of project `i`.
3. The next `M` lines each contain two integers, `A` and `B`, indicating that project `A` must be completed before project `B`.

#### Output
The output should be a single line containing a valid order of project execution such that:
- All dependencies are satisfied.
- The sequence is lexicographically minimal based on the group ID and project ID rules.

If there is no valid order due to a cycle, output `-1`.

#### Example
##### Input
```
5 4
3 2 2 1 3
1 3
1 4
3 5
4 5
```
##### Output
```
2 1 4 3 5
```

#### Notes
- Projects are represented as nodes of a directed graph, with dependencies represented as directed edges.
- The problem can be solved using topological sorting with a priority queue to ensure the lexicographically minimal order.
- If a cycle is detected, output `-1` to indicate that it is impossible to complete all projects.

"""

def find_order(N, M, group_ids, dependencies):
    # Create adjacency list and in-degree count
    adj_list = defaultdict(list)
    in_degree = [0] * (N + 1)
    
    for A, B in dependencies:
        adj_list[A].append(B)
        in_degree[B] += 1
    
    # Min-heap to get the lexicographically smallest order
    min_heap = []
    
    # Initialize the heap with nodes having zero in-degree
    for i in range(1, N + 1):
        if in_degree[i] == 0:
            heapq.heappush(min_heap, (group_ids[i - 1], i))
    
    result = []
    
    while min_heap:
        group_id, node = heapq.heappop(min_heap)
        result.append(node)
        
        for neighbor in adj_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                heapq.heappush(min_heap, (group_ids[neighbor - 1], neighbor))
    
    if len(result) == N:
        return result
    else:
        return -1

# Read input
input = sys.stdin.read
data = input().split()

N = int(data[0])
M = int(data[1])
group_ids = list(map(int, data[2:N+2]))
dependencies = [tuple(map(int, data[i:i+2])) for i in range(N+2, len(data), 2)]

# Find the order
order = find_order(N, M, group_ids, dependencies)

# Print the result
if order == -1:
    print(order)
else:
    print(" ".join(map(str, order)))