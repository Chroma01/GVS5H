import sys
import numpy as np

def main():
    data = sys.stdin.read().split()
    H = int(data[0])
    W = int(data[1])
    rows_str = data[2:]
    # compress row patterns into frequency array
    size = 1 << W
    cnt = np.zeros(size, dtype=np.int64)
    for s in rows_str:
        mask = int(s, 2)
        cnt[mask] += 1
    total_rows = H
    # dp[mask, k] = sum_{b: popcount(b XOR mask)=k} cnt[b]
    # initialize: dp[mask, 0] = cnt[mask], others 0
    dp = np.zeros((size, W+1), dtype=np.int64)
    dp[:, 0] = cnt
    # process each bit
    for i in range(W):
        step = 1 << i
        # iterate over blocks of size 2*step
        for base in range(0, size, step << 1):
            # split into two halves: first half (bit i=0), second half (bit i=1)
            dp0 = dp[base:base+step]
            dp1 = dp[base+step:base+(step<<1)]
            # shift dp1 and dp0 right by 1 along axis=1
            dp1_shift = np.roll(dp1, 1, axis=1)
            dp1_shift[:, 0] = 0
            dp0_shift = np.roll(dp0, 1, axis=1)
            dp0_shift[:, 0] = 0
            # compute new values
            new_dp0 = dp0 + dp1_shift
            new_dp1 = dp0_shift + dp1
            # write back
            dp[base:base+step] = new_dp0
            dp[base+step:base+(step<<1)] = new_dp1
    # compute cost for each mask
    # precompute min(k, W-k) for k=0..W
    min_vals = np.array([min(k, W - k) for k in range(W+1)], dtype=np.int64)
    # cost = dp dot min_vals
    costs = dp.dot(min_vals)
    ans = int(costs.min())
    print(ans)

if __name__ == "__main__":
    main()