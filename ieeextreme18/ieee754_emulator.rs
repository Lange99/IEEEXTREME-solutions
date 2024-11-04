// IEEE754 Emulator -> 70% of the test cases passed
// Time limit: 2000 ms
// Memory limit: 512 MB
//
// The IEEE 754 single-precision floating-point format is a 32-bit binary format that represents real numbers.
// These 32 bits are divided into three distinct parts:
//
// 1. Sign bit (1 bit):
//    - The first bit (bit 31) indicates the sign of the number.
//    - 0 means the number is positive, 1 means the number is negative.
//
// 2. Exponent (8 bits):
//    - The next 8 bits (bits 30 to 23) represent the exponent in a "biased" format, with a bias of 127.
//    - The actual exponent is calculated as: exponent = (exponent bits value) - 127.
//
// 3. Fraction (mantissa) (23 bits):
//    - The last 23 bits (bits 22 to 0) represent the fraction (mantissa).
//    - The IEEE 754 format assumes a "normalized" representation where the leading bit is 1 and is not stored.
//    - Therefore, the actual value of the mantissa is: 1 + fraction bits.
//
// The floating-point value is computed as:
//    (-1)^sign * 2^(exponent - 127) * (1 + mantissa).
//
// Commands to simulate include:
// - Look-Up Table (LUT): Retrieves a stored value from a LUT based on bits from C[0].
// - NAND Gate: Computes the bitwise NAND of two stored values.
// - Fused Multiply-Add (FMA): Computes a * b + c with only one rounding step, improving precision.
// - Constant Declaration: Stores a specified hexadecimal constant.
//
// The input consists of multiple test cases. For each test case, we:
// - Start with an initial hexadecimal value C[0].
// - Execute commands using values stored in C and predefined LUTs.
//
// Standard Input:
// - First line: an integer T, the number of test cases.
// - For each test case:
//   - First line: hexadecimal value C[0], representing a 32-bit IEEE 754 float.
//   - Second line: an integer L, the number of LUTs to read.
//   - Next L lines: each contains an integer 2^k_i followed by 2^k_i hexadecimal values for a LUT.
//   - Next line: an integer Q, the number of commands to execute.
//   - Next Q lines: each line contains a command:
//     - L i j b: Store the corresponding LUT result. Guaranteed that 0 ≤ i < L, 0 ≤ j ≤ j + b - 1 < 32, and b ≤ k_i.
//     - N i j: Store the bitwise NAND of C[i] and C[j].
//     - F i j k: Store the FMA result C[i] * C[j] + C[k].
//     - C h: Store the specified hexadecimal value.
//
// Standard Output:
// - For each test case, output the result of the last command executed.
//
// Constraints and Notes:
// - 1 ≤ T ≤ 10^5
// - 1 ≤ ∑ Q_i ≤ 10^5 across all test cases (total commands across all test cases ≤ 10^5).
// - Sum of sizes of LUTs across test cases does not exceed 10^5.


use std::io::{self, BufRead};
use std::str::FromStr;

// Step 1: Extract sign, exponent, and fraction from a 32-bit hexadecimal value
fn extract_ieee754(hex_value: u32) -> (u8, i32, f32) {
    let sign_bit = (hex_value >> 31) & 1;
    let exponent_bits = ((hex_value >> 23) & 0xFF) as i32;
    let fraction_bits = hex_value & 0x7FFFFF;

    let fraction = if exponent_bits == 0 {
        // Denormalized number
        (fraction_bits as f32) / (2.0_f32.powi(23))
    } else {
        // Normalized number
        1.0 + (fraction_bits as f32) / (2.0_f32.powi(23))
    };

    let exponent = exponent_bits - 127;

    (sign_bit as u8, exponent, fraction)
}

// Step 2: Convert extracted components to a floating-point number
fn ieee754_to_float(sign: u8, exponent: i32, fraction: f32) -> f32 {
    let sign_multiplier = if sign == 0 { 1.0 } else { -1.0 };
    sign_multiplier * 2.0_f32.powi(exponent) * fraction
}

// Step 3: Perform LUT command
fn lut_command(C0: u32, lut: &Vec<u32>, j: u8, b: u8) -> u32 {
    let extracted_bits = (C0 >> j) & ((1 << b) - 1);
    if let Some(&value) = lut.get(extracted_bits as usize) {
        value
    } else {
        0
    }
}

// Step 4: Perform NAND command
fn nand_command(C: &Vec<u32>, i: usize, j: usize) -> u32 {
    if i >= C.len() || j >= C.len() {
        0
    } else {
        !(C[i] & C[j]) & 0xFFFFFFFF
    }
}

// Step 5: Perform FMA command
fn fma_command(C: &Vec<u32>, i: usize, j: usize, k: usize) -> u32 {
    if i >= C.len() || j >= C.len() || k >= C.len() {
        return 0;
    }
    let (sign_a, exp_a, frac_a) = extract_ieee754(C[i]);
    let (sign_b, exp_b, frac_b) = extract_ieee754(C[j]);
    let (sign_c, exp_c, frac_c) = extract_ieee754(C[k]);

    let a = ieee754_to_float(sign_a, exp_a, frac_a);
    let b = ieee754_to_float(sign_b, exp_b, frac_b);
    let c = ieee754_to_float(sign_c, exp_c, frac_c);

    let result = a.mul_add(b, c); // Perform fused multiply-add

    float_to_ieee754(result)
}

// Step 6: Convert a floating-point number to IEEE 754 representation
fn float_to_ieee754(value: f32) -> u32 {
    value.to_bits()
}

// Step 7: Perform constant command
fn constant_command(h: &str) -> u32 {
    u32::from_str_radix(h, 16).unwrap_or(0)
}

// Main function to read input, execute commands, and produce output
fn main() {
    let stdin = io::stdin();
    let mut iterator = stdin.lock().lines();

    let test_case_number = iterator.next().unwrap().unwrap().parse::<usize>().unwrap();
    let mut results = Vec::new();

    for _ in 0..test_case_number {
        let C0_hex = iterator.next().unwrap().unwrap();
        let C0 = u32::from_str_radix(&C0_hex, 16).unwrap_or(0);
        let mut C = vec![C0];

        let L = iterator.next().unwrap().unwrap().parse::<usize>().unwrap();
        let mut LUTs = Vec::new();

        for _ in 0..L {
            let line = iterator.next().unwrap().unwrap();
            let parts: Vec<&str> = line.split_whitespace().collect();
            let k = usize::from_str(parts[0]).unwrap();
            let entries = parts[1..]
                .iter()
                .map(|&x| u32::from_str_radix(x, 16).unwrap())
                .collect::<Vec<u32>>();
            LUTs.push(entries);
        }

        let Q = iterator.next().unwrap().unwrap().parse::<usize>().unwrap();

        for _ in 0..Q {
            let command_line = iterator.next().unwrap().unwrap();
            let command_parts: Vec<&str> = command_line.split_whitespace().collect();
            let command = command_parts[0];

            match command {
                "L" => {
                    let i = command_parts[1].parse::<usize>().unwrap();
                    let j = command_parts[2].parse::<u8>().unwrap();
                    let b = command_parts[3].parse::<u8>().unwrap();
                    if i < LUTs.len() {
                        let result = lut_command(C[0], &LUTs[i], j, b);
                        C.push(result);
                    } else {
                        C.push(0);
                    }
                }
                "N" => {
                    let i = command_parts[1].parse::<usize>().unwrap();
                    let j = command_parts[2].parse::<usize>().unwrap();
                    let result = nand_command(&C, i, j);
                    C.push(result);
                }
                "F" => {
                    let i = command_parts[1].parse::<usize>().unwrap();
                    let j = command_parts[2].parse::<usize>().unwrap();
                    let k = command_parts[3].parse::<usize>().unwrap();
                    let result = fma_command(&C, i, j, k);
                    C.push(result);
                }
                "C" => {
                    let hex_value = command_parts[1];
                    let result = constant_command(hex_value);
                    C.push(result);
                }
                _ => {}
            }
        }

        results.push(format!("{:08x}", C.last().unwrap()));
    }



    for result in results {
        println!("{}", result);
    }
}
