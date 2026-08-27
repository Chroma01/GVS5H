import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    P = data[1:1 + n]
    tree = [0] * (n + 2)
    total = 0
    for idx in range(n):
        p = int(P[idx])
        # s = number of already-seen elements with value < p
        s = 0
        j = p - 1
        while j > 0:
            s += tree[j]
            j -= j & -j
        L = idx - s          # number of earlier elements greater than p
        if L:
            total += L * idx - (L * (L - 1) >> 1)
        j = p
        while j <= n:
            tree[j] += 1
            j += j & -j
    sys.stdout.write(str(total) + "\n")

main()