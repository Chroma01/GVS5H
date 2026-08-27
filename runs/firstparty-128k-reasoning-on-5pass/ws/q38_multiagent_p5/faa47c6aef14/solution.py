import sys
from bisect import bisect_left

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    x = data[1] - 1
    idx = 2
    red = data[idx:idx+n]
    idx += n
    red_total = sum(red)
    blue = data[idx:idx+n]
    idx += n
    blue_total = sum(blue)
    inv_p = [0] * n
    for i in range(n):
        inv_p[data[idx + i] - 1] = i
    idx += n
    inv_q = [0] * n
    for i in range(n):
        inv_q[data[idx + i] - 1] = i
    del data

    def get_chain(inv, has, total):
        if total == 0:
            return []
        node_at = [x]
        cur = x
        d = 0
        max_d = 0
        in_cycle = 0
        while True:
            h = has[cur]
            if h:
                in_cycle += h
                if d > max_d:
                    max_d = d
            nxt = inv[cur]
            if nxt == x:
                break
            cur = nxt
            d += 1
            node_at.append(cur)
        if in_cycle != total:
            return None
        if max_d == 0:
            return []
        return node_at[max_d:0:-1]

    r = get_chain(inv_p, red, red_total)
    if r is None:
        print(-1)
        return
    b = get_chain(inv_q, blue, blue_total)
    if b is None:
        print(-1)
        return

    del red, blue, inv_p, inv_q

    if not r or not b:
        print(len(r) + len(b))
        return

    pos = [-1] * n
    for i, node in enumerate(r):
        pos[node] = i

    tails = []
    for node in b:
        p = pos[node]
        if p != -1:
            j = bisect_left(tails, p)
            if j == len(tails):
                tails.append(p)
            else:
                tails[j] = p

    print(len(r) + len(b) - len(tails))

if __name__ == "__main__":
    solve()