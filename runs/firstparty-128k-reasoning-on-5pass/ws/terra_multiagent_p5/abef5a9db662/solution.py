import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    contests = [(next(it), next(it)) for _ in range(n)]

    q = next(it)
    queries = [next(it) for _ in range(q)]

    order = sorted(range(q), key=lambda i: queries[i])
    initial = [queries[i] for i in order]

    size = 1
    while size < q:
        size <<= 1

    neg_inf = -10**18
    mx = [neg_inf] * (size * 2)
    lazy = [0] * (size * 2)

    for i, x in enumerate(initial):
        mx[size + i] = x

    for k in range(size - 1, 0, -1):
        mx[k] = max(mx[k << 1], mx[k << 1 | 1])

    def push(k):
        z = lazy[k]
        if z:
            left = k << 1
            right = left | 1
            mx[left] += z
            mx[right] += z
            lazy[left] += z
            lazy[right] += z
            lazy[k] = 0

    def range_add(k, left, right, ql, qr):
        if ql <= left and right <= qr:
            mx[k] += 1
            lazy[k] += 1
            return

        push(k)
        mid = (left + right) >> 1

        if ql < mid:
            range_add(k << 1, left, mid, ql, qr)
        if mid < qr:
            range_add(k << 1 | 1, mid, right, ql, qr)

        mx[k] = max(mx[k << 1], mx[k << 1 | 1])

    def first_at_least(x):
        if mx[1] < x:
            return q

        k = 1
        while k < size:
            push(k)
            left = k << 1
            if mx[left] >= x:
                k = left
            else:
                k = left | 1

        return k - size

    for l, r in contests:
        a = first_at_least(l)
        b = first_at_least(r + 1)
        if a < b:
            range_add(1, 0, size, a, b)

    sorted_answers = [0] * q
    for i in range(q):
        k = size + i
        value = mx[k]
        while k > 1:
            k >>= 1
            value += lazy[k]
        sorted_answers[i] = value

    answers = [0] * q
    for sorted_index, original_index in enumerate(order):
        answers[original_index] = sorted_answers[sorted_index]

    sys.stdout.write("\n".join(map(str, answers)))

if __name__ == "__main__":
    main()