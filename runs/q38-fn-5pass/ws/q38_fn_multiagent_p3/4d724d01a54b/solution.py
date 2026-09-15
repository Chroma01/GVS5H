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

    bit = [0] * (n + 1)
    ans = 0

    for x in range(n, 0, -1):
        idx = pos[x]

        # Count already processed larger values whose initial positions are < idx.
        larger_left = 0
        j = idx - 1
        while j > 0:
            larger_left += bit[j]
            j -= j & -j

        cur = idx - larger_left

        # Move x right from cur to its final position x.
        if cur < x:
            d = x - cur
            ans += (cur + x - 1) * d // 2

        # Mark this value as processed.
        j = idx
        while j <= n:
            bit[j] += 1
            j += j & -j

    print(ans)

if __name__ == "__main__":
    main()