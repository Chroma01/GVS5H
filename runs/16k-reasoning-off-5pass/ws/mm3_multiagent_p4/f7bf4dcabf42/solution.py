import sys

MOD = 998244353

def solve():
    import sys
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    it = iter(input_data)
    N = int(next(it))
    M = int(next(it))
    S = next(it).strip()
    # Precompute transition table
    size = 1 << N
    trans = [[0] * 26 for _ in range(size)]
    # For each mask, compute cur array
    for mask in range(size):
        # cur[i] = number of set bits among first i bits (i from 0..N)
        cur = [0] * (N + 1)
        # cur[0] = 0
        # cur[i] = cur[i-1] + (bit i-1)
        for i in range(1, N + 1):
            bit = (mask >> (i - 1)) & 1
            cur[i] = cur[i - 1] + bit
        # For each character
        for c_idx in range(26):
            c = chr(ord('a') + c_idx)
            # Compute newcur after appending character c
            newcur = [0] * (N + 1)
            # newcur[0] = 0
            # iterate i = 1..N
            # We need newcur[i-1] for the current i, so compute sequentially
            # Use the recurrence: newcur[i] = max(oldcur[i], newcur[i-1], oldcur[i-1] + match)
            for i in range(1, N + 1):
                old_i = cur[i]
                old_i_1 = cur[i - 1]
                prev_new = newcur[i - 1]
                match = 1 if S[i - 1] == c else 0
                # newcur[i] is the max of three values
                # Since newcur[i-1] >= oldcur[i-1], the max is at least prev_new
                # But we compute explicitly
                cand1 = old_i
                cand2 = prev_new
                cand3 = old_i_1 + match
                # max of three
                newcur[i] = cand1
                if cand2 > newcur[i]:
                    newcur[i] = cand2
                if cand3 > newcur[i]:
                    newcur[i] = cand3
            # Build new mask from newcur differences
            new_mask = 0
            for i in range(1, N + 1):
                if newcur[i] > newcur[i - 1]:
                    new_mask |= (1 << (i - 1))
            trans[mask][c_idx] = new_mask

    # DP over length M
    dp = [0] * size
    dp[0] = 1
    for _ in range(M):
        newdp = [0] * size
        for mask in range(size):
            val = dp[mask]
            if val == 0:
                continue
            # iterate over all 26 letters
            tr = trans[mask]
            # local variable for speed
            for c_idx in range(26):
                nmask = tr[c_idx]
                newdp[nmask] = (newdp[nmask] + val) % MOD
        dp = newdp

    # Compute answers
    ans = [0] * (N + 1)
    for mask in range(size):
        k = bin(mask).count('1')
        ans[k] = (ans[k] + dp[mask]) % MOD

    # Output
    print(' '.join(str(ans[i]) for i in range(N + 1)))

if __name__ == "__main__":
    solve()