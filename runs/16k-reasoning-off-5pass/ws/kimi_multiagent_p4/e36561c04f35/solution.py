import sys

def solve():
    data = sys.stdin.buffer.read().split()
    ptr = 0
    T = int(data[ptr]); ptr += 1
    out = []
    for _ in range(T):
        N = int(data[ptr]); ptr += 1
        A = list(map(int, data[ptr:ptr+N])); ptr += N

        # Coordinate-compress values to 0..m-1 for O(1) arrays.
        comp = {}
        B = [0]*N
        for idx, v in enumerate(A):
            c = comp.get(v)
            if c is None:
                c = len(comp)
                comp[v] = c
            B[idx] = c

        INF = float('inf')
        dp = [0]*(N+1)          # dp[i] = min ops to delete prefix A[0:i]
        best = [INF]*len(comp)  # best[c] = min(dp[j] - j + cnt_c(j)) over valid j
        cnt = [0]*len(comp)     # cnt[c] = occurrences of value c in current prefix

        for i in range(1, N+1):
            c = B[i-1]
            cnt[c] += 1
            k = cnt[c]                      # cnt_v(i)
            # Candidate j = 0: delete all non-v in (0, i-1] as singletons, then v's.
            dpi = (i - k) + 1
            # Candidate j >= 1 with A[j] == v (0-indexed position j):
            # dp[j] + (non-v count in (j, i-1]) + 1
            #      = dp[j] + (i-1-j) - (cnt_v(i-1) - cnt_v(j)) + 1
            #      = (i - cnt_v(i)) + (dp[j] - j + cnt_v(j))
            if best[c] < INF:
                cand = best[c] + i - k
                if cand < dpi:
                    dpi = cand
            dp[i] = dpi
            # Position i-1 (value v) becomes a valid block-start for future i':
            # j = i-1, store dp[i-1] - (i-1) + cnt_v(i-1), cnt_v(i-1) = k-1.
            val = dp[i-1] - (i-1) + (k-1)
            if val < best[c]:
                best[c] = val

        out.append(str(dp[N]))
    sys.stdout.write('\n'.join(out) + '\n')

solve()