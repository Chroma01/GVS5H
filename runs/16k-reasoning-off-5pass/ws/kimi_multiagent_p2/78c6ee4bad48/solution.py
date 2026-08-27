import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = list(map(int, data[1:1 + n]))
    gaps = [x[i + 1] - x[i] for i in range(n - 1)]
    # parity classes of gap indices (0-based): even indices <-> original odd positions
    even_class = sorted(gaps[0::2])
    odd_class = sorted(gaps[1::2])
    ans = n * x[0]
    # weights: gap at 0-based index j has weight (n - 1 - j), decreasing in j.
    # Assign ascending gaps to ascending positions within each parity class (rearrangement inequality).
    for idx, g in enumerate(even_class):
        j = 2 * idx
        ans += (n - 1 - j) * g
    for idx, g in enumerate(odd_class):
        j = 2 * idx + 1
        ans += (n - 1 - j) * g
    print(ans)

main()