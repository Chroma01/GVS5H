import sys

MOD = 998244353

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    S = data[2].strip()
    S_idx = [ord(ch) - 97 for ch in S]  # 0..25
    
    size = 1 << N
    # precompute transitions: trans[mask][ci] = next_mask
    trans = [[0] * 26 for _ in range(size)]
    
    for mask in range(size):
        # compute old_f[i] = number of set bits among first i positions
        old = [0] * (N + 1)
        cnt = 0
        for i in range(1, N + 1):
            if mask & (1 << (i - 1)):
                cnt += 1
            old[i] = cnt
        
        for ci in range(26):
            new_mask = 0
            prev = 0  # new_f[0] = 0
            for i in range(1, N + 1):
                # candidate from extending with character ci
                if ci == S_idx[i - 1]:
                    cand = old[i - 1] + 1
                else:
                    cand = old[i - 1]
                # new_f[i] = max(old[i], cand)
                cur = old[i] if old[i] >= cand else cand
                if cur > prev:
                    new_mask |= (1 << (i - 1))
                prev = cur
            trans[mask][ci] = new_mask
    
    # DP over length M
    dp = [0] * size
    dp[0] = 1
    for _ in range(M):
        ndp = [0] * size
        for mask in range(size):
            val = dp[mask]
            if val == 0:
                continue
            row = trans[mask]
            for ci in range(26):
                ndp[row[ci]] = (ndp[row[ci]] + val) % MOD
        dp = ndp
    
    # sum by popcount
    ans = [0] * (N + 1)
    for mask in range(size):
        k = mask.bit_count()
        ans[k] = (ans[k] + dp[mask]) % MOD
    
    print(' '.join(map(str, ans)))

if __name__ == "__main__":
    solve()