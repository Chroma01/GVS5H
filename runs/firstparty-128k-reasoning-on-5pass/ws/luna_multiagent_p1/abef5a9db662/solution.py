import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    contests = [(next(it), next(it)) for _ in range(n)]
    q = next(it)
    queries = [next(it) for _ in range(q)]

    M = 500000
    size = 1
    while size < M:
        size <<= 1

    tree = [0] * (2 * size)
    lazy = [0] * (2 * size)

    tree[size:size + M] = range(1, M + 1)
    for i in range(size - 1, 0, -1):
        tree[i] = max(tree[i << 1], tree[i << 1 | 1])

    def push(node):
        value = lazy[node]
        if value:
            left = node << 1
            right = left | 1
            tree[left] += value
            lazy[left] += value
            tree[right] += value
            lazy[right] += value
            lazy[node] = 0

    def first_at_least(node, left, right, value):
        if tree[node] < value:
            return size + 1
        if left == right:
            return left

        push(node)
        mid = (left + right) >> 1
        child = node << 1
        if tree[child] >= value:
            return first_at_least(child, left, mid, value)
        return first_at_least(child | 1, mid + 1, right, value)

    def range_add(node, left, right, ql, qr):
        if ql <= left and right <= qr:
            tree[node] += 1
            lazy[node] += 1
            return

        push(node)
        mid = (left + right) >> 1
        child = node << 1

        if ql <= mid:
            range_add(child, left, mid, ql, qr)
        if mid < qr:
            range_add(child | 1, mid + 1, right, ql, qr)

        tree[node] = max(tree[child], tree[child | 1])

    for l, r in contests:
        start = first_at_least(1, 1, size, l)
        if start > M:
            continue

        end = first_at_least(1, 1, size, r + 1) - 1
        if end > M:
            end = M

        if start <= end:
            range_add(1, 1, size, start, end)

    answers = []
    for x in queries:
        node = 1
        add = 0
        left = 1
        right = size

        while left != right:
            add += lazy[node]
            mid = (left + right) >> 1
            if x <= mid:
                node <<= 1
                right = mid
            else:
                node = node << 1 | 1
                left = mid + 1

        answers.append(str(tree[node] + add))

    sys.stdout.write("\n".join(answers))


if __name__ == "__main__":
    solve()