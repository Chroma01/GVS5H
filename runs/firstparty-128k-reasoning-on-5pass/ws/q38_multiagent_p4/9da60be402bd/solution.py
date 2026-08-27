import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    rows = data[1:1 + n]
    in_edges = [[] for _ in range(n)]
    out_bits = [[0] * 26 for _ in range(n)]
    odd_base = []
    for i, row in enumerate(rows):
        for j, ch in enumerate(row):
            if ch != '-':
                c = ord(ch) - 97
                in_edges[j].append((i, c))
                out_bits[i][c] |= 1 << j
                odd_base.append(i * n + j)
    full = (1 << n) - 1

    def bfs(base):
        dist = [-1] * (n * n)
        unvis = [full] * n
        q = []
        for code in base:
            if dist[code] == -1:
                dist[code] = 0
                x = code // n
                y = code - x * n
                unvis[x] &= ~(1 << y)
                q.append(code)
        head = 0
        while head < len(q):
            code = q[head]
            head += 1
            nd = dist[code] + 1
            x = code // n
            y = code - x * n
            for i, c in in_edges[x]:
                new = out_bits[y][c] & unvis[i]
                if new:
                    unvis[i] &= ~new
                    base_idx = i * n
                    while new:
                        lsb = new & -new
                        j = lsb.bit_length() - 1
                        idx = base_idx + j
                        dist[idx] = nd
                        q.append(idx)
                        new ^= lsb
        return dist

    even = bfs([i * n + i for i in range(n)])
    odd = bfs(odd_base)
    ans = []
    inf = 10**9
    for i in range(n):
        row = []
        base = i * n
        for j in range(n):
            code = base + j
            best = inf
            e = even[code]
            if e != -1:
                best = min(best, 2 * e)
            o = odd[code]
            if o != -1:
                best = min(best, 2 * o + 1)
            if i == j:
                best = 0
            row.append(str(best if best != inf else -1))
        ans.append(' '.join(row))
    sys.stdout.write('\n'.join(ans))

if __name__ == '__main__':
    main()