import sys


def solve():
    input = sys.stdin.buffer.readline

    n = int(input())
    a = [0] + list(map(int, input().split()))

    prefix = [0] * (n + 1)
    seen = [False] * (n + 1)
    distinct = 0
    for i in range(1, n + 1):
        if not seen[a[i]]:
            seen[a[i]] = True
            distinct += 1
        prefix[i] = distinct

    suffix = [0] * (n + 2)
    seen = [False] * (n + 1)
    distinct = 0
    for i in range(n, 0, -1):
        if not seen[a[i]]:
            seen[a[i]] = True
            distinct += 1
        suffix[i] = distinct

    size = n - 1
    neg_inf = -10**15
    tree = [neg_inf] * (4 * size + 5)
    lazy = [0] * (4 * size + 5)

    def push(node):
        value = lazy[node]
        if value:
            left = node * 2
            right = left + 1
            tree[left] += value
            tree[right] += value
            lazy[left] += value
            lazy[right] += value
            lazy[node] = 0

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

    def range_add(node, left, right, qleft, qright):
        if qleft <= left and right <= qright:
            tree[node] += 1
            lazy[node] += 1
            return

        push(node)
        mid = (left + right) // 2
        if qleft <= mid:
            range_add(node * 2, left, mid, qleft, qright)
        if qright > mid:
            range_add(node * 2 + 1, mid + 1, right, qleft, qright)
        tree[node] = max(tree[node * 2], tree[node * 2 + 1])

    last = [0] * (n + 1)
    last[a[1]] = 1
    answer = 0

    for j in range(2, n):
        first_split = j - 1
        point_set(1, 1, size, first_split, prefix[first_split])

        previous = last[a[j]]
        last[a[j]] = j

        left_bound = max(1, previous)
        range_add(1, 1, size, left_bound, j - 1)

        answer = max(answer, tree[1] + suffix[j + 1])

    print(answer)


if __name__ == "__main__":
    solve()