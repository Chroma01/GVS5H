
## ideation
```python
import sys

def fwht(a):
    """In‑place Fast Walsh–Hadamard Transform (XOR version)."""
    n = len(a)
    step = 1
    while step < n:
        for i in range(0, n, step << 1):
            for j in range(i, i + step):
                u = a[j]
                v = a[j + step]
                a[j] = u + v
                a[j + step] = u - v
        step <<= 1

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    N = 1 << W

    freq = [0] * N
    for _ in range(H):
        s = next(it).decode()
        mask = 0
        for j, ch in enumerate(s):
            if ch == '1':
                mask |= 1 << j
        freq[mask] += 1

    # f[mask] = min(popcount(mask), W - popcount(mask))
    f = [0] * N
    for mask in range(N):
        p = mask.bit_count()
        f[mask] = p if p <= W - p else W - p

    # XOR‑convolution of freq and f via FWHT
    a = freq[:]
    b = f[:]
    fwht(a)
    fwht(b)
    for i in range(N):
        a[i] = a[i] * b[i]
    fwht(a)              # inverse transform (same routine)
    n_inv = N
    for i in range(N):
        a[i] //= n_inv    # normalisation

    ans = min(a)
    print(ans)

if __name__ == "__main__":
    solve()
```

## worker: finalize
The solution exploits the commutativity of row and column flips: only the parity of flips matters.  
For a fixed column mask `C`, each row with original mask `M` contributes `min(popcount(M xor C), W - popcount(M xor C))` after optimal row flipping. Summing over all rows yields a XOR‑convolution of the frequency array of row masks with the function `f(mask) = min(popcount(mask), W - popcount(mask))`.  
This convolution is evaluated in `O(2^W * W)` time using the Fast Walsh–Hadamard Transform (FWHT). The final answer is the minimum value over all column masks.

Complexities:  
- Time: `O(H·W + 2^W·W)` ( ≤ ~5·10⁶ operations for `W = 18`).  
- Memory: `O(2^W)` integers ( ≤ 262 144 entries).

The algorithm is proven correct in the detailed proof provided in the plan.
