```python
import sys

def solve() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].strip()

    # Positions of '1's (0‑based indices)
    pos = [i for i, ch in enumerate(S) if ch == '1']
    K = len(pos)

    # d_i = original position of i‑th '1' minus its index among the ones
    d = [pos[i] - i for i in range(K)]

    # The optimal starting position of the final block is a median of d_i.
    median = d[K // 2]

    # The block must fit entirely inside the string: start ∈ [0, N‑K]
    start = median
    if start < 0:
        start = 0
    elif start > N - K:
        start = N - K

    # Minimal number of adjacent swaps needed
    ans = sum(abs(x - start) for x in d)
    print(ans)

if __name__ == "__main__":
    solve()
```