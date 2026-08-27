import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    p = data[1:1 + n]

    bit = [0] * (n + 1)
    ans = 0
    tri = 0  # T(i-1) = (i-1)*i//2, updated incrementally

    for i, x in enumerate(p, 1):
        tri += i - 1

        # Fenwick query: number of previous values strictly smaller than x
        s = 0
        j = x - 1
        while j > 0:
            s += bit[j]
            j -= j & -j

        # Contribution of inserting P_i into the sorted prefix:
        # sum of edges (s+1) through (i-1)
        ans += tri - s * (s + 1) // 2

        # Fenwick update: add current value x
        j = x
        while j <= n:
            bit[j] += 1
            j += j & -j

    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()