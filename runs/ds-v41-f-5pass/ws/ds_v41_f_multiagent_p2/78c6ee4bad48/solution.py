import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = list(map(int, data[1:1 + n]))

    x1 = x[0]
    gaps = [x[i + 1] - x[i] for i in range(n - 1)]

    # 1-based gap index j: gap j = gaps[j-1].
    # odd-indexed gaps j = 1,3,5,... -> gaps[0], gaps[2], ...
    # even-indexed gaps j = 2,4,6,... -> gaps[1], gaps[3], ...
    odd = sorted(gaps[0::2])
    even = sorted(gaps[1::2])

    total = n * x1
    for k, g in enumerate(odd):
        j = 2 * k + 1          # weight n - j
        total += (n - j) * g
    for k, g in enumerate(even):
        j = 2 * k + 2          # weight n - j
        total += (n - j) * g

    sys.stdout.write(str(total) + "\n")

main()