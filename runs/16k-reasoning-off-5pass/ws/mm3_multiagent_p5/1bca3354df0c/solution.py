import sys
sys.setrecursionlimit(1 << 25)
input = sys.stdin.readline

def solve():
    N, M = map(int, input().split())
    adj = [[] for _ in range(N)]
    for _ in range(M):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        adj[u].append(v)
        adj[v].append(u)
    
    color = [-1] * N
    components = []  # list of (L, R) for each component
    for i in range(N):
        if color[i] == -1:
            stack = [i]
            color[i] = 0
            L = 1
            R = 0
            while stack:
                u = stack.pop()
                for v in adj[u]:
                    if color[v] == -1:
                        color[v] = color[u] ^ 1
                        if color[v] == 0:
                            L += 1
                        else:
                            R += 1
                        stack.append(v)
            components.append((L, R))
    
    # Compute Grundy value: XOR of (L-1) and (R-1) for each component
    grundy = 0
    for L, R in components:
        grundy ^= (L - 1) ^ (R - 1)
    
    if grundy != 0:
        print("Aoki")
    else:
        print("Takahashi")

solve()