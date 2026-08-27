import sys
from collections import defaultdict

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    # Term 1: sum over all subarrays of number of distinct values
    # contribution of position i (1-indexed): (i - prev_occurrence) * (n - i + 1)
    last = [0] * (n + 2)
    term1 = 0
    for i, x in enumerate(A, start=1):
        term1 += (i - last[x]) * (n - i + 1)
        last[x] = i

    # positions of each value
    pos = defaultdict(list)
    for i, x in enumerate(A, start=1):
        pos[x].append(i)

    def avoid_count(S):
        # number of subarrays [L,R] (1<=L<=R<=n) containing no position of S
        # S: sorted list of forbidden positions
        total = 0
        prev = 0
        for p in S:
            g = p - prev - 1
            total += g * (g + 1) // 2
            prev = p
        g = n - prev
        total += g * (g + 1) // 2
        return total

    total_sub = n * (n + 1) // 2
    term2 = 0
    for v in range(1, n + 1):
        if v not in pos or (v + 1) not in pos:
            continue
        P = pos[v]
        Q = pos[v + 1]
        both = sorted(P + Q)  # merged sorted list of positions with value v or v+1
        # subarrays containing at least one v and at least one v+1
        cnt = total_sub - avoid_count(P) - avoid_count(Q) + avoid_count(both)
        term2 += cnt

    print(term1 - term2)

solve()