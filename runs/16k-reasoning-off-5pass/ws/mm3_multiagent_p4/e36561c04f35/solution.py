import sys
from sys import stdin

def solve():
    data = stdin.buffer.read().split()
    idx = 0
    T = int(data[idx]); idx += 1
    out = []
    for _ in range(T):
        N = int(data[idx]); idx += 1
        A = [int(data[idx + i]) for i in range(N)]
        idx += N
        
        # Compute last occurrence for each position
        last_occ = [0] * N
        d = {}
        for i in range(N - 1, -1, -1):
            if A[i] in d:
                last_occ[i] = d[A[i]]
            else:
                last_occ[i] = i
            d[A[i]] = i
        
        # The correct O(N) greedy:
        # Process left to right maintaining a set S of values whose 
        # last occurrence is strictly to the right (i.e., "open" values).
        # For each A[i]:
        #   - If A[i] is in S: this occurrence pairs with a future occurrence, 
        #     so it can share a block. Remove A[i] from S (it closes a block).
        #   - If A[i] is NOT in S:
        #       - If i == last_occ[i] (last occurrence): this is a standalone 
        #         element that must form its own block. Increment answer.
        #       - Else (first occurrence): add A[i] to S, increment answer.
        # The answer counts the number of block-forming decisions.
        S = set()
        ans = 0
        for i in range(N):
            v = A[i]
            if v in S:
                # This occurrence pairs with a future one; close a block
                S.remove(v)
                # No new block needed for this occurrence (it joins the future's block)
            else:
                # v not in S: either first occurrence (last_occ > i) or last occurrence
                if i == last_occ[i]:
                    # Last occurrence, no future: standalone block
                    ans += 1
                else:
                    # First occurrence, future exists: open a block
                    S.add(v)
                    ans += 1
        out.append(str(ans))
    
    sys.stdout.write('\n'.join(out))

solve()