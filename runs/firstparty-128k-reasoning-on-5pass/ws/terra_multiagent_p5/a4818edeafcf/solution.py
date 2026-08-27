import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = [0] + data[1:]

    pref = [0] * (n + 1)
    seen = [False] * (n + 1)
    cnt = 0
    for i in range(1, n + 1):
        x = a[i]
        if not seen[x]:
            seen[x] = True
            cnt += 1
        pref[i] = cnt

    suff = [0] * (n + 2)
    seen = [False] * (n + 1)
    cnt = 0
    for i in range(n, 0, -1):
        x = a[i]
        if not seen[x]:
            seen[x] = True
            cnt += 1
        suff[i] = cnt

    neg_inf = -10**9
    seg = [neg_inf] * (4 * n + 10)
    lazy = [0] * (4 * n + 10)

    def apply(node, value):
        seg[node] += value
        lazy[node] += value

    def push(node):
        value = lazy[node]
        if value:
            left = node * 2
            apply(left, value)
            apply(left + 1, value)
            lazy[node] = 0

    def point_set(node, left, right, pos, value):
        if left == right:
            seg[node] = value
            lazy[node] = 0
            return
        push(node)
        mid = (left + right) >> 1
        if pos <= mid:
            point_set(node * 2, left, mid, pos, value)
        else:
            point_set(node * 2 + 1, mid + 1, right, pos, value)
        seg[node] = max(seg[node * 2], seg[node * 2 + 1])

    def range_add(node, left, right, ql, qr):
        if ql <= left and right <= qr:
            apply(node, 1)
            return
        push(node)
        mid = (left + right) >> 1
        if ql <= mid:
            range_add(node * 2, left, mid, ql, qr)
        if mid < qr:
            range_add(node * 2 + 1, mid + 1, right, ql, qr)
        seg[node] = max(seg[node * 2], seg[node * 2 + 1])

    last = [0] * (n + 1)
    last[a[1]] = 1
    answer = 0

    for j in range(2, n):
        i = j - 1
        point_set(1, 1, n, i, pref[i])

        x = a[j]
        left = last[x]
        if left == 0:
            left = 1

        range_add(1, 1, n, left, j - 1)
        last[x] = j

        answer = max(answer, seg[1] + suff[j + 1])

    print(answer)

if __name__ == "__main__":
    solve()