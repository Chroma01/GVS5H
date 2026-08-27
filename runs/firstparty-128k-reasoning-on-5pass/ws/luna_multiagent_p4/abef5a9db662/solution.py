import sys


def solve():
    it = iter(map(int, sys.stdin.buffer.read().split()))

    n = next(it)
    contests = [(next(it), next(it)) for _ in range(n)]

    q = next(it)
    queries = [next(it) for _ in range(q)]

    order = sorted(range(q), key=queries.__getitem__)
    values = [queries[i] for i in order]

    size = 4 * q + 5
    seg = [0] * size
    lazy = [0] * size

    def build(node, left, right):
        if left == right:
            seg[node] = values[left]
            return
        mid = (left + right) // 2
        build(node * 2, left, mid)
        build(node * 2 + 1, mid + 1, right)
        seg[node] = max(seg[node * 2], seg[node * 2 + 1])

    def push(node):
        v = lazy[node]
        if v:
            lc = node * 2
            rc = lc + 1
            seg[lc] += v
            seg[rc] += v
            lazy[lc] += v
            lazy[rc] += v
            lazy[node] = 0

    def add(node, left, right, ql, qr):
        if ql <= left and right <= qr:
            seg[node] += 1
            lazy[node] += 1
            return

        push(node)
        mid = (left + right) // 2
        if ql <= mid:
            add(node * 2, left, mid, ql, qr)
        if mid < qr:
            add(node * 2 + 1, mid + 1, right, ql, qr)
        seg[node] = max(seg[node * 2], seg[node * 2 + 1])

    def first_ge(threshold):
        if seg[1] < threshold:
            return q

        node = 1
        left = 0
        right = q - 1
        while left < right:
            push(node)
            mid = (left + right) // 2
            if seg[node * 2] >= threshold:
                node = node * 2
                right = mid
            else:
                node = node * 2 + 1
                left = mid + 1
        return left

    def first_gt(threshold):
        if seg[1] <= threshold:
            return q

        node = 1
        left = 0
        right = q - 1
        while left < right:
            push(node)
            mid = (left + right) // 2
            if seg[node * 2] > threshold:
                node = node * 2
                right = mid
            else:
                node = node * 2 + 1
                left = mid + 1
        return left

    build(1, 0, q - 1)

    for l, r in contests:
        begin = first_ge(l)
        end = first_gt(r) - 1
        if begin <= end:
            add(1, 0, q - 1, begin, end)

    answers = [0] * q

    def collect(node, left, right, carry):
        if left == right:
            answers[order[left]] = seg[node] + carry
            return

        carry += lazy[node]
        mid = (left + right) // 2
        collect(node * 2, left, mid, carry)
        collect(node * 2 + 1, mid + 1, right, carry)

    collect(1, 0, q - 1, 0)
    sys.stdout.write("\n".join(map(str, answers)))


if __name__ == "__main__":
    solve()