import sys
from collections import defaultdict

def solve():
    data = sys.stdin.buffer.read().split()
    ptr = 0
    T = int(data[ptr]); ptr += 1
    out = []
    for _ in range(T):
        N = int(data[ptr]); ptr += 1
        A = list(map(int, data[ptr:ptr+N])); ptr += N

        dp = [0] * (N + 1)
        # For each value v, maintain:
        #   cnt[v] = number of occurrences of v seen so far (i.e., cnt_i^v)
        #   best[v] = min over processed positions j (with A[j]=v) of (dp[j-1] - cnt_{j-1}^v)
        cnt = defaultdict(int)
        best = defaultdict(lambda: 10**18)

        for i in range(1, N + 1):
            v = A[i-1]
            cnt[v] += 1
            c = cnt[v]  # cnt_i^v

            # Option 1: delete A[i] alone as a prefix of length 1
            dpi = dp[i-1] + 1

            # Option 2: delete a block consisting of all occurrences of v up to i,
            # gathered together. Using the derived formula:
            #   dp[i] = (i - cnt_i^v) + 1 + min_{j in pos(v), j<=i} (dp[j-1] - cnt_{j-1}^v)
            # We include j = i (cost dp[i-1] - (c-1)) which corresponds to deleting
            # just the suffix of v's ending at i with no earlier v's... actually j=i
            # gives dp[i-1] + (i - i) - 1 + 1 = dp[i-1], which is never better than
            # option 1, so it's safe to include.
            b = best[v]
            cand = dp[i-1] - (c - 1)
            if cand < b:
                b = cand
                best[v] = b
            val = (i - c) + 1 + b
            if val < dpi:
                dpi = val

            dp[i] = dpi

        out.append(str(dp[N]))

    sys.stdout.write('\n'.join(out) + '\n')

solve()