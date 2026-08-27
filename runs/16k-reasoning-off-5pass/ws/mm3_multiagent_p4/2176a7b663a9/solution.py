import sys
from sys import stdin
input = stdin.readline

def solve():
    N = int(input())
    W = list(map(int, input().split()))
    L = [0]*N
    R = [0]*N
    intervals = []
    for i in range(N):
        l, r = map(int, input().split())
        L[i] = l
        R[i] = r
        intervals.append((l, r, i))
    
    Q = int(input())
    queries = []
    for _ in range(Q):
        s, t = map(int, input().split())
        s -= 1; t -= 1
        queries.append((s, t))
    
    # Check direct edge
    def disjoint(i, j):
        return R[i] < L[j] or R[j] < L[i]
    
    out = []
    for s, t in queries:
        if disjoint(s, t):
            out.append(W[s] + W[t])
        else:
            out.append(-1)
    
    print('\n'.join(map(str, out)))

solve()