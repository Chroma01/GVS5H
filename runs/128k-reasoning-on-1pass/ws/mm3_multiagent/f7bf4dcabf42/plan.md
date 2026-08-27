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

    # prefix counts for each mask: cnt[mask][i] = number of matched positions among first i characters of S
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
            # newcnt[0] = 0
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