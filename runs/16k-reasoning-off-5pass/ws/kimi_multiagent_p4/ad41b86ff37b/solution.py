import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    deg = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    idx = 1
    for _ in range(n - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    best_kept = 0
    for c in range(1, n + 1):
        vals = [deg[v] - 1 for v in adj[c] if deg[v] >= 2]
        if not vals:
            continue
        vals.sort(reverse=True)
        # for rank i (1-indexed), choose y = vals[i-1], count = i
        # kept = 1 + (1 + y) * i
        local = 0
        for i, a in enumerate(vals, 1):
            if a < 1:
                break
            cand = (a + 1) * i
            if cand > local:
                local = cand
        kept = local + 1
        if kept > best_kept:
            best_kept = kept

    print(n - best_kept)

main()