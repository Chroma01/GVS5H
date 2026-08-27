import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    bit = [0] * (n + 1)
    ans = 0

    # P is stored in data[1] .. data[n]
    # Scan from right to left.
    for idx in range(n, 0, -1):
        v = data[idx]

        # Count smaller values already seen, i.e. smaller values to the right.
        i = v - 1
        m = 0
        while i > 0:
            m += bit[i]
            i -= i & -i

        # Sum of ranks v-m, v-m+1, ..., v-1
        ans += m * (2 * v - m - 1) // 2

        # Mark value v as seen.
        i = v
        while i <= n:
            bit[i] += 1
            i += i & -i

    print(ans)

if __name__ == "__main__":
    main()