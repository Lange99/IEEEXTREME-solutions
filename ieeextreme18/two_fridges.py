# Two Fridges -> 100% Score
# Time limit: 750 ms
# Memory limit: 256 MB
#
# Dexter is playing again with N substances trying to complete his greatest invention. 
# Because it's running late, Dexter has decided the invention will have to wait until tomorrow.
# In the meanwhile, he needs to find a way to store the N substances in his two fridges. 
# Each fridge can be set to a certain temperature, an integer value between −100 and 100. 
# For each of the N substances, Dexter knows an interval [a_i, b_i], meaning the storing 
# temperature of the i-th substance needs to fall in that specific interval.
#
# Help Dexter decide the temperatures of the two fridges.
#
# Standard input:
# The first line contains a single integer N.
# Each of the following N lines contains two values a_i and b_i, representing the storing interval 
# for the i-th substance.
#
# Standard output:
# If there is no solution, print −1.
# Otherwise, print two values T1 and T2 (T1 ≤ T2), representing the temperatures of the two fridges.
#
# Constraints and notes:
# - 0 ≤ N ≤ 100
# - −100 ≤ a_i ≤ b_i ≤ 100
# - −100 ≤ T1 ≤ T2 ≤ 100
# If there are multiple solutions, print the one where T1 is minimum. If there are still multiple solutions, 
# print the one where T2 is minimum.


def find_fridge_temperatures(substances):
    # Collect all unique endpoints of the intervals
    endpoints = set()
    for a, b in substances:
        endpoints.add(a)
        endpoints.add(b)
    candidates = sorted(endpoints)
    
    # Try each candidate temperature
    for T in candidates:
        for reverse in [False, True]:
            group1 = []
            group2 = []
            for a, b in substances:
                if a <= T <= b:
                    if reverse:
                        group2.append((a, b))
                    else:
                        group1.append((a, b))
                else:
                    if reverse:
                        group1.append((a, b))
                    else:
                        group2.append((a, b))
            # Check if both groups have non-empty intersections
            valid = True
            # Check Group 1
            if group1:
                max_a1 = max(a for a, b in group1)
                min_b1 = min(b for a, b in group1)
                if max_a1 > min_b1:
                    valid = False
            else:
                max_a1 = None
                min_b1 = None
            # Check Group 2
            if group2:
                max_a2 = max(a for a, b in group2)
                min_b2 = min(b for a, b in group2)
                if max_a2 > min_b2:
                    valid = False
            else:
                max_a2 = None
                min_b2 = None
            if valid:
                # Assign temperatures
                if group1:
                    T1 = max_a1  # Any value in [max_a1, min_b1]
                else:
                    T1 = T  # Default value
                if group2:
                    T2 = max_a2  # Any value in [max_a2, min_b2]
                else:
                    T2 = T  # Default value
                # Ensure T1 <= T2 if required
                if T1 > T2:
                    T1, T2 = T2, T1
                return T1, T2
    # If no valid partition is found
    return -1


# Reading input
n = int(input())
if n == 0:
    print(-100, -100)
    exit()
substances = [tuple(map(int, input().split())) for _ in range(n)]

# Finding the solution and printing the result
result = find_fridge_temperatures(substances)
if result == -1:
    print(-1)
else:
    print(result[0], result[1])
