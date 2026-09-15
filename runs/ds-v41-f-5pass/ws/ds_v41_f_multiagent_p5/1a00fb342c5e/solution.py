import sys

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    m = int(data[pos]); pos += 1

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        x = int(data[pos]); y = int(data[pos + 1]); z = int(data[pos + 2]); pos += 3
        if x == y:
            # self loop: A_x XOR A_x = 0, so requires z == 0
            if z != 0:
                sys.stdout.write("-1\n")
                return
            continue
        adj[x].append((y, z))
        adj[y].append((x, z))

    pot = [-1] * (n + 1)   # relative XOR potential from component root
    ans = [0] * (n + 1)
    MAXB = 31

    for s in range(1, n + 1):
        if pot[s] != -1:
            continue
        pot[s] = 0
        stack = [s]
        members = []
        while stack:
            u = stack.pop()
            members.append(u)
            pu = pot[u]
            for v, z in adj[u]:
                pv = pot[v]
                if pv == -1:
                    pot[v] = pu ^ z
                    stack.append(v)
                elif (pu ^ pv) != z:
                    sys.stdout.write("-1\n")
                    return

        size = len(members)
        cnt = [0] * MAXB
        for v in members:
            pv = pot[v]
            b = 0
            while pv:
                if pv & 1:
                    cnt[b] += 1
                pv >>= 1
                b += 1

        # choose the component offset bit-by-bit (majority minimization)
        c = 0
        for b in range(MAXB):
            if cnt[b] * 2 > size:
                c |= (1 << b)

        for v in members:
            ans[v] = pot[v] ^ c

    sys.stdout.write(' '.join(map(str, ans[1:])) + '\n')

main()