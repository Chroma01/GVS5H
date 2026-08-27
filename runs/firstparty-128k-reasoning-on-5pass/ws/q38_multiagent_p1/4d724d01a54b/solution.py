import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    bit = [0] * (n + 1)
    ans = 0

    for idx in range(1, n + 1):
        x = data[idx]

        # Query count of already seen values smaller than x.
        i = x - 1
        smaller_before = 0
        while i > 0:
            smaller_before += bit[i]
            i -= i & -i

        # Contribution: sum of edge costs from smaller_before + 1 to x - 1.
        ans += (x - 1) * x // 2 - smaller_before * (smaller_before + 1) // 2

        # Insert current value x.
        i = x
        while i <= n:
            bit[i] += 1
            i += i & -i

    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    main()