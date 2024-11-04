// Rectangles and Arrays -> 90% of the test cases passed
// Time limit: 500 ms
// Memory limit: 256 MB
//
// You are given an array A of N integers representing heights. The task is to determine the largest possible
// area of a rectangle that can be formed using a contiguous subarray of A.
//
// A rectangle is defined by choosing two indices l and r (1 ≤ l ≤ r ≤ N) and a height h such that h is
// not greater than any of the elements between indices l and r, inclusive. The area of the rectangle
// is calculated as (r - l + 1) * h.
//
// Additionally, you can modify the value of any element in the array once to any positive integer between 1 and X.
// After making this one modification, you need to determine the maximum possible area of any rectangle that can be formed.
//
// Input:
// - The first line contains two integers, N (number of elements) and X (maximum value to which you can set an element).
// - The second line contains N integers, representing the heights A[i] in the array.
//
// Output:
// - Output a single integer representing the maximum area of a rectangle that can be formed after modifying at most
//   one element of the array.
//
// Constraints:
// - 1 ≤ N ≤ 10^6
// - 1 ≤ X ≤ 10^6
// - 1 ≤ A[i] ≤ 10^6 for every i=1,…,N

use std::io;
use std::cmp;

/// Function to calculate the largest possible area of a rectangle using precomputed limits.
/// `heights`: array of heights.
/// `left`, `right`: arrays representing the indices of the nearest smaller elements to the left and right of each element.
fn largest_rectangle_area(heights: &Vec<i32>, left: &Vec<usize>, right: &Vec<usize>) -> i32 {
    let mut max_area = 0;
    // Iterate through each height to calculate the area of the rectangle possible with each height.
    for i in 0..heights.len() {
        max_area = cmp::max(max_area, heights[i] * (right[i] - left[i]) as i32);
    }
    max_area
}

/// Function to precompute the limits for each element.
/// `heights`: array of heights.
/// Returns tuples of `left` and `right` arrays:
/// - `left[i]`: index of the nearest smaller element to the left of `i`.
/// - `right[i]`: index of the nearest smaller element to the right of `i`.
fn precompute_limits(heights: &Vec<i32>) -> (Vec<usize>, Vec<usize>) {
    let n = heights.len();
    let mut left = vec![0; n];
    let mut right = vec![n; n];
    let mut stack: Vec<usize> = Vec::new();

    // Calculate nearest smaller element to the left for each element.
    for i in 0..n {
        while let Some(&last) = stack.last() {
            if heights[last] >= heights[i] {
                stack.pop(); // Pop elements from the stack until we find a smaller height.
            } else {
                break;
            }
        }
        left[i] = if stack.is_empty() { 0 } else { stack.last().unwrap() + 1 }; // Set left limit for the current element.
        stack.push(i); // Push the current index onto the stack.
    }

    stack.clear(); // Clear the stack for reuse.

    // Calculate nearest smaller element to the right for each element.
    for i in (0..n).rev() {
        while let Some(&last) = stack.last() {
            if heights[last] >= heights[i] {
                stack.pop(); // Pop elements from the stack until we find a smaller height.
            } else {
                break;
            }
        }
        right[i] = if stack.is_empty() { n } else { *stack.last().unwrap() }; // Set right limit for the current element.
        stack.push(i); // Push the current index onto the stack.
    }

    (left, right) // Return the left and right limit arrays.
}

/// Function to calculate the maximum possible area of a rectangle after modifying at most one element.
/// `a`: initial array of heights.
/// `x`: maximum value that can be assigned to any element in the array.
fn max_area_with_one_change(a: Vec<i32>, x: i32) -> i32 {
    let n = a.len();
    let (left, right) = precompute_limits(&a);

    // Calculate the maximum area without any modifications.
    let mut max_area = largest_rectangle_area(&a, &left, &right);

    // Find the index that is most limiting the maximum area.
    let mut limiting_index = 0;
    for i in 0..n {
        let area = a[i] * (right[i] - left[i]) as i32;
        if area < max_area {
            limiting_index = i; // Identify the element that limits the area.
            break;
        }
    }

    // Attempt to modify the most limiting element to the maximum value `x`.
    let mut modified_a = a.clone();
    modified_a[limiting_index] = x;
    let (new_left, new_right) = precompute_limits(&modified_a);
    // Calculate the new maximum area with the modified array.
    max_area = cmp::max(max_area, largest_rectangle_area(&modified_a, &new_left, &new_right));

    max_area
}

fn main() {
    let mut input = String::new();
    // Read the first line of input to get `n` (number of elements) and `x` (maximum value).
    io::stdin().read_line(&mut input).unwrap();
    let mut parts = input.trim().split_whitespace();
    let n: usize = parts.next().unwrap().parse().unwrap();
    let x: i32 = parts.next().unwrap().parse().unwrap();

    input.clear();
    // Read the second line of input to get the array of heights `a`.
    io::stdin().read_line(&mut input).unwrap();
    let a: Vec<i32> = input
        .trim()
        .split_whitespace()
        .map(|s| s.parse().unwrap())
        .collect();

    // Calculate and print the result.
    println!("{}", max_area_with_one_change(a, x));
}
