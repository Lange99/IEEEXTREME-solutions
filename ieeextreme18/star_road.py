# Star Road -> 20% of test cases passed
# Time limit: 1000 ms
# Memory limit: 256 MB
#
# You are a food critic that just finished competing in the IEEExtreme, and you started 
# traveling through a country with N cities. Each city has a restaurant which is rated 
# by a number of stars, indicating how good it is. The country has N−1 roads, such that 
# there is a unique simple path between any two cities.
#
# As a very strict food critic, you only eat at a new restaurant if it has strictly more 
# stars than the one where you last dined. However, you also love to eat, so you want to 
# visit the maximum number of restaurants possible while following these rules.
#
# You are tasked with planning a journey that starts at some city A and ends at some city B, ensuring that:
# - You can eat in as many restaurants as possible during the journey.
# - You never go back through the same road once you've passed it.
#
# Note that you don't have to eat in every single city you visit, but can simply pass through it.
#
# Standard input:
# - The first line contains an integer N, the number of cities.
# - The second line contains N integers, where the i-th integer represents the number of 
#   stars of the restaurant in city i.
# - The following N−1 lines each contain two integers u and v, indicating a road between cities u and v.
#
# Standard output:
# - Print the maximum number of restaurants the critic can dine at, under the given constraints.
#
# Constraints and notes:
# - 2 ≤ N ≤ 10^5
# - 1 ≤ S_i ≤ 10^5, where by S_i we understand the number of stars for the restaurant in city i.
# - 1 ≤ u ≠ v ≤ N for every road.

def max_restaurants(N, stars, edges):
    # Build adjacency list
    adj = [[] for _ in range(N)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    dp = [1] * N  # Initialize dp array

    # Sort nodes based on star ratings
    # example of nodes: [(1, 0), (2, 1), (3, 2), (4, 3), (5, 4)]
    nodes = sorted([(stars[u], u) for u in range(N)])


    # Process nodes in increasing order of star ratings
    for star_u, u in nodes:
        for v in adj[u]:
            if stars[v] < star_u:
                dp[u] = max(dp[u], dp[v] + 1)

    return max(dp)


# Example usage:
N = int(input())
stars = list(map(int, input().split()))
edges = [tuple(map(lambda x: int(x)-1, input().split())) for _ in range(N-1)]
print(max_restaurants(N, stars, edges))