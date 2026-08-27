import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    adj = [[] for _ in range(n + 1)]
    idx = 1
    for _ in range(n - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
    deg = [0] * (n + 1)
    for c in range(1, n + 1):
        deg[c] = len(adj[c])
    best = 0
    for c in range(1, n + 1):
        caps = [deg[v] - 1 for v in adj[c]]
        caps.sort(reverse=True)
        for i, y in enumerate(caps, 1):
            if y < 1:
                break
            kept = 1 + (1 + y) * i
            if kept > best:
                best = kept
    sys.stdout.write(str(n - best) + "\n")

main()