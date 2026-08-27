
## ideation
```python
import sys

MOD = 998244353

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    S = data[2].strip()
    S_int = [ord(c) - 97 for c in S]
    size = 1 << N

    # cnt[mask][i] = number of matched positions among first i characters of S
    cnt = [[0] * (N + 1) for _ in range(size)]
    for mask in range(size):
        c = 0
        for i in range(N):
            if mask >> i & 1:
                c += 1
            cnt[mask][i + 1] = c

    # transition table: trans[mask][c] = new mask after appending character c (0..25)
    trans = [[0] * 26 for _ in range(size)]
    for mask in range(size):
        for ch in range(26):
            newcnt = [0] * (N + 1)
            for i in range(1, N + 1):
                old_i = cnt[mask][i]
                val = old_i
                if val < newcnt[i - 1]:
                    val = newcnt[i - 1]
                if S_int[i - 1] == ch:
                    cand = cnt[mask][i - 1] + 1
                    if cand > val:
                        val = cand
                newcnt[i] = val
            new_mask = 0
            for i in range(1, N + 1):
                if newcnt[i] == newcnt[i - 1] + 1:
                    new_mask |= (1 << (i - 1))
            trans[mask][ch] = new_mask

    f = [0] * size
    f[0] = 1
    for _ in range(M):
        new_f = [0] * size
        for mask in range(size):
            if f[mask] == 0:
                continue
            val = f[mask]
            row = trans[mask]
            for ch in range(26):
                new_mask = row[ch]
                new_f[new_mask] = (new_f[new_mask] + val) % MOD
        f = new_f

    ans = [0] * (N + 1)
    for mask in range(size):
        k = mask.bit_count()
        ans[k] = (ans[k] + f[mask]) % MOD

    print(' '.join(str(ans[i]) for i in range(N + 1)))

if __name__ == "__main__":
    solve()
```

## worker: finalize
The algorithm uses a deterministic automaton whose states are subsets (bitmasks) of the positions of `S` that have already been matched in the longest common subsequence (LCS) of the current prefix of `T` and `S`.  
- For a state `mask` and a next character `c`, the transition `trans[mask][c]` is computed by the standard LCS DP on the prefixes.  
  `cnt[mask][i]` stores how many positions among the first `i` characters of `S` are already matched (i.e. the LCS length for the prefix `S[:i]`).  
  The DP recurrence `newcnt[i] = max(old_i, newcnt[i-1], (S[i-1]==c) ? cnt[mask][i-1]+1)` yields the new LCS lengths, and a bit is set in the new mask exactly where the length increases.  
- Starting with the empty string (mask `0`), we simulate the construction of all strings `T` of length `M` by applying the transition for each of the `M` positions. Because each character is processed independently, every possible string is counted exactly once.  
- After `M` steps, the value `f[mask]` is the number of strings whose final matched set is `mask`. The LCS length of such a string equals the number of set bits in `mask`. Summing `f[mask]` over masks with the same bit‑count gives the required answer for each `k`.  

Complexities:  
- Precomputation of `trans`: `O(2^N · 26 · N)`.  
- DP over the length `M`: `O(M · 2^N · 26)`.  
With `N ≤ 10` and `M ≤ 100` this easily fits in time. Memory usage is `O(2^N)` (a few thousand integers).
