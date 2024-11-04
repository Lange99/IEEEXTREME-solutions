// Power of Three -> 40% of test cases passed
// Time limit: 1000 ms
// Memory limit: 256 MB
//
// Given a positive integer N, the task is to determine if there exists a nonnegative integer x
// such that 3^x = N. If such an integer exists, output x; otherwise, output -1.
//
// Input:
// - The input consists of one integer N.
//
// Output:
// - If there exists a nonnegative integer x such that 3^x = N, output x.
// - Otherwise, output -1.
//
// Constraints and Notes:
// - N is a nonnegative number with at most 10^7 digits.
// - The time limit is the same across all languages.
// - The test cases are grouped, and all tests in a group must pass to earn points for that group.


use std::io;

fn main() {
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    let input = input.trim();

    // Controllo dei casi speciali
    if input == "1" {
        println!("0");
        return;
    }
    if input == "0" || input.starts_with('-') || input.chars().any(|c| !c.is_digit(10)) {
        println!("-1");
        return;
    }

    let mut n = input.to_string();
    let mut x = 0;

    while n != "1" {
        if !is_divisible_by_3_fast(&n) {
            println!("-1");
            return;
        }

        // Divide n per 3 usando solo il necessario, per numeri grandi
        n = divide_by_3_optimized(&n);
        x += 1;
    }

    println!("{}", x);
}

// Funzione per verificare se il numero è divisibile per 3
fn is_divisible_by_3_fast(n: &str) -> bool {
    n.chars().filter_map(|c| c.to_digit(10)).sum::<u32>() % 3 == 0
}

/// Divides a large number (given as a string) by 3 without converting it to a numeric type.
/// This function performs long division on each digit, generating the quotient directly as a string.
///
/// # Explanation:
/// - Processes each digit of `n` sequentially, using the remainder from each division step.
/// - Uses modular arithmetic to carry over remainders between digits, simulating manual long division.
/// - Ignores leading zeros in the result for correct formatting.
///
/// # Example:
/// ```
/// let result = divide_by_3_optimized("124");
/// assert_eq!(result, "41");
/// ```
///
/// # Complexity:
/// - Efficient for large inputs, as it avoids conversions to numeric types, ideal for numbers
///   with up to 10 million digits.
fn divide_by_3_optimized(n: &str) -> String {
    // Initialize `result` as an empty string with preallocated capacity equal to the length of `n`.
    // This will store the final quotient as a string without leading zeros.
    let mut result = String::with_capacity(n.len());

    // `remainder` keeps track of the remainder for each digit division. 
    // This is crucial as it allows us to carry over any remainder to the next digit.
    let mut remainder = 0;

    // Iterate over each character `c` in the string `n`.
    for c in n.chars() {
        // Convert the current character `c` to a digit and add any leftover `remainder * 10`.
        // `current` represents the current number to divide, combining the remainder from the previous step.
        let current = remainder * 10 + c.to_digit(10).unwrap();

        // Calculate the current quotient by integer division of `current` by 3.
        let quotient = current / 3;

        // Update `remainder` with the remainder of `current / 3`, which will be used in the next iteration.
        remainder = current % 3;

        // To avoid leading zeros in `result`, we only append `quotient` if:
        // - `result` is not empty, or
        // - `quotient` is non-zero.
        if !(result.is_empty() && quotient == 0) {
            result.push(char::from_digit(quotient, 10).unwrap());
        }
    }

    // If `result` is still empty, it means the result of the division is zero.
    // Return "0" in this case; otherwise, return the `result` string.
    if result.is_empty() {
        "0".to_string()
    } else {
        result
    }
}
