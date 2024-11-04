# Laser Defense -> 100% of the test cases
# Time limit: 2500 ms
# Memory limit: 256 MB
#
# A group of thieves has decided to steal the statements of this year's IEEEXtreme. 
# To do so, they need to cross a parking lot in front of the IEEE headquarters.
#
# The parking lot can be viewed as a square with its lower-left corner at (0, 0) 
# and the upper-right corner at (L, L). In the lower-left and lower-right corners of the parking lot, 
# the scientific committee has installed two lasers that send beams of light capable of detecting movement.
#
# The two lasers are marked as A and B. The left laser (A) sends beams that intersect either 
# the upper or right sides of the square. The right laser (B) sends beams that intersect 
# either the upper or left sides.
#
# Each beam divides the parking lot into distinct areas. Given the number of beams and their directions, 
# your task is to compute the total number of resulting areas.
#
# Standard Input:
# - The first line contains three integers L, N, and M:
#   - L: size of the parking lot (side length of the square).
#   - N: number of beams sent by laser A.
#   - M: number of beams sent by laser B.
# - The next N lines describe the laser beams sent by laser A:
#   - Each line contains a character (U or R) and an integer coordinate C.
#     - 'U' specifies a beam that intersects the upper side, with C as the x-coordinate.
#     - 'R' specifies a beam that intersects the right side, with C as the y-coordinate.
# - The following M lines describe the laser beams sent by laser B:
#   - Each line contains a character (U or L) and an integer coordinate C.
#     - 'U' specifies a beam that intersects the upper side, with C as the x-coordinate.
#     - 'L' specifies a beam that intersects the left side, with C as the y-coordinate.
#
# Standard Output:
# - Print a single integer representing the number of resulting areas.
#
# Constraints and Notes:
# - 2 ≤ L ≤ 10^9
# - 0 ≤ N, M ≤ 10^5
# - 0 < C < L
# - No identical laser beams appear in the input.


from bisect import bisect_right

def count_areas(L, N, M, beams_A, beams_B):
    # Separate beams by type for laser A and laser B
    right_beams = []
    up_beams_A = []
    left_beams = []
    up_beams_B = []
    
    for beam in beams_A:
        direction, coord = beam
        if direction == 'R':
            right_beams.append(coord)
        elif direction == 'U':
            up_beams_A.append(coord)
    
    for beam in beams_B:
        direction, coord = beam
        if direction == 'L':
            left_beams.append(coord)
        elif direction == 'U':
            up_beams_B.append(coord)
      
    # Sort the beam coordinates for efficient processing
    right_beams.sort()
    up_beams_A.sort()
    left_beams.sort()
    up_beams_B.sort()

    # Number of beams in each category
    num_beams_right = len(right_beams)
    num_beams_left = len(left_beams)
    num_beams_up_A = len(up_beams_A)
    num_beams_up_B = len(up_beams_B)

    # Handle edge cases where beams only come from one side
    if num_beams_right == 0:
        return num_beams_left + 1
    if num_beams_left == 0:
        return num_beams_right + 1

    # Efficiently count the intersections between UP beams of A and B
    intersections = 0
    for beam_b in up_beams_B:
        idx = bisect_right(up_beams_A, beam_b)
        intersections += num_beams_up_A - idx

    # Calculate the number of resulting areas
    num_areas = N + 1 \
                + num_beams_left * (N + 1) \
                + intersections \
                + num_beams_up_B * num_beams_right \
                + num_beams_up_B

    return num_areas

# Reading input
L, N, M = map(int, input().split())
beams_A = [input().split() for _ in range(N)]
beams_A = [(direction, int(coord)) for direction, coord in beams_A]
beams_B = [input().split() for _ in range(M)]
beams_B = [(direction, int(coord)) for direction, coord in beams_B]

# Finding the number of resulting areas and printing the result
result = count_areas(L, N, M, beams_A, beams_B)
print(result)
