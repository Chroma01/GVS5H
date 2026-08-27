import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); m = int(data[1])
    A = list(map(int, data[2:2 + n]))

    cnt = [0] * m
    sumPos = [0] * m
    for i in range(n):
        a = A[i]
        cnt[a] += 1
        sumPos[a] += i + 1

    # Fenwick tree over values 0..m-1, count inversions for k = 0
    tree = [0] * (m + 1)
    inv = 0
    for i in range(n):
        a = A[i]
        # number of already inserted values <= a
        s = 0
        j = a + 1
        while j > 0:
            s += tree[j]
            j -= j & (-j)
        inv += i - s  # values strictly greater than a among first i elements
        j = a + 1
        while j <= m:
            tree[j] += 1
            j += j & (-j)

    ans = [inv]
    for k in range(m - 1):
        v = m - 1 - k
        c = cnt[v]
        inv += 2 * sumPos[v] - c - c * n
        ans.append(inv)

    sys.stdout.write("\n".join(map(str, ans)) + "\n")

main()