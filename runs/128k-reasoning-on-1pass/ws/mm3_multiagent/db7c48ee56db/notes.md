
## ideation
```python
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]
    total_xor = 0
    for a in A:
        total_xor ^= a
    # Enumerate the smaller side of the subsets
    k = K if K <= N - K else N - K
    if k == 0:
        print(total_xor)
        return
    sys.setrecursionlimit(1000000)
    ans_holder = [0]
    N_local = N
    A_local = A
    total_xor_local = total_xor
    k_local = k
    K_local = K

    def dfs(start, depth, cur_xor):
        if depth == k_local:
            cand = cur_xor if k_local == K_local else total_xor_local ^ cur_xor
            if cand > ans_holder[0]:
                ans_holder[0] = cand
            return
        remaining = k_local - depth
        # The next chosen index can be at most N - remaining
        for i in range(start, N_local - remaining + 1):
            dfs(i + 1, depth + 1, cur_xor ^ A_local[i])

    dfs(0, 0, 0)
    print(ans_holder[0])

if __name__ == "__main__":
    solve()
```

## worker: finalize
- The problem guarantees \(\binom{N}{K} \le 10^6\), so the total number of \(K\)-element subsets is at most one million.  
- To reduce the work we always enumerate the *smaller* side of each subset: let \(k = \min(K, N-K)\).  
  * If \(K \le N-K\) (i.e., \(k = K\)), each subset of size \(k\) is exactly a valid choice, and its XOR is simply the XOR of its elements.  
  * If \(K > N-K\) (i.e., \(k = N-K\)), we enumerate the complement of a valid set. For a complement subset \(S\) of size \(k\), the XOR of the original \(K\) elements equals \(\text{totalXor} \oplus \bigoplus_{x \in S} x\), where \(\text{totalXor}\) is the XOR of all numbers.  
- A depth‑first search builds the subsets one element at a time, carrying the current XOR. When a full subset of size \(k\) is formed we update the global maximum.  
- The recursion depth never exceeds \(k\). Since \(\binom{N}{k} \le 10^6\) and \(k \le 23\) (the largest value with \(\binom{N}{k} \le 10^6\)), the depth is tiny.  
- Time complexity: \(O\!\bigl(\binom{N}{k}\cdot k\bigr) \le 2.3\times10^7\) elementary operations – well within limits.  
- Memory consumption is \(O(N)\) for the input array.
