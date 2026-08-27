import sys


def main():
    input = sys.stdin.buffer.readline

    line = input()
    if not line:
        return
    N = int(line)

    A = list(map(int, input().split()))
    while len(A) < N:
        A.extend(map(int, input().split()))
    if len(A) > N:
        A = A[:N]

    Q = int(input())

    # f[i] = first index j such that A[j] >= 2 * A[i], or N if none.
    f = [0] * N
    j = 0
    for i in range(N):
        if j < i + 1:
            j = i + 1
        target = A[i] * 2
        while j < N and A[j] < target:
            j += 1
        f[i] = j

    # F[r] = last i such that f[i] <= r + 1.
    F = [-1] * N
    i = 0
    for r in range(N):
        limit = r + 1
        while i < N and f[i] <= limit:
            i += 1
        F[r] = i - 1

    # Iterative max segment tree over g[i] = f[i] - i.
    size = 1
    while size < N:
        size <<= 1

    NEG = -10**18
    seg = [NEG] * (size << 1)
    base = size

    for i in range(N):
        seg[base + i] = f[i] - i

    for idx in range(base - 1, 0, -1):
        left = seg[idx << 1]
        right = seg[(idx << 1) | 1]
        seg[idx] = left if left >= right else right

    del A, f

    tokens = sys.stdin.buffer.read().split()

    out = []
    append = out.append

    seg_local = seg
    size_local = size
    F_local = F
    neg = NEG
    to_int = int

    for idx in range(0, 2 * Q, 2):
        L = to_int(tokens[idx])
        R = to_int(tokens[idx + 1])

        l = L - 1
        r = R - 1

        # Maximum possible top-end index by the "at most half of the items" bound.
        P = (l + r - 1) >> 1

        T = F_local[r]
        if T > P:
            T = P

        if T < l:
            append("0")
            continue

        # Range maximum of g on [l, T].
        left = l + size_local
        right = T + size_local
        mx = neg

        while left <= right:
            if left & 1:
                v = seg_local[left]
                if v > mx:
                    mx = v
                left += 1
            if not (right & 1):
                v = seg_local[right]
                if v > mx:
                    mx = v
                right -= 1
            left >>= 1
            right >>= 1

        p0 = r - mx
        if p0 > T:
            p0 = T

        ans = p0 - l + 1
        if ans < 0:
            ans = 0
        append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()