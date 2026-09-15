import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    P = data[1:1 + n]

    # Fenwick tree over values 1..n, counting how many seen values are <= some bound.
    tree = [0] * (n + 1)
    ans = 0

    for idx in range(n):
        val = int(P[idx])
        pos = idx + 1  # 1-indexed original position of this element

        # count of already-seen values that are <= val (== < val since val not inserted yet)
        s = 0
        j = val
        while j > 0:
            s += tree[j]
            j -= j & (-j)

        # c = number of earlier (already-seen) values strictly greater than val
        c = idx - s

        # this element makes c leftward swaps at positions pos-1, pos-2, ..., pos-c
        ans += c * pos - c * (c + 1) // 2

        # insert val
        j = val
        while j <= n:
            tree[j] += 1
            j += j & (-j)

    sys.stdout.write(str(ans) + "\n")


main()