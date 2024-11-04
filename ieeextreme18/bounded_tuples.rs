// Bounded Tuples -> 31% of test cases passed
// Time limit: 3000 ms
// Memory limit: 256 MB
//
// Alice needs to choose N non-negative integer values V1, V2, ..., VN.
//
// Bob gives Alice M constraints of the form: the sum of the elements of a given subset of V
// should be greater or equal than a given value 'low' and smaller or equal than another
// given value 'high'. Formally, the i-th constraint is represented by a set of Ki indices
// P1, P2, ..., PKi, such that:
//
// low_i ≤ V[P1] + V[P2] + ... + V[PKi] ≤ high_i
//
// Your task is to calculate how many assignments of the variables Vi satisfy all the inequalities.
// Output the result modulo 998244353. However, if there are infinitely many valid assignments, print "infinity".
//
// Standard Input:
// - The first line contains two integers N and M.
// - The next M lines each contain the integers low_i, high_i, and Ki. Then, on the same line,
//   Ki indices P1, P2, ..., PKi follow.
//
// Standard Output:
// - Print the answer on the first line.
//
// Constraints and Notes:
// - 1 ≤ N ≤ 8
// - 0 ≤ M ≤ 4
// - 0 ≤ low_i, high_i ≤ 10^18
// - 1 ≤ Ki ≤ 3

use std::io;

const MOD: u64 = 998244353;

fn find_tuples_within_bounds(
    n: usize,
    low_high: &Vec<(u64, u64)>,
    indices: &Vec<Vec<usize>>,
) -> u64 {
    let max_value = low_high.iter().map(|&(_, high)| high).max().unwrap_or(0) as usize;

    // Initialize DP table
    let mut dp = vec![vec![0u64; max_value + 1]; n + 1];
    dp[0][0] = 1; // There's one way to make sum 0 with 0 elements

    // Fill DP table to count valid sums
    for i in 1..=n {
        for j in 0..=max_value {
            dp[i][j] = dp[i - 1][j];
            if j > 0 {
                dp[i][j] = (dp[i][j] + dp[i][j - 1]) % MOD;
            }
        }
    }

    let mut count = 0;

    // Function to validate if the tuple sums are within specified bounds
    fn is_valid(tpl: &[u64], low_high: &Vec<(u64, u64)>, indices: &Vec<Vec<usize>>) -> bool {
        // Iterate over each constraint in `low_high`, obtaining the index and the (low, high) bounds
        for (i, &(low, high)) in low_high.iter().enumerate() {
            // Calculate the sum of elements specified by the current constraint
            // `indices[i]` contains the indices of `tpl` to sum for constraint `i`
            let element_sum: u64 = indices[i].iter().map(|&index| tpl[index]).sum();

            // Check if the calculated sum is within the bounds `low` and `high`
            // If the sum does not satisfy the constraint, return `false` since the tuple is invalid
            if element_sum < low || element_sum > high {
                return false;
            }
        }
        // If all sums satisfy their constraints, return `true` indicating the tuple is valid
        true
    }

    // Generate tuples and validate only those within bounds using DP count
    let mut tpl = vec![0; n];
    while tpl[0] <= max_value as u64 {
        if is_valid(&tpl, low_high, indices) {
            count = (count + 1) % MOD;
        }

        // Increment tuple values without exceeding max_value
        let mut i = n - 1;
        loop {
            tpl[i] += 1;
            if tpl[i] <= max_value as u64 {
                break;
            } else {
                tpl[i] = 0;
                if i == 0 {
                    return count; // Exit once we've iterated all tuples
                }
                i -= 1;
            }
        }
    }

    count
}

fn main() {
    let mut input = String::new();
    io::stdin()
        .read_line(&mut input)
        .expect("Failed to read line");
    let nums: Vec<usize> = input
        .trim()
        .split_whitespace()
        .map(|x| x.parse().expect("Not a number"))
        .collect();
    let n = nums[0];
    let m = nums[1];

    let mut low_high = vec![];
    let mut indices = vec![];

    for _ in 0..m {
        let mut line = String::new();
        io::stdin()
            .read_line(&mut line)
            .expect("Failed to read line");
        let data: Vec<u64> = line
            .trim()
            .split_whitespace()
            .map(|x| x.parse().expect("Not a number"))
            .collect();

        let low = data[0];
        let high = data[1];
        let k = data[2] as usize;
        // Subtract 1 from each index to convert to 0-based index
        // necessary for the tuple generation 
        let idx = data[3..3 + k].iter().map(|&x| (x - 1) as usize).collect();

        low_high.push((low, high));
        indices.push(idx);
    }

    if m == 0 {
        println!("infinity");
    } else {
        println!("{}", find_tuples_within_bounds(n, &low_high, &indices));
    }
}
