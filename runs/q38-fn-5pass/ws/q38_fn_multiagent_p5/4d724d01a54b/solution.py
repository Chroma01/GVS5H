import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    p = data[1:]

    pos = [0] * (n + 1)
    for i, v in enumerate(p, 1):
        pos[v] = i

    bit = [0] * (n + 1)
    ans = 0

    for x in range(1, n + 1):
        idx = pos[x]

        # Count already processed smaller values at positions <= idx.
        # Since pos[x] itself is not processed yet, this is the number
        # of smaller values to the left of x.
        s = 0
        j = idx
        while j > 0:
            s += bit[j]
            j -= j & -j

        m = (x - 1) - s  # smaller values initially to the right of x

        # Minimum cost contributed by moving x right across those m values:
        # (x - m) + (x - m + 1) + ... + (x - 1)
        ans += m * x - m * (m + 1) // 2

        # Mark position of x as processed.
        j = idx
        while j <= n:
            bit[j] += 1
            j += j & -j

    print(ans)

if __name__ == "__main__":
    main()