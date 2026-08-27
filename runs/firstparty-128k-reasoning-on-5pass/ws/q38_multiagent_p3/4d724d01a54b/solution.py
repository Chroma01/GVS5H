import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    bit = [0] * (n + 1)
    ans = 0

    for i in range(1, n + 1):
        x = int(data[i])

        # r = number of previous values strictly smaller than x
        idx = x - 1
        r = 0
        while idx:
            r += bit[idx]
            idx -= idx & -idx

        # Contribution of position i:
        # sum of edges r+1 .. i-1
        ans += i * (i - 1) // 2 - r * (r + 1) // 2

        # Add current value to Fenwick tree
        idx = x
        while idx <= n:
            bit[idx] += 1
            idx += idx & -idx

    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()