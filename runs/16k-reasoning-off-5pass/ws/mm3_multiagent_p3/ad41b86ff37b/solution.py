import sys

def solve():
    input = sys.stdin.readline
    N = int(input().strip())
    adj = [[] for _ in range(N+1)]
    for _ in range(N-1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    deg = [0]*(N+1)
    for i in range(1, N+1):
        deg[i] = len(adj[i])
    
    max_total = 0
    for c in range(1, N+1):
        if len(adj[c]) == 0:
            continue
        # list of available leaves for each neighbor branch
        a = [deg[nb] - 1 for nb in adj[c]]
        a.sort(reverse=True)
        i = 0
        k = len(a)
        while i < k:
            v = a[i]
            if v == 0:
                # y must be at least 1, so skip v=0
                i += 1
                continue
            j = i
            while j+1 < k and a[j+1] == v:
                j += 1
            cnt = j + 1   # number of neighbors with a_i >= v
            total = 1 + cnt * (1 + v)
            if total > max_total:
                max_total = total
            i = j + 1
    
    # The problem guarantees a Snowflake Tree can be obtained, so max_total >= 3.
    print(N - max_total)

if __name__ == "__main__":
    solve()