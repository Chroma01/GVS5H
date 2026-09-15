import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:2 + n]))

    # ---- inversion count of A (values in [0, m-1]) via Fenwick ----
    size = m  # 1-based indices 1..m, value v -> v+1
    tree = [0] * (size + 1)

    def update(v):
        i = v + 1
        while i <= size:
            tree[i] += 1
            i += i & (-i)

    def query(v):  # count of inserted values <= v
        i = v + 1
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & (-i)
        return s

    inv0 = 0
    inserted = 0
    for v in a:
        inv0 += inserted - query(v)
        update(v)
        inserted += 1

    # ---- per-element wrap contribution ----
    # element i wraps at transition k = M-1-A_i, contributing -(N-2i-1)
    bucket = [0] * (m + 2)
    for i, v in enumerate(a):
        bucket[v + 1] += n - 2 * i - 1

    # prefix sums diff[0..m]; diff[m] == 0 always
    diff = [0] * (m + 2)
    acc = 0
    for j in range(m + 1):
        acc += bucket[j]
        diff[j] = acc

    out = []
    for k in range(m):
        out.append(inv0 + diff[m - k])
    sys.stdout.write("\n".join(map(str, out)) + "\n")

main()