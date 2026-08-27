import sys

def solve():
    input = sys.stdin.buffer.readline
    n = int(input())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    seen = [False] * (n + 1)
    cnt = 0
    for i, x in enumerate(a):
        if not seen[x]:
            seen[x] = True
            cnt += 1
        pref[i + 1] = cnt

    suf = [0] * (n + 1)
    seen = [False] * (n + 1)
    cnt = 0
    for i in range(n - 1, -1, -1):
        x = a[i]
        if not seen[x]:
            seen[x] = True
            cnt += 1
        suf[i] = cnt

    size = 4 * n
    neg_inf = -10**15
    seg = [neg_inf] * size
    lazy = [0] * size

    def push(node):
        z = lazy[node]
        if z:
            left = node * 2
            right = left + 1
            seg[left] += z
            lazy[left] += z
            seg[right] += z
            lazy[right] += z
            lazy[node] = 0

    def point_set(node, left, right, pos, value):
        if right - left == 1:
            seg[node] = value
            lazy[node] = 0
            return
        push(node)
        mid = (left + right) // 2
        if pos < mid:
            point_set(node * 2, left, mid, pos, value)
        else:
            point_set(node * 2 + 1, mid, right, pos, value)
        seg[node] = max(seg[node * 2], seg[node * 2 + 1])

    def range_add(node, left, right, ql, qr):
        if ql <= left and right <= qr:
            seg[node] += 1
            lazy[node] += 1
            return
        push(node)
        mid = (left + right) // 2
        if ql < mid:
            range_add(node * 2, left, mid, ql, qr)
        if mid < qr:
            range_add(node * 2 + 1, mid, right, ql, qr)
        seg[node] = max(seg[node * 2], seg[node * 2 + 1])

    last = [-1] * (n + 1)
    last[a[0]] = 0

    ans = 0

    # p is the last index of the middle subarray.
    # Thus the second cut is j = p + 1, and p <= n - 2.
    for p in range(1, n - 1):
        # Activate first cut i = p, for which the middle is initially A[p].
        point_set(1, 0, n, p, pref[p])

        x = a[p]
        left = max(1, last[x] + 1)
        range_add(1, 0, n, left, p + 1)
        last[x] = p

        ans = max(ans, seg[1] + suf[p + 1])

    print(ans)

if __name__ == "__main__":
    solve()