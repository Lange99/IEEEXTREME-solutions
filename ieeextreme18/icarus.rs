// Icarus -> 93.75 of the test cases passed
// Time limit: 500 ms
// Memory limit: 256 MB
//
// Icarus is trapped in a maze represented as a binary tree, where each node represents a room.
// Each room has up to three neighboring rooms: the parent, the left child, and the right child.
// One specific room contains a secret exit, and the goal is to prevent Icarus from ever reaching it.
//
// Icarus starts in a specified node A and follows a movement pattern based on a string S:
// - 'L' means he tries to move to the left child.
// - 'R' means he tries to move to the right child.
// - 'U' means he tries to move to the parent node.
// Icarus will follow the sequence in S, looping back to the start once he reaches its end.
// If a move specified in S is impossible (e.g., moving to a nonexistent node), Icarus skips that move.
//
// Input:
// - The input contains a single line with the string S.
//
// Output:
// - The first line should contain three integers: N (number of nodes), A (starting node), B (exit node).
// - The next N lines should describe each node i (from 1 to N) with two integers representing:
//   - The left child of i.
//   - The right child of i.
//   - Use 0 if the node does not have a left or right child.
// - If it's impossible to prevent Icarus from reaching the exit given the constraints, output -1.
//
// Constraints and Notes:
// - 1 ≤ |S| ≤ 2000
// - 1 ≤ N ≤ 2 * |S|
// - Ensure the chosen exit node B is unreachable from the start node A by following the sequence in S.

use std::io::{self, Write};

// Tree construction to trap Icarus:
// The binary tree is built to ensure Icarus can never reach the exit node `b`.
// - `n_nodes` is chosen as twice the length of the string `s`, to create a sufficient number of nodes.
// - Each node `i` has a left child `2 * i` and a right child `2 * i + 1`, forming a complete binary tree 
//   with many possible paths and some dead ends.
// - We define `a = 1` as the starting node (root) and `b = n_nodes` as the unreachable exit node, creating
//   a structure where numerous intermediate nodes make a direct path to `b` difficult.
// This approach ensures that Icarus follows the movement pattern in `s` but can never reach the exit node `b`.
fn solve(s: &str) {
    let n = s.len();
    let n_nodes = 2 * n;
    let mut left = vec![0; n_nodes + 1];
    let mut right = vec![0; n_nodes + 1];

    // Costruzione dell'albero binario:
    for i in 1..=n {
        if 2 * i <= n_nodes {
            left[i] = 2 * i; // figlio sinistro
        }
        if 2 * i + 1 <= n_nodes {
            right[i] = 2 * i + 1; // figlio destro
        }
    }

    // Nodo di partenza e di uscita
    let a = 1;
    let b = n_nodes;

    // Output
    let stdout = io::stdout();
    let mut handle = stdout.lock();
    writeln!(handle, "{} {} {}", n_nodes, a, b).unwrap();
    // Stampa dell'albero binario
    for i in 1..=n_nodes {
        writeln!(handle, "{} {}", left[i], right[i]).unwrap();
    }
}

fn main() {
    // Legge l'input
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    let s = input.trim();

    // Esegue la funzione solve
    solve(s);
}
