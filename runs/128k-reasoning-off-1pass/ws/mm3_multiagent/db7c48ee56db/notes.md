
## ideation
### TASKS
- [ ] Parse input: `N`, `K`, and array `A`.
- [ ] If `K == 1`, output `max(A)` and return.
- [ ] If `K == N`, output XOR of all elements and return.
- [ ] Initialize combination indices `comb = [0, 1, ..., K-1]`.
- [ ] Loop until all combinations are processed:
  - Compute XOR of `A[comb[0]], ..., A[comb[K-1]]`.
  - Update maximum XOR if current is larger.
  - Generate the next combination using the standard algorithm: find the rightmost index `i` that can be incremented, increment it, and set subsequent indices to consecutive values. If no such `i` exists, break.
- [ ] Print the maximum XOR found.

```python
import sys

def solve():
    import sys
    input = sys.stdin.readline
    N, K = map(int, input().split())
    A = list(map(int, input().split()))
    
    if K == 1:
        print(max(A))
        return
    if K == N:
        xor_all = 0
        for a in A:
            xor_all ^= a
        print(xor_all)
        return
    
    comb = list(range(K))
    max_xor = 0
    while True:
        cur_xor = 0
        for idx in comb:
            cur_xor ^= A[idx]
        if cur_xor > max_xor:
            max_xor = cur_xor
        # Generate next combination
        i = K - 1
        while i >= 0 and comb[i] == N - K + i:
            i -= 1
        if i < 0:
            break
        comb[i] += 1
        for j in range(i + 1, K):
            comb[j] = comb[j-1] + 1
            
    print(max_xor)

if __name__ == "__main__":
    solve()
```
