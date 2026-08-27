
## ideation
```python
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    
    # Compute nxt[i] = smallest j > i with A[j] >= 2*A[i], or N if none
    nxt = [N] * N
    d = [0] * N
    j = N
    for i in range(N-1, -1, -1):
        ai = A[i]
        # Move j leftwards while the element just before j is large enough
        while j > i+1 and A[j-1] >= 2 * ai:
            j -= 1
        if j < N and A[j] >= 2 * ai:
            nxt[i] = j
        else:
            nxt[i] = N
        d[i] = nxt[i] - i
    
    # Build sparse table for range maximum queries on d
    LOG = (N).bit_length()
    st = [d[:]]
    for k in range(1, LOG):
        prev = st[k-1]
        length = N - (1 << k) + 1
        if length <= 0:
            break
        curr = [0] * length
        half = 1 << (k-1)
        for i in range(length):
            a = prev[i]
            b = prev[i + half]
            curr[i] = a if a > b else b
        st.append(curr)
    
    # Precompute logs for RMQ
    logs = [0] * (N + 1)
    for i in range(2, N+1):
        logs[i] = logs[i // 2] + 1
    
    def range_max(l, r):
        """Return max of d[l..r] (inclusive)."""
        length = r - l + 1
        k = logs[length]
        a = st[k][l]
        b = st[k][r - (1 << k) + 1]
        return a if a > b else b
    
    Q = int(next(it))
    out = []
    for _ in range(Q):
        L = int(next(it)) - 1
        R = int(next(it)) - 1
        M = R - L + 1
        lo = 0
        hi = M // 2
        while lo < hi:
            mid = (lo + hi + 1) // 2
            # Check if we can make mid kagamimochi using mochi L..L+mid-1 as small ones
            max_d = range_max(L, L + mid - 1)
            if max_d <= M - mid:
                lo = mid
            else:
                hi = mid - 1
        out.append(str(lo))
    
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
```
