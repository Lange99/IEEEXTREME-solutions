# Cheap Construction -> 37.5 of the test cases
# Time limit: 2500 ms
# Memory limit: 256 MB
#
# Moto Archipelago has N islands numbered from 1 to N. The manager wants to connect the islands 
# with bridges using Kashi Construction Company.
#
# Kashi Construction Company works based on a string S of lowercase alphabets, where each character 
# represents one of the N islands. Given a substring T, the company performs the following operation:
# - For every l and r such that S[l, r] = T, it builds bridges to connect consecutive islands 
#   from island l to island r.
# 
# For example, if S = "aabcabcaa" and T = "abca", then the substring S[2,5] matches T, resulting 
# in bridges between islands (2,3), (3,4), and (4,5). Similarly, S[5,8] matches T, resulting in 
# bridges (5,6), (6,7), and (7,8).
#
# The task is to determine the shortest string T that can be sent to the company to achieve exactly 
# k connected components for each k from 1 to N. If it's not possible to achieve exactly k components 
# with any substring T, the answer should be 0 for that k.
#
# Standard Input:
# - The first line contains the string S of lowercase alphabets.
#
# Standard Output:
# - Output N integers in one line. The i-th integer represents the answer for k = i.
#
# Constraints and Notes:
# - 1 ≤ N ≤ 5000


def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

def union(parent, rank, x, y):
    rootX = find(parent, x)
    rootY = find(parent, y)
    if rootX != rootY:
        if rank[rootX] > rank[rootY]:
            parent[rootY] = rootX
        elif rank[rootX] < rank[rootY]:
            parent[rootX] = rootY
        else:
            parent[rootY] = rootX
            rank[rootX] += 1

def count_components(n, bridges):
    parent = list(range(n))
    rank = [0] * n
    for u, v in bridges:
        union(parent, rank, u, v)
    return len(set(find(parent, i) for i in range(n)))

def shortest_string_for_components(S):
    N = len(S)
    results = [0] * N
    seen_substrings = set()
    
    for length in range(1, N + 1):
        for start in range(N - length + 1):
            T = S[start:start + length]
            if T in seen_substrings:
                continue
            seen_substrings.add(T)
            bridges = []
            for i in range(N - length + 1):
                if S[i:i + length] == T:
                    for j in range(i, i + length - 1):
                        bridges.append((j, j + 1))
            components = count_components(N, bridges)
            if components <= N and (results[components - 1] == 0 or length < results[components - 1]):
                results[components - 1] = length
    
    return results

# Read input using custom parser
def parser():
    while 1:
        data = list(input().split(' '))
        for number in data:
            if len(number) > 0:
                yield(number)   

input_parser = parser()

def get_word():
    global input_parser
    return next(input_parser)

S = get_word().strip()

# Get the results
results = shortest_string_for_components(S)

# Print the results
print(" ".join(map(str, results)))
