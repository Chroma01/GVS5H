import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    P = list(map(int, data[1:1 + n]))

    # pos[v] = position (1-indexed) of value v in P
    pos = [0] * (n + 1)
    for i, v in enumerate(P, 1):
        pos[v] = i

    # Fenwick tree over positions, counting placed values
    bit = [0] * (n + 2)

    def bit_add(i, delta):
        while i <= n:
            bit[i] += delta
            i += i & (-i)

    def bit_sum(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & (-i)
        return s

    def S(k):
        return k * (k + 1) // 2

    ans = 0
    # Insert values 1..N in order; r_v = rank of pos[v] among pos[1..v]
    # Cost to bring value v to its final place = sum of boundary indices
    # from r_v to v-1 = S(v-1) - S(r_v-1)
    for v in range(1, n + 1):
        p = pos[v]
        le = bit_sum(p)          # number of already placed values with position <= p
        r = le + 1               # rank of p among positions of values 1..v
        ans += S(v - 1) - S(r - 1)
        bit_add(p, 1)

    print(ans)

main()