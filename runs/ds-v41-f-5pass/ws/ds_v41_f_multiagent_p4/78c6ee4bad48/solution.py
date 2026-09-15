import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = list(map(int, data[1:1 + n]))

    odd_g = []
    odd_w = []
    even_g = []
    even_w = []
    for k in range(n - 1):
        j = k + 1                # 1-based gap index
        d = x[k + 1] - x[k]      # positive gap
        if j & 1:                # odd position in 1-based indexing
            odd_g.append(d)
            odd_w.append(n - j)  # coefficient of d_j in the sum
        else:
            even_g.append(d)
            even_w.append(n - j)

    # rearrangement inequality: largest gap with smallest weight
    odd_g.sort(reverse=True)
    odd_w.sort()
    even_g.sort(reverse=True)
    even_w.sort()

    total = n * x[0]             # first piece never moves
    total += sum(g * w for g, w in zip(odd_g, odd_w))
    total += sum(g * w for g, w in zip(even_g, even_w))
    print(total)

main()