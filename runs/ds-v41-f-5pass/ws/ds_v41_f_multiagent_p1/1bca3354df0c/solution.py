import sys
from collections import deque

def main():
    input = sys.stdin.buffer.read().split()
    idx = 0
    N = int(input[idx]); idx+=1
    M = int(input[idx]); idx+=1
    adj = [[] for _ in range(N+1)]
    for _ in range(M):
        u = int(input[idx]); idx+=1
        v = int(input[idx]); idx+=1
        adj[u].append(v)
        adj[v].append(u)
    if N % 2 == 1:
        print("Aoki" if M % 2 == 1 else "Takahashi")
        return
    color = [-1]*(N+1)
    o = 0; k = 0; base = 0
    for s in range(1, N+1):
        if color[s] == -1:
            color[s] = 0
            dq = deque([s])
            cnt = [0,0]
            while dq:
                u = dq.popleft()
                cnt[color[u]] += 1
                for w in adj[u]:
                    if color[w] == -1:
                        color[w] = color[u]^1
                        dq.append(w)
            a = min(cnt[0], cnt[1])
            b = max(cnt[0], cnt[1])
            size = a+b
            if size % 2 == 1:
                o += 1
                if size > 1:
                    k += 1
            else:
                if a % 2 == 1:  # both parts odd
                    base += 1
    if k > 0:
        print("Aoki")
    else:
        w = (M + base + o//2) % 2
        print("Aoki" if w == 1 else "Takahashi")

main()