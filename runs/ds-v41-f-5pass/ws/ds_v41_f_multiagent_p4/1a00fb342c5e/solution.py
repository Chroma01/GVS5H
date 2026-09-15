import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    m = int(data[pos]); pos += 1

    # Forward-star adjacency
    head = [-1] * (n + 1)
    nxt = [0] * (2 * m)
    to = [0] * (2 * m)
    wt = [0] * (2 * m)
    ec = 0

    for _ in range(m):
        x = int(data[pos]); y = int(data[pos + 1]); z = int(data[pos + 2]); pos += 3
        to[ec] = y; wt[ec] = z; nxt[ec] = head[x]; head[x] = ec; ec += 1
        to[ec] = x; wt[ec] = z; nxt[ec] = head[y]; head[y] = ec; ec += 1

    offset = [-1] * (n + 1)
    ans = [0] * (n + 1)
    BITS = 30

    for s in range(1, n + 1):
        if offset[s] != -1:
            continue
        offset[s] = 0
        comp = []
        dq = deque([s])
        while dq:
            u = dq.popleft()
            comp.append(u)
            ou = offset[u]
            e = head[u]
            while e != -1:
                v = to[e]
                z = wt[e]
                if offset[v] == -1:
                    offset[v] = ou ^ z
                    dq.append(v)
                else:
                    if (ou ^ offset[v]) != z:
                        sys.stdout.write("-1\n")
                        return
                e = nxt[e]

        csz = len(comp)
        rv = 0
        for k in range(BITS):
            bit = 1 << k
            cnt = 0
            for v in comp:
                if offset[v] & bit:
                    cnt += 1
            if cnt * 2 > csz:
                rv |= bit
        for v in comp:
            ans[v] = rv ^ offset[v]

    sys.stdout.write(" ".join(map(str, ans[1:])) + "\n")

main()