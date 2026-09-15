import sys

MOD = 998244353

def find(parent, diff, x):
    root = x
    parity = 0
    while parent[root] != root:
        parity ^= diff[root]
        root = parent[root]
    cur = x
    cur_parity = parity
    while parent[cur] != cur:
        nxt = parent[cur]
        old = diff[cur]
        parent[cur] = root
        diff[cur] = cur_parity
        cur_parity ^= old
        cur = nxt
    return root, parity

def union(parent, diff, rank, x, y, c):
    rx, px = find(parent, diff, x)
    ry, py = find(parent, diff, y)
    if rx == ry:
        return (px ^ py) == c
    d = c ^ px ^ py
    if rank[rx] < rank[ry]:
        parent[rx] = ry
        diff[rx] = d
    else:
        parent[ry] = rx
        diff[ry] = d
        if rank[rx] == rank[ry]:
            rank[rx] += 1
    return True

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    T = int(next(it))
    out = []
    for _ in range(T):
        H = int(next(it))
        W = int(next(it))
        grid = [next(it) for _ in range(H)]
        n = H + W
        parent = list(range(n))
        rank = [0] * n
        diff = [0] * n
        colParity = [0] * W
        invalid = False
        for i in range(H):
            row = grid[i]
            rowParity = 0
            for j in range(W):
                a = 1 if row[j] == 65 else 0
                if a == 0:
                    c = 1 ^ colParity[j] ^ rowParity
                    if not union(parent, diff, rank, i, H + j, c):
                        invalid = True
                        break
                rowParity ^= a
            if invalid:
                break
            if rowParity != 0:
                invalid = True
                break
            for j in range(W):
                if row[j] == 65:
                    colParity[j] ^= 1
        if not invalid:
            for j in range(W):
                if colParity[j] != 0:
                    invalid = True
                    break
        if invalid:
            out.append('0')
        else:
            comps = 0
            for i in range(n):
                if parent[i] == i:
                    comps += 1
            out.append(str(pow(2, comps, MOD)))
    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    solve()