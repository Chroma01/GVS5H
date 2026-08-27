import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    adj = [[] for _ in range(N + 1)]
    deg = [0] * (N + 1)
    for _ in range(N - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    max_kept = 0
    for c in range(1, N + 1):
        vals = [deg[v] - 1 for v in adj[c]]
        vals.sort()
        m = len(vals)
        i = 0
        while i < m:
            # y = vals[i]; cnt = number of neighbors with a_v >= y
            cnt = m - i
            cand = 1 + (1 + vals[i]) * cnt
            if cand > max_kept:
                max_kept = cand
            # skip duplicates
            j = i + 1
            while j < m and vals[j] == vals[i]:
                j += 1
            i = j

    print(N - max_kept)

main()