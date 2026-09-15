import sys


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    m = int(data[1])

    adj = [[] for _ in range(n + 1)]
    idx = 2

    for _ in range(m):
        x = int(data[idx])
        y = int(data[idx + 1])
        z = int(data[idx + 2])
        idx += 3

        if x == y:
            if z != 0:
                sys.stdout.write("-1\n")
                return
            continue

        adj[x].append((y, z))
        adj[y].append((x, z))

    del data

    pot = [-1] * (n + 1)
    ans = [0] * (n + 1)

    for start in range(1, n + 1):
        if pot[start] != -1:
            continue

        if not adj[start]:
            pot[start] = 0
            ans[start] = 0
            continue

        pot[start] = 0
        stack = [start]
        comp = []
        vals = []
        max_val = 0

        while stack:
            u = stack.pop()
            comp.append(u)
            pu = pot[u]
            vals.append(pu)

            if pu > max_val:
                max_val = pu

            for v, w in adj[u]:
                np = pu ^ w
                pv = pot[v]

                if pv == -1:
                    pot[v] = np
                    stack.append(v)
                elif pv != np:
                    sys.stdout.write("-1\n")
                    return

        size = len(comp)
        offset = 0

        if max_val:
            for b in range(max_val.bit_length()):
                cnt = 0
                for val in vals:
                    cnt += (val >> b) & 1

                if cnt * 2 > size:
                    offset |= 1 << b

        if offset:
            for u, val in zip(comp, vals):
                ans[u] = val ^ offset
        else:
            for u, val in zip(comp, vals):
                ans[u] = val

    sys.stdout.write(" ".join(map(str, ans[1:])) + "\n")


if __name__ == "__main__":
    solve()