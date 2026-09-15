import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    p = data[1:1 + n]

    pos = [0] * (n + 1)
    for i, v in enumerate(p, 1):
        pos[v] = i

    # Fenwick tree initially containing 1 at every original position.
    bit = [0] + [1] * n
    for i in range(1, n + 1):
        j = i + (i & -i)
        if j <= n:
            bit[j] += bit[i]

    ans = 0

    # Process values from largest to smallest.
    for x in range(n, 0, -1):
        idx = pos[x]

        # Current position of x among the remaining values 1..x.
        cur = 0
        i = idx
        while i > 0:
            cur += bit[i]
            i -= i & -i

        # Move x right from cur to x.
        # Cost is cur + (cur + 1) + ... + (x - 1).
        d = x - cur
        ans += d * (cur + x - 1) // 2

        # Remove x from the Fenwick tree.
        i = idx
        while i <= n:
            bit[i] -= 1
            i += i & -i

    print(ans)

if __name__ == "__main__":
    main()