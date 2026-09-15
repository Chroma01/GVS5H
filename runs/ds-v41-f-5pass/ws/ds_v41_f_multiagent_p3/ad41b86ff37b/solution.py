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

    best = 0
    for c in range(1, n + 1):
        # a_v = number of non-center neighbors available at v
        vals = [deg[v] - 1 for v in adj[c]]
        vals.sort(reverse=True)
        for i, a in enumerate(vals):
            if a < 1:
                break
            # use (i+1) branches, each with y = a leaves  -> kept = 1 + (i+1)*(a+1)
            cand = 1 + (i + 1) * (a + 1)
            if cand > best:
                best = cand

    sys.stdout.write(str(n - best) + "\n")

main()