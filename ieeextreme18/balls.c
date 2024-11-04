/*
Balls -> 26% of test cases passed.
Time limit: 2000 ms
Memory limit: 256 MB

Josh has N tiles arranged in a row, numbered from 1 to N. He also has K balls, each with a property called elasticity.
When Josh throws a ball with elasticity E[i], it will hit tiles at positions E[i], 2*E[i], 3*E[i], and so on, until it exceeds N.

The task is to calculate how many tiles will be hit at least once when all K balls are thrown simultaneously.

Input:
- The first line contains two integers N (number of tiles) and K (number of balls).
- The second line contains K integers, representing the elasticity of each ball.

Output:
- Output a single integer representing the number of tiles that will be hit at least once.

Constraints and Notes:
- 1 ≤ N ≤ 10^14
- 1 ≤ K ≤ 100
- 1 ≤ E[i] ≤ 1000
- The greatest common divisor of any two elasticities is 1 (i.e., gcd(E[i], E[j]) = 1 for all i ≠ j), ensuring
  that their hit patterns on the tiles are independent and do not perfectly overlap.
*/

#include <stdio.h>
#include <stdlib.h>

long long gcd(long long a, long long b) {
    while (b != 0) {
        long long t = b;
        b = a % b;
        a = t;
    }
    return a;
}

long long lcm(long long a, long long b) {
    return a / gcd(a, b) * b;
}

long long count_multiples(long long N, long long x) {
    return N / x;
}

long long count_tiles(long long N, long long K, long long *E) {
    long long count = 0;

    // Inclusione
    for (long long i = 1; i < (1 << K); i++) {
        long long lcm_value = 1;
        int bits = 0;

        for (long long j = 0; j < K; j++) {
            if (i & (1 << j)) {
                lcm_value = lcm(lcm_value, E[j]);
                bits++;
                if (lcm_value > N) break; // Se il LCM supera N, non ha senso continuare
            }
        }

        if (lcm_value > N) continue;

        if (bits % 2 == 1) {
            count += count_multiples(N, lcm_value);
        } else {
            count -= count_multiples(N, lcm_value);
        }
    }

    return count;
}

int main() {
    long long N;
    long long K;
    if (scanf("%lld %lld", &N, &K) != 2) {
        fprintf(stderr, "Error reading input for N and K\n");
        return 1;
    }

    long long *E = (long long *)malloc(K * sizeof(long long));
    if (E == NULL) {
        fprintf(stderr, "Memory allocation failed for E array\n");
        return 1;
    }

    for (long long i = 0; i < K; i++) {
        if (scanf("%lld", &E[i]) != 1) {
            fprintf(stderr, "Error reading input for E[%lld]\n", i);
            free(E);
            return 1;
        }
    }

    printf("%lld\n", count_tiles(N, K, E));

    free(E);
    return 0;
}
