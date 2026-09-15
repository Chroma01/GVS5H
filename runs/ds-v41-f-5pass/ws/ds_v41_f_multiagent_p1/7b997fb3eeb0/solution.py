import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    A = data[1:1 + n]
    q = data[1 + n]
    ptr = 1 + n + 1

    # gap[i] = nxt[i] - i, where nxt[i] is the first index with A[nxt] >= 2*A[i]
    gap = [0] * n
    j = 0
    for i in range(n):
        target = A[i] * 2
        while j < n and A[j] < target:
            j += 1
        gap[i] = j - i

    # Sparse table for range maximum of gap
    table = [gap]
    j = 1
    while (1 << j) <= n:
        prev = table[-1]
        half = 1 << (j - 1)
        curr = list(map(max, prev, prev[half:]))
        table.append(curr)
        j += 1

    # log table for O(1) length to exponent
    log = [0] * (n + 1)
    for i in range(2, n + 1):
        log[i] = log[i >> 1] + 1

    pow2 = [1 << k for k in range(len(table))]

    out = []
    append = out.append

    for _ in range(q):
        L = data[ptr] - 1
        R = data[ptr + 1] - 1
        ptr += 2

        # Check if even K = 1 is possible (t = L)
        if L + gap[L] > R:
            append("0")
            continue

        upper = (L + R - 1) // 2
        lo = L
        hi = upper
        while lo < hi:
            mid = (lo + hi + 1) >> 1
            length = mid - L + 1
            k = log[length]
            row = table[k]
            mx = row[L]
            idx2 = mid - pow2[k] + 1
            v = row[idx2]
            if v > mx:
                mx = v
            if mid + mx <= R:
                lo = mid
            else:
                hi = mid - 1

        append(str(lo - L + 1))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()