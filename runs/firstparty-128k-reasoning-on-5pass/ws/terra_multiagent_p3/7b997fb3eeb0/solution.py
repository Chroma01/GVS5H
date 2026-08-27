import sys
from array import array

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    a = [next(it) for _ in range(n)]

    # F[i]: first index j such that A[j] >= 2*A[i], or n if absent.
    # D[i] = F[i] - i.
    d = array('i')
    j = 0
    for i in range(n):
        target = a[i] * 2
        if j < i:
            j = i
        while j < n and a[j] < target:
            j += 1
        d.append(j - i)

    # Sparse table for range maximum queries on D.
    st = [d]
    length = 1
    while length * 2 <= n:
        prev = st[-1]
        count = n - length * 2 + 1
        cur = array('i', (
            prev[i] if prev[i] >= prev[i + length] else prev[i + length]
            for i in range(count)
        ))
        st.append(cur)
        length *= 2

    log2 = [0] * (n + 1)
    for i in range(2, n + 1):
        log2[i] = log2[i >> 1] + 1

    def range_max(left, right):
        # Half-open interval [left, right).
        size = right - left
        k = log2[size]
        row = st[k]
        v1 = row[left]
        v2 = row[right - (1 << k)]
        return v1 if v1 >= v2 else v2

    q = next(it)
    out = []

    for _ in range(q):
        l = next(it) - 1
        r = next(it) - 1
        size = r - l + 1

        low = 0
        high = size // 2 + 1

        while high - low > 1:
            k = (low + high) // 2

            # For p in [l, l+k), require:
            # F[p] - p <= size - k.
            if range_max(l, l + k) <= size - k:
                low = k
            else:
                high = k

        out.append(str(low))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()