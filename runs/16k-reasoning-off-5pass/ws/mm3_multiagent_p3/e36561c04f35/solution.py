import sys
from collections import Counter, deque

def solve():
    input = sys.stdin.readline
    T = int(input())
    out = []
    for _ in range(T):
        N = int(input())
        A = list(map(int, input().split()))
        freq = Counter(A)
        m = max(freq.values())
        ans = max(2 * m - 1, N)
        out.append(str(ans))
    print('\n'.join(out))

solve()