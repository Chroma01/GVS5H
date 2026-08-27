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

    deg = [len(a) for a in adj]

    best = 0
    # Try every vertex as the red center of the Snowflake Tree.
    for r in range(1, n + 1):
        # Capacity of neighbor b as a blue vertex:
        # number of leaves it can have besides r.
        caps = [deg[b] - 1 for b in adj[r]]
        caps.sort(reverse=True)
        # Choosing the k best branches forces y = caps[k-1] (must be >= 1).
        for k, c in enumerate(caps, 1):
            if c < 1:
                break
            kept = 1 + k * (c + 1)  # 1 center + k blue + k*y leaves
            if kept > best:
                best = kept

    print(n - best)

main()