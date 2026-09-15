import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    bit = [0] * (n + 1)
    ans = 0

    for pos in range(1, n + 1):
        x = data[pos]

        # Count already seen values <= x.
        le = 0
        j = x
        while j:
            le += bit[j]
            j -= j & -j

        # Number of larger elements already seen to the left of x.
        larger_before = (pos - 1) - le

        # Current position of x after conceptually removing those larger elements.
        cur = pos - larger_before  # same as le + 1

        # Move x right from cur to its final position x.
        if cur < x:
            ans += (cur + x - 1) * (x - cur) // 2

        # Insert x into Fenwick tree.
        j = x
        while j <= n:
            bit[j] += 1
            j += j & -j

    print(ans)

if __name__ == "__main__":
    solve()