import sys


def solve():
    input = sys.stdin.readline
    n = int(input())
    a = list(map(int, input().split()))

    # Prefix distinct counts.
    pref = [0] * (n + 1)
    seen = [False] * (n + 1)
    count = 0
    for i, x in enumerate(a, 1):
        if not seen[x]:
            seen[x] = True
            count += 1
        pref[i] = count

    # Suffix distinct counts.
    suf = [0] * (n + 2)
    seen = [False] * (n + 1)
    count = 0
    for i in range(n, 0, -1):
        x = a[i - 1]
        if not seen[x]:
            seen[x] = True
            count += 1
        suf[i] = count

    # Previous occurrence of every element.
    prev = [0] * (n + 1)
    last = [0] * (n + 1)
    for i, x in enumerate(a, 1):
        prev[i] = last[x]
        last[x] = i

    size = 1
    while size < n:
        size <<= 1

    neg_inf = -10**9
    tree = [neg_inf] * (2 * size)
    lazy = [0] * (2 * size)

    def push(node):
        value = lazy[node]
        if value:
            left = node << 1
            right = left | 1
            tree[left] += value
            tree[right] += value
            lazy[left] += value
            lazy[right] += value
            lazy[node] = 0

    def point_set(node, left, right, pos, value):
        if right - left == 1:
            tree[node] = value
            lazy[node] = 0
            return
        push(node)
        mid = (left + right) >> 1
        if pos < mid:
            point_set(node << 1, left, mid, pos, value)
        else:
            point_set(node << 1 | 1, mid, right, pos, value)
        tree[node] = max(tree[node << 1], tree[node << 1 | 1])

    def range_add(node, left, right, ql, qr, value):
        if ql <= left and right <= qr:
            tree[node] += value
            lazy[node] += value
            return
        push(node)
        mid = (left + right) >> 1
        if ql < mid:
            range_add(node << 1, left, mid, ql, qr, value)
        if mid < qr:
            range_add(node << 1 | 1, mid, right, ql, qr, value)
        tree[node] = max(tree[node << 1], tree[node << 1 | 1])

    answer = 0

    # For each j, activate i = j-1, then extend the middle segment.
    for j in range(2, n):
        i_new = j - 1
        point_set(1, 0, size, i_new, pref[i_new])

        left = max(1, prev[j])
        range_add(1, 0, size, left, j, 1)

        candidate = tree[1] + suf[j + 1]
        if candidate > answer:
            answer = candidate

    print(answer)


if __name__ == "__main__":
    solve()