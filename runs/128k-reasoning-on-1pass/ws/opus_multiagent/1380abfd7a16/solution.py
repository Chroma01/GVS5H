import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    if n == 0:
        sys.stdout.write("")
        return
    P = list(map(int, data[1:n + 1]))

    size = 1
    while size < n:
        size <<= 1

    tree = [0] * (2 * size)
    tree[size:size + n] = [1] * n
    # bottom-up build, level by level (slice based, fast)
    w = size
    while w > 1:
        half = w >> 1
        tree[half:w] = [a + b for a, b in zip(tree[w:2 * w:2], tree[w + 1:2 * w:2])]
        w = half

    A = [0] * n
    t = tree
    sz = size

    for i in range(n, 0, -1):
        k = P[i - 1]
        node = 1
        t[1] -= 1
        while node < sz:
            node <<= 1
            lv = t[node]
            if lv >= k:
                t[node] = lv - 1
            else:
                k -= lv
                node += 1
                t[node] -= 1
        A[node - sz] = i

    sys.stdout.write(' '.join(map(str, A)))

main()