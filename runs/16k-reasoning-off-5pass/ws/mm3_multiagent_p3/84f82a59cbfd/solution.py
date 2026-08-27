import sys
import math

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    Q = int(data[0])
    A_list = list(map(int, data[1:1+Q]))
    
    # Maximum sqrt value needed
    MAX_SQRT = 10**6
    
    # Sieve to count distinct prime factors
    # f[i] = number of distinct prime factors of i
    f = [0] * (MAX_SQRT + 1)
    
    # We can use a modified sieve: for each prime p, for multiples of p, increment f[multiple]
    # But to find primes efficiently, we can do standard sieve first, then iterate over primes.
    is_prime = [True] * (MAX_SQRT + 1)
    is_prime[0] = is_prime[1] = False
    primes = []
    for i in range(2, MAX_SQRT + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i*i, MAX_SQRT + 1, i):
                is_prime[j] = False
                # This inner loop is for sieve, not for counting f
    # Actually we can combine: for each prime p, for multiples of p, add 1 to f
    # But we need f to count distinct primes; we can do:
    f = [0] * (MAX_SQRT + 1)
    for p in primes:
        for j in range(p, MAX_SQRT + 1, p):
            f[j] += 1
    
    # Build best[i] = largest number <= i that has exactly 2 distinct prime factors, or 0 if none
    best = [0] * (MAX_SQRT + 1)
    current_best = 0
    for i in range(1, MAX_SQRT + 1):
        if f[i] == 2:
            current_best = i
        best[i] = current_best
    
    out_lines = []
    for A in A_list:
        S = math.isqrt(A)
        r = best[S]
        # Problem guarantees r exists, but for safety:
        if r == 0:
            # find next r > S? But problem says it exists, so this shouldn't happen.
            # Just in case, find the smallest with 2 prime factors >= 6
            r = 6  # 2*3
        out_lines.append(str(r * r))
    
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()