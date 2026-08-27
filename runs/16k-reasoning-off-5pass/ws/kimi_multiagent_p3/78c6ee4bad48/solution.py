import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = list(map(int, data[1:1 + n]))
    # gaps d_j = x_{j+1} - x_j for j = 1..n-1 (1-indexed)
    odd = []  # gaps at odd j
    even = []  # gaps at even j
    for j in range(1, n):
        d = x[j] - x[j - 1]
        if j & 1:
            odd.append(d)
        else:
            even.append(d)
    # To minimize sum (n-j)*d_j with weights decreasing in j,
    # pair smallest gaps with largest weights (smallest j): sort ascending,
    # assign to positions of the same parity in ascending j order.
    odd.sort()
    even.sort()
    total = n * x[0]
    oi = ei = 0
    for j in range(1, n):
        if j & 1:
            d = odd[oi]; oi += 1
        else:
            d = even[ei]; ei += 1
        total += (n - j) * d
    print(total)

main()