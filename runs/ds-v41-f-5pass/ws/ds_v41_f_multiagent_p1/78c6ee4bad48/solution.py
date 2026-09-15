import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = list(map(int, data[1:1 + n]))

    # gaps between consecutive sorted coordinates: g_j = x[j] - x[j-1], 1-based j
    odd = []   # gap indices 1, 3, 5, ...
    even = []  # gap indices 2, 4, 6, ...
    for j in range(1, n):
        g = x[j] - x[j - 1]
        if j & 1:
            odd.append(g)
        else:
            even.append(g)

    # Sum of coordinates = n*x[0] + sum_j g_j * (n - j)
    # The operation only swaps g_i and g_{i+2}, so each parity class is freely
    # permutable. To minimise the weighted sum, give larger gaps to later
    # positions (smaller weight n - j).
    total = n * x[0]

    odd.sort(reverse=True)
    even.sort(reverse=True)

    mo = len(odd)
    for t in range(mo):
        # t-th largest gap goes to the t-th largest odd index (descending)
        idx_desc = 2 * (mo - 1 - t) + 1
        total += odd[t] * (n - idx_desc)

    me = len(even)
    for t in range(me):
        idx_desc = 2 * (me - 1 - t) + 2
        total += even[t] * (n - idx_desc)

    sys.stdout.write(str(total) + "\n")


main()