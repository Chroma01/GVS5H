import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    a = data[2:2 + n]

    tree = [0] * (m + 1)          # Fenwick tree over values 0..m-1 (1-indexed)
    c = [0] * m                   # count of each value
    S = [0] * m                   # sum of 0-indexed positions of each value

    inv = 0
    total = 0
    for i in range(n):
        x = int(a[i])
        # count of already-seen values <= x  (strictly greater contribute inversions)
        s = 0
        j = x + 1
        while j > 0:
            s += tree[j]
            j -= j & (-j)
        inv += total - s
        j = x + 1
        while j <= m:
            tree[j] += 1
            j += j & (-j)
        total += 1
        c[x] += 1
        S[x] += i

    out = [str(inv)]
    ans = inv
    # For k=1..M-1 apply delta for v = M-1, M-2, ..., 1
    for k in range(1, m):
        v = m - k
        ans += 2 * S[v] - c[v] * (n - 1)
        out.append(str(ans))

    sys.stdout.write("\n".join(out) + "\n")

main()