import sys

def solve():
    input = sys.stdin.buffer.read().split()
    ptr = 0
    t = int(input[ptr]); ptr += 1
    out = []
    for _ in range(t):
        n = int(input[ptr]); ptr += 1
        a = list(map(int, input[ptr:ptr+n])); ptr += n
        
        dp = [0] * (n + 1)
        cnt = [0] * (n + 1)  # cnt[v] = occurrences of v up to current position
        last = {}  # v -> (last_idx, cnt_at_last_idx, dp_at_last_idx)
        
        for i in range(1, n + 1):
            v = a[i-1]
            cnt[v] += 1
            
            # Option 1: delete single element (always valid)
            dp[i] = dp[i-1] + 1
            
            # Option 2: delete block from 1 to i (all elements are v after swaps)
            # Cost = (i - cnt[v]) swaps + 1 deletion
            dp[i] = min(dp[i], i - cnt[v] + 1)
            
            # Option 3: delete block from last[v]+1 to i
            # We need dp[j] + (i-j) - count_v(j+1..i) + 1
            # where j = last[v], count_v(j+1..i) = cnt[v] - cnt_at_last
            if v in last:
                j, cnt_j, dp_j = last[v]
                count_v_in_block = cnt[v] - cnt_j
                cost = dp_j + (i - j) - count_v_in_block + 1
                dp[i] = min(dp[i], cost)
            
            # Update last occurrence info for v
            last[v] = (i, cnt[v], dp[i])
        
        out.append(str(dp[n]))
    print('\n'.join(out))

solve()