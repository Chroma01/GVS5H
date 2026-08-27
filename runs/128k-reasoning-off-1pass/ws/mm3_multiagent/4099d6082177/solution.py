import sys

def main():
    sys.setrecursionlimit(1 << 25)
    input = sys.stdin.readline
    
    N, K = map(int, input().split())
    if K == 1:
        print("Yes")
        return
    
    total = N * K
    adj = [[] for _ in range(total + 1)]
    for _ in range(total - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    def dfs(u, parent):
        segments = []
        for v in adj[u]:
            if v == parent:
                continue
            s = dfs(v, u)
            if s == -1:
                return -1
            if s > 0:
                segments.append(s)
        
        if not segments:
            return 1
        
        segments.sort()
        i, j = 0, len(segments) - 1
        while i < j:
            if segments[i] + segments[j] != K - 1:
                return -1
            i += 1
            j -= 1
        
        if i == j:
            left = segments[i]
            val = left + 1
            if val == K:
                return 0
            elif val < K:
                return val
            else:
                return -1
        else:
            return 0
    
    result = dfs(1, 0)
    print("Yes" if result == 0 else "No")

main()