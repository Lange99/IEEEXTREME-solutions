
# Corporation -> 25% of the test cases passed
# Time limit: 1000 ms
# Memory limit: 256 MB
#
# A corporation has N employees with IDs from 1 to N, each with an initial monthly salary. Two types of events can occur:
#
# Event Types:
# - Type 0: All employees from l to r have their salary set to c.
# - Type 1: Each employee from l to r has their salary increased by c (c can be negative).
#   - After each event, an employee's happiness changes based on whether their salary increased (+1), decreased (-1),
#     or remained the same (no change).
#
# Query Types:
# - Type 2: Calculate the average salary of all employees from l to r.
# - Type 3: Calculate the average happiness of all employees from l to r.
#
# The goal is to process Q events and queries.
#
# Input:
# - The first line contains two integers N (number of employees) and Q (number of events/queries).
# - The second line contains N integers representing the initial salaries of the employees.
# - The next Q lines describe consecutive events and queries:
#   - Type 0: 0 l r c (set salaries from l to r to c)
#   - Type 1: 1 l r c (adjust salaries from l to r by c)
#   - Type 2: 2 l r (query the average salary from l to r)
#   - Type 3: 3 l r (query the average happiness from l to r)
#
# Output:
# - For each query of type 2 or type 3, output the result as a fraction P/Q in its simplest form,
#   where P and Q are coprime integers (gcd(P, Q) = 1).
#
# Constraints and Notes:
# - 1 ≤ N, Q ≤ 2 * 10^5
# - Initial salaries are integers in the range [1, 10^9]
# - 1 ≤ l ≤ r ≤ N
# - -10^9 ≤ c ≤ 10^9
# - Salary values can become negative after some events.
# - Each employee's initial happiness is 0.

from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def get_fraction(num, denom):
    common_divisor = gcd(num, denom)
    return f"{num // common_divisor}/{denom // common_divisor}"

def process_queries(n, q, salaries, operations):
    happiness = [0] * n
    
    results = []
    for op in operations:
        if op[0] == 0:
            # Type 0: Set salaries from l to r to c
            _, l, r, c = op
            for i in range(l-1, r):
                if salaries[i] < c:
                    happiness[i] += 1
                elif salaries[i] > c:
                    happiness[i] -= 1
                salaries[i] = c
        elif op[0] == 1:
            # Type 1: Increment salaries from l to r by c
            _, l, r, c = op
            for i in range(l-1, r):
                if c > 0:
                    happiness[i] += 1
                elif c < 0:
                    happiness[i] -= 1
                salaries[i] += c
        elif op[0] == 2:
            # Type 2: Query average salary from l to r
            _, l, r = op
            total_salary = sum(salaries[l-1:r])
            count = r - l + 1
            results.append(get_fraction(total_salary, count))
        elif op[0] == 3:
            # Type 3: Query average happiness from l to r
            _, l, r = op
            total_happiness = sum(happiness[l-1:r])
            count = r - l + 1
            results.append(get_fraction(total_happiness, count))
    
    return results

# Input
n, q = map(int, input().split())
salaries = list(map(int, input().split()))
operations = [list(map(int, input().split())) for _ in range(q)]

# Process the queries
results = process_queries(n, q, salaries, operations)

# Output the results
for result in results:
    print(result)
