import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    total = N * K
    adj = [[] for _ in range(total + 1)]
    for _ in range(total - 1):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        adj[u].append(v)
        adj[v].append(u)

    if K == 1:
        sys.stdout.write("Yes\n")
        return

    # Iterative post-order DFS from root 1
    parent = [0] * (total + 1)
    order = []
    stack = [1]
    parent[1] = -1
    while stack:
        u = stack.pop()
        order.append(u)
        for w in adj[u]:
            if w != parent[u]:
                parent[w] = u
                stack.append(w)

    ret = [0] * (total + 1)
    target = K - 1
    ok = True

    for u in reversed(order):
        counts = {}
        for w in adj[u]:
            if parent[w] == u:
                v = ret[w]
                if v:
                    counts[v] = counts.get(v, 0) + 1
        leftover = 0
        # pair values summing to target
        for a in list(counts.keys()):
            if counts[a] == 0:
                continue
            b = target - a
            if b < a:
                continue
            if a == b:
                c = counts[a]
                pairs = c // 2
                rem = c - 2 * pairs
                counts[a] = rem
            else:
                cb = counts.get(b, 0)
                ca = counts[a]
                pairs = ca if ca < cb else cb
                counts[a] = ca - pairs
                counts[b] = cb - pairs
        # count leftovers
        for a, c in counts.items():
            if c:
                if leftover != 0:
                    ok = False
                    break
                leftover = a
                if c > 1:
                    ok = False
                    break
        if not ok:
            break
        if leftover:
            nv = leftover + 1
            ret[u] = 0 if nv == K else nv
        else:
            ret[u] = 1

    if not ok or ret[1] != 0:
        sys.stdout.write("No\n")
    else:
        sys.stdout.write("Yes\n")

main()