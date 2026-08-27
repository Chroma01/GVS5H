import sys


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    p = list(map(int, data[1:1 + n]))

    # bit[x] = number of previous values <= x
    bit = [0] * (n + 1)

    def bit_add(i: int, delta: int) -> None:
        while i <= n:
            bit[i] += delta
            i += i & -i

    def bit_sum(i: int) -> int:
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    # diff over adjacent-swap edges 1..n-1.
    # If position j has r larger values before it, the leftmost-descent
    # reduced word uses every edge in [j-r, j-1] once for this element.
    diff = [0] * (n + 2)
    for j, x in enumerate(p, start=1):
        prev = j - 1
        le = bit_sum(x)
        r = prev - le  # number of previous values greater than x
        if r:
            l = j - r
            rr = j - 1
            diff[l] += 1
            diff[rr + 1] -= 1
        bit_add(x, 1)

    ans = 0
    cur = 0
    for i in range(1, n):
        cur += diff[i]
        ans += i * cur
    print(ans)


if __name__ == "__main__":
    solve()