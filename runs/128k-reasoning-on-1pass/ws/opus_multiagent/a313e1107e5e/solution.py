import sys
from bisect import bisect_left, bisect_right

def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    n = int(data[pos]); pos += 1
    q = int(data[pos]); pos += 1
    A = data[pos:pos + n]
    pos += n
    # queries
    Rs = [0] * q
    Xs = [0] * q
    # linked list buckets by R
    head = [-1] * (n + 1)
    nxt = [-1] * q
    for i in range(q):
        r = int(data[pos]); pos += 1
        x = int(data[pos]); pos += 1
        Rs[i] = r
        Xs[i] = x
        nxt[i] = head[r]
        head[r] = i

    ans = [0] * q
    tails = []
    bl = bisect_left
    br = bisect_right
    ap = None
    for i in range(1, n + 1):
        a = int(A[i - 1])
        p = bl(tails, a)
        if p == len(tails):
            tails.append(a)
        else:
            tails[p] = a
        j = head[i]
        while j != -1:
            ans[j] = br(tails, Xs[j])
            j = nxt[j]

    sys.stdout.write('\n'.join(map(str, ans)))
    sys.stdout.write('\n')

main()