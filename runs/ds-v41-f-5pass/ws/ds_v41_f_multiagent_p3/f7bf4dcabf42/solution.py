import sys

def main():
    input_data = sys.stdin.read().split()
    N = int(input_data[0])
    M = int(input_data[1])
    S = input_data[2]
    MOD = 998244353

    # Encode state as N-bit mask: bit (i-1) is 1 if dp[i]-dp[i-1] == 1.
    # dp[0] = 0 always.  dp[i] = popcount of lower i bits.
    def transition(mask, c):
        # rebuild old row
        dp = [0] * (N + 1)
        for i in range(1, N + 1):
            dp[i] = dp[i - 1] + ((mask >> (i - 1)) & 1)
        ndp = [0] * (N + 1)
        for i in range(1, N + 1):
            v = dp[i]
            if ndp[i - 1] > v:
                v = ndp[i - 1]
            if S[i - 1] == c:
                t = dp[i - 1] + 1
                if t > v:
                    v = t
            ndp[i] = v
        nmask = 0
        for i in range(1, N + 1):
            if ndp[i] != ndp[i - 1]:
                nmask |= (1 << (i - 1))
        return nmask

    distinct = set(S)
    letters = list(distinct)
    other_count = 26 - len(distinct)

    # Precompute transitions for distinct letters
    trans_distinct = {}
    for c in letters:
        trans_distinct[c] = {}

    states_count = 1 << N
    # Build transition table lazily via dictionary cache
    cache = {}
    def get_trans(mask, c):
        key = (mask, c)
        r = cache.get(key)
        if r is None:
            r = transition(mask, c)
            cache[key] = r
        return r

    # Precompute all transitions we will need: for masks reachable
    # We'll just compute on the fly with memo.
    other_key = '\x00'  # representative for letters not in S
    def get_other_trans(mask):
        key = (mask, other_key)
        r = cache.get(key)
        if r is None:
            # any char not in S behaves identically
            nmask = 0
            dp = [0] * (N + 1)
            for i in range(1, N + 1):
                dp[i] = dp[i - 1] + ((mask >> (i - 1)) & 1)
            ndp = [0] * (N + 1)
            for i in range(1, N + 1):
                v = dp[i]
                if ndp[i - 1] > v:
                    v = ndp[i - 1]
                ndp[i] = v
            for i in range(1, N + 1):
                if ndp[i] != ndp[i - 1]:
                    nmask |= (1 << (i - 1))
            r = nmask
            cache[key] = r
        return r

    # DP over length M
    # cur[mask] = number of strings so far reaching that row-state
    cur = {0: 1}
    for _ in range(M):
        nxt = {}
        for mask, cnt in cur.items():
            # distinct letters
            for c in letters:
                nm = get_trans(mask, c)
                nxt[nm] = (nxt.get(nm, 0) + cnt) % MOD
            # other letters grouped
            if other_count > 0:
                nm = get_other_trans(mask)
                nxt[nm] = (nxt.get(nm, 0) + cnt * other_count) % MOD
        cur = nxt

    ans = [0] * (N + 1)
    for mask, cnt in cur.items():
        k = bin(mask).count('1')
        ans[k] = (ans[k] + cnt) % MOD

    print(' '.join(str(x % MOD) for x in ans))

main()