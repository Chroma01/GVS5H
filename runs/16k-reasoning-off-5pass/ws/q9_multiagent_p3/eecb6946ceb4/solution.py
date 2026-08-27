import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        S = []
        for _ in range(N):
            S.append(int(next(iterator)))
    except StopIteration:
        return

    if N < 3:
        print(0)
        return

    # Find the maximum value to determine the size of the polynomial
    max_val = 0
    for x in S:
        if x > max_val:
            max_val = x
    
    # The maximum sum of two elements is 2 * max_val
    # We need a size that is a power of 2 and greater than 2 * max_val
    limit = 2 * max_val
    size = 1
    while size <= limit:
        size *= 2
    
    # Create the frequency array (polynomial coefficients)
    # cnt[i] = 1 if i is in S, else 0
    cnt = [0] * size
    for x in S:
        cnt[x] = 1

    # Constants for NTT
    MOD = 998244353
    G = 3

    def power(a, b, m):
        res = 1
        a %= m
        while b > 0:
            if b % 2 == 1:
                res = (res * a) % m
            a = (a * a) % m
            b //= 2
        return res

    def inverse(a, m):
        return power(a, m - 2, m)

    def ntt(a, invert):
        n = len(a)
        j = 0
        for i in range(1, n):
            bit = n >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j ^= bit
            if i < j:
                a[i], a[j] = a[j], a[i]
        
        length = 2
        while length <= n:
            wlen = power(G, (MOD - 1) // length, MOD)
            if invert:
                wlen = inverse(wlen, MOD)
            
            w = 1
            for i in range(0, n, length):
                for j in range(i, i + length // 2):
                    u = a[j]
                    v = (a[j + length // 2] * w) % MOD
                    a[j] = (u + v) % MOD
                    a[j + length // 2] = (u - v) % MOD
                w = (w * wlen) % MOD
            length <<= 1

    # Perform NTT on cnt
    ntt(cnt, False)
    
    # Square the polynomial (point-wise multiplication)
    for i in range(size):
        cnt[i] = (cnt[i] * cnt[i]) % MOD
        
    # Perform Inverse NTT
    ntt(cnt, True)
    
    # Calculate the answer
    ans = 0
    for x in S:
        target = 2 * x
        if target < size:
            count = cnt[target]
            # count is the number of ordered pairs (A, C) such that A + C = 2*B
            # Since A != C (distinct elements), pairs are (A,C) and (C,A).
            # We divide by 2 to count unique sets {A, C}.
            ans = (ans + count // 2) % MOD
            
    print(ans)

if __name__ == '__main__':
    solve()