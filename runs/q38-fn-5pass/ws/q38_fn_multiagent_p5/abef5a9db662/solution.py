import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    p = 0
    N = data[p]
    p += 1

    M = 500000

    # Fenwick tree over the difference array D.
    # Initially D[i] = 1 for all i, so prefix sums are A[x] = x.
    bit = [0] + [i & -i for i in range(1, M + 1)]

    # Keep the difference array explicitly as well, so final answers
    # can be obtained by one O(M) prefix-sum pass instead of Q Fenwick sums.
    diff = [0] + [1] * M

    top = 1 << (M.bit_length() - 1)

    def find_ge(target, bit=bit, M=M, top=top):
        """Smallest index i such that prefix_sum(i) >= target.
        Returns M + 1 if no such index exists.
        """
        idx = 0
        acc = 0
        step = top
        while step:
            nxt = idx + step
            if nxt <= M and acc + bit[nxt] < target:
                acc += bit[nxt]
                idx = nxt
            step >>= 1
        return idx + 1

    find = find_ge

    for _ in range(N):
        L = data[p]
        R = data[p + 1]
        p += 2

        l = find(L)
        r = find(R + 1) - 1

        if l <= r:
            # Fenwick point update: D[l] += 1
            i = l
            while i <= M:
                bit[i] += 1
                i += i & -i
            diff[l] += 1

            # Fenwick point update: D[r + 1] -= 1
            if r < M:
                rp = r + 1
                i = rp
                while i <= M:
                    bit[i] -= 1
                    i += i & -i
                diff[rp] -= 1

    # Convert difference array to final ratings for all initial ratings.
    cur = 0
    for i in range(1, M + 1):
        cur += diff[i]
        diff[i] = cur

    Q = data[p]
    p += 1

    out = []
    append = out.append
    ans = diff

    for _ in range(Q):
        x = data[p]
        p += 1
        append(str(ans[x]))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()