import sys


def main():
    input = sys.stdin.readline
    n = int(input())
    p = list(map(int, input().split()))

    bit = [0] * (n + 1)

    def add(i):
        while i <= n:
            bit[i] += 1
            i += i & -i

    def sum_prefix(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    ans = 0
    for x in p:
        smaller_before = sum_prefix(x - 1)
        # Contribution of x:
        # sum(smaller_before + 1, ..., x - 1)
        ans += (x - 1) * x // 2 - smaller_before * (smaller_before + 1) // 2
        add(x)

    print(ans)


if __name__ == "__main__":
    main()