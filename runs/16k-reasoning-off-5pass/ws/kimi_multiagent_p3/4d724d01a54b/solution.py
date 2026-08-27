import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    P = list(map(int, data[1:1 + n]))

    # pos[v] = original index (1-based) of value v
    pos = [0] * (n + 1)
    for i, v in enumerate(P, 1):
        pos[v] = i

    # Fenwick tree over positions 1..n storing counts of values <= current v
    bit = [0] * (n + 1)

    def add(i):
        while i <= n:
            bit[i] += 1
            i += i & -i

    def query(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    ans = 0
    # Process values v = 1..N.
    # r_v = #{x <= v : pos_x <= pos_v} = rank of pos_v among positions of values 1..v.
    # Strategy: process values in DECREASING order, moving each v rightward to slot v.
    # When v is processed, values > v already occupy slots v+1..N, so unplaced values
    # 1..v occupy positions 1..v in their original relative order; v sits at rank r_v
    # and must cross cuts r_v, r_v+1, ..., v-1, paying sum_{j=r_v}^{v-1} j.
    # This is optimal: cut j must be used at least #{v > j : r_v <= j} times
    # (each such v forces a distinct crossing of cut j), and the strategy achieves
    # exactly that count at every cut.
    for v in range(1, n + 1):
        p = pos[v]
        r = query(p) + 1  # values < v already inserted; +1 for v itself
        d = v - r
        if d > 0:
            ans += d * (v + r - 1) // 2
        add(p)

    print(ans)

solve()