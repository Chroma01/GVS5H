import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    adj = [[] for _ in range(n + 1)]
    deg = [0] * (n + 1)
    idx = 1
    for _ in range(n - 1):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)
        deg[u] += 1
        deg[v] += 1

    best = 0
    for c in range(1, n + 1):
        # avail(v) = number of v's neighbors other than c = deg(v) - 1
        avails = [deg[v] - 1 for v in adj[c]]
        avails.sort(reverse=True)
        # take x largest; y = avails[x-1]; kept = 1 + x * (1 + y), need y >= 1
        for x in range(1, len(avails) + 1):
            y = avails[x - 1]
            if y < 1:
                break
            kept = 1 + x * (1 + y)
            if kept > best:
                best = kept

    sys.stdout.write(str(n - best) + "\n")

main()