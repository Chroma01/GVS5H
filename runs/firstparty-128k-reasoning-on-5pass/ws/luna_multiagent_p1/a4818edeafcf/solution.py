import sys


def solve():
    input = sys.stdin.buffer.readline

    n = int(input())
    a = list(map(int, input().split()))

    pref = [0] * (n + 1)
    seen = [False] * (n + 1)
    count = 0
    for i, x in enumerate(a, 1):
        if not seen[x]:
            seen[x] = True
            count += 1
        pref[i] = count

    suff = [0] * (n + 2)
    seen = [False] * (n + 1)
    count = 0
    for i in range(n, 0, -1):
        x = a[i - 1]
        if not seen[x]:
            seen[x] = True
            count += 1
        suff[i] = count

    size = 4 * (n + 2)
    neg_inf = -10**15
    tree = [neg_inf] * size
    lazy = [0] * size

    def push(node):
        value = lazy[node]
        if value:
            left = node * 2
            right = left + 1
            tree[left] += value
            lazy[left] += value
            tree[right] += value
            lazy[right] += value
            lazy[node] = 0

    def range_add(node, left, right, ql, qr):
        if ql <= left and right <= qr:
            tree[node] += 1
            lazy[node] += 1
            return

        push(node)
        mid = (left + right) // 2
        if ql <= mid:
            range_add(node * 2, left, mid, ql, qr)
        if mid < qr:
            range_add(node * 2 + 1, mid + 1, right, ql, qr)
        tree[node] = max(tree[node * 2], tree[node * 2 + 1])

    def point_set(node, left, right, pos, value):
        if left == right:
            tree[node] = value
            lazy[node] = 0
            return

        push(node)
        mid = (left + right) // 2
        if pos <= mid:
            point_set(node * 2, left, mid, pos, value)
        else:
            point_set(node * 2 + 1, mid + 1, right, pos, value)
        tree[node] = max(tree[node * 2], tree[node * 2 + 1])

    last = [0] * (n + 1)
    last[a[0]] = 1

    answer = 0

    for j in range(2, n):
        x = a[j - 1]
        previous = last[x]

        range_add(1, 1, n - 1, max(1, previous), j - 1)

        # The newly valid first split is i = j - 1.
        point_set(1, 1, n - 1, j - 1, pref[j - 1] + 1)

        last[x] = j
        answer = max(answer, tree[1] + suff[j + 1])

    print(answer)


if __name__ == "__main__":
    solve()