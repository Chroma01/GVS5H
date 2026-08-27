
## ideation
```python
import sys

def main():
    MOD = 998244353
    N = int(sys.stdin.readline())
    s = sys.stdin.readline().strip()
    k = s.count('1')
    # Count connected components of 1's in s (cyclically)
    if k == 0:
        components = 0
    else:
        components = 0
        prev = '0'
        for c in s:
            if c == '1' and prev == '0':
                components += 1
            prev = c
        if s[-1] == '1' and s[0] == '1':
            components -= 1  # Because it's a cycle, merge first and last if both are 1
    # Formula: 2^N * 2^k - 2^{N-1} * 2^{k-1} * components
    pow2_N = pow(2, N, MOD)
    pow2_N_minus1 = pow(2, N-1, MOD) if N > 0 else 0
    pow2_k = pow(2, k, MOD)
    pow2_k_minus1 = pow(2, k-1, MOD) if k > 0 else 0
    ans = (pow2_N * pow2_k - pow2_N_minus1 * pow2_k_minus1 * components) % MOD
    print(ans)

if __name__ == "__main__":
    main()
```
