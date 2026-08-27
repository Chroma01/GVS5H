import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    rows = [data[1 + i].decode() for i in range(N)]

    # Label-bucketed edge structures
    in_list = [[[] for _ in range(N)] for _ in range(26)]  # in_list[c][l] = [a, ...] with a->l labeled c
    out_bits = [[0] * N for _ in range(26)]                # out_bits[c][r] = bitset of b with r->b labeled c
    in_mask = [0] * N   # bitmask of labels on edges entering l
    out_mask = [0] * N  # bitmask of labels on edges leaving r

    ans = [[-1] * N for _ in range(N)]
    assigned = [0] * N  # assigned[a] = bitset of b whose dist[a][b] is finalized

    # Dial-style buckets: buckets[d] = encoded states (l*N + r) with distance d
    buckets = [[] for _ in range(2)]

    # Base case 1: empty string is a palindrome, dist[v][v] = 0
    for v in range(N):
        ans[v][v] = 0
        assigned[v] = 1 << v
        buckets[0].append(v * N + v)

    # Base case 2: any single edge label is a palindrome of length 1
    for i in range(N):
        row = rows[i]
        for j in range(N):
            ch = row[j]
            if ch != '-':
                c = ord(ch) - 97
                in_list[c][j].append(i)
                out_bits[c][i] |= (1 << j)
                in_mask[j] |= (1 << c)
                out_mask[i] |= (1 << c)
                bit = 1 << j
                if not (assigned[i] & bit):
                    assigned[i] |= bit
                    ans[i][j] = 1
                    buckets[1].append(i * N + j)

    # Dijkstra over pair-states (l, r). All transitions add exactly 2:
    # if a->l and r->b share a label, dist[a][b] <= dist[l][r] + 2.
    # Processing buckets in increasing d means first assignment is final.
    d = 0
    while d < len(buckets):
        cur = buckets[d]
        if cur:
            nd = d + 2
            while len(buckets) <= nd:
                buckets.append([])
            nb = buckets[nd]
            for state in cur:
                l, r = divmod(state, N)
                cm = in_mask[l] & out_mask[r]  # labels present on both sides
                while cm:
                    lb = cm & -cm
                    c = lb.bit_length() - 1
                    cm ^= lb
                    ob = out_bits[c][r]
                    for a in in_list[c][l]:
                        new = ob & ~assigned[a]
                        if new:
                            assigned[a] |= new
                            ans_a = ans[a]
                            base = a * N
                            bits = new
                            while bits:
                                bbit = bits & -bits
                                b = bbit.bit_length() - 1
                                bits ^= bbit
                                ans_a[b] = nd
                                nb.append(base + b)
        d += 1

    out = sys.stdout
    for i in range(N):
        out.write(' '.join(map(str, ans[i])) + '\n')

main()