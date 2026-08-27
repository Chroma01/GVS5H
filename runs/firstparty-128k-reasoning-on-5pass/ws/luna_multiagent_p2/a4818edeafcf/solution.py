import sys

def solve():
    input = sys.stdin.buffer.readline
    n = int(input())
    a = [0] + list(map(int, input().split()))

    prefix = [0] * (n + 1)
    seen = [False] * (n + 1)
    count = 0
    for i in range(1, n + 1):
        if not seen[a[i]]:
            seen[a[i]] = True
            count += 1
        prefix[i] = count

    suffix = [0] * (n + 2)
    seen = [False] * (n + 1)
    count = 0
    for i in range(n, 0, -1):
        if not seen[a[i]]:
            seen[a[i]] = True
            count += 1
        suffix[i] = count

    previous = [0] * (n + 1)
    last = [0] * (n + 1)
    for i in range(1, n + 1):
        previous[i] = last[a[i]]
        last[a[i]] = i

    m = n - 2
    neg_inf = -10**15
    size = 4 * m + 5
    tree = [neg_inf] * size
    lazy = [0] * size

    sys.setrecursionlimit(1_000_000)

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

    def set_value(node, left, right, pos, value):
        if left == right:
            tree[node] = value
            return
        push(node)
        mid = (left + right) // 2
        if pos <= mid:
            set_value(node * 2, left, mid, pos, value)
        else:
            set_value(node * 2 + 1, mid + 1, right, pos, value)
        tree[node] = max(tree[node * 2], tree[node * 2 + 1])

    def add_range(node, left, right, ql, qr):
        if ql <= left and right <= qr:
            tree[node] += 1
            lazy[node] += 1
            return
        push(node)
        mid = (left + right) // 2
        if ql <= mid:
            add_range(node * 2, left, mid, ql, qr)
        if mid < qr:
            add_range(node * 2 + 1, mid + 1, right, ql, qr)
        tree[node] = max(tree[node * 2], tree[node * 2 + 1])

    answer = 0

    for j in range(2, n):
        left_boundary = j - 1
        set_value(1, 1, m, left_boundary, prefix[left_boundary])

        start = max(1, previous[j])
        add_range(1, 1, m, start, j - 1)

        answer = max(answer, tree[1] + suffix[j + 1])

    print(answer)

if __name__ == "__main__":
    solve()