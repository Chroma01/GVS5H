import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    p = data[1:]

    bit = [0] * (n + 1)

    def add(i):
        while i <= n:
            bit[i] += 1
            i += i & -i

    def prefix_sum(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    ans = 0
    for j, x in enumerate(p, 1):
        # Number of previously seen values smaller than x.
        k = prefix_sum(x - 1)

        # x is inserted from position j into position k + 1.
        # It crosses edges k+1, k+2, ..., j-1.
        ans += (j + k) * (j - 1 - k) // 2

        add(x)

    print(ans)


if __name__ == "__main__":
    main()