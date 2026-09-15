import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    # pos[value] = 1-based original position
    pos = [0] * (n + 1)
    for i in range(n):
        pos[int(data[1 + i])] = i + 1

    tree = [0] * (n + 1)
    total = 0

    for v in range(1, n + 1):
        p = pos[v]
        # query: number of values u < v with pos[u] <= p  (== pos[u] < p)
        s = 0
        i = p
        while i > 0:
            s += tree[i]
            i -= i & (-i)
        c = s + 1  # rank of v among values 1..v (current position in reduced array)
        # move v right from rank c to position v: sum_{i=c}^{v-1} i = T(v-1)-T(c-1)
        total += (v - 1) * v // 2 - (c - 1) * c // 2
        # insert pos[v]
        i = p
        while i <= n:
            tree[i] += 1
            i += i & (-i)

    print(total)


main()