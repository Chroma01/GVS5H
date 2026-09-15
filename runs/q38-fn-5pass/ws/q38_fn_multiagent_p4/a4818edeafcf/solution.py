import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    data[0] = 0
    A = data  # 1-indexed: A[1..N]

    # L[i] = number of distinct values in A[1..i]
    L = [0] * (N + 1)
    seen = bytearray(N + 1)
    cnt = 0
    for i in range(1, N + 1):
        x = A[i]
        if not seen[x]:
            seen[x] = 1
            cnt += 1
        L[i] = cnt

    # R[i] = number of distinct values in A[i..N]
    R = [0] * (N + 2)
    seen = bytearray(N + 1)
    cnt = 0
    for i in range(N, 0, -1):
        x = A[i]
        if not seen[x]:
            seen[x] = 1
            cnt += 1
        R[i] = cnt

    # Segment tree over first cuts.
    #
    # For active first cut i, maintain:
    #   value(i) = L[i] + distinct(A[i+1..j])
    #
    # Instead of lazy range-add, maintain a difference array D of suffix adds.
    # value(i) = L[i] + prefix_sum_D(i).
    #
    # Each node stores:
    #   sumv[node] = sum of D in its interval
    #   best[node] = max over active positions p in its interval of
    #                L[p] + sum of D from interval start to p
    #
    # Combine:
    #   sum = left.sum + right.sum
    #   best = max(left.best, left.sum + right.best)
    #
    # The -1 boundary of a suffix add is postponed until that position itself
    # becomes active.  This is safe because active first cuts always form a
    # prefix, so a boundary to the right cannot affect current active values.
    NEG = -10**9
    size = 1 << (N - 1).bit_length()
    offset = size - 1
    sumv = [0] * (2 * size)
    best = [NEG] * (2 * size)

    def activate(pos, sumv=sumv, best=best, offset=offset, L=L):
        k = pos + offset
        if pos == 1:
            best[k] = L[pos]
        else:
            # Postponed boundary -1 from second cut pos.
            sumv[k] = -1
            best[k] = L[pos] - 1

        k >>= 1
        while k:
            left = k << 1
            right = left + 1
            s = sumv[left]
            sumv[k] = s + sumv[right]
            val = s + best[right]
            lb = best[left]
            best[k] = lb if lb >= val else val
            k >>= 1

    def add_one(pos, sumv=sumv, best=best, offset=offset):
        k = pos + offset
        sumv[k] += 1
        best[k] += 1

        k >>= 1
        while k:
            left = k << 1
            right = left + 1
            s = sumv[left]
            sumv[k] = s + sumv[right]
            val = s + best[right]
            lb = best[left]
            best[k] = lb if lb >= val else val
            k >>= 1

    # Previous occurrence of A[j] is maintained on the fly.
    last = [0] * (N + 1)
    last[A[1]] = 1

    ans = 0
    act = activate
    add = add_one
    best_arr = best
    R_arr = R
    A_arr = A
    last_arr = last

    # Second cut j: 2 <= j <= N-1.
    for j in range(2, N):
        x = A_arr[j]
        p = last_arr[x]
        last_arr[x] = j

        m = j - 1          # newly valid first cut
        act(m)

        # A[j] contributes to middle distinct count for first cuts i >= p.
        # If p == 0, it contributes for all active i.
        l = p if p else 1
        add(l)

        cur = best_arr[1] + R_arr[j + 1]
        if cur > ans:
            ans = cur

    print(ans)


if __name__ == "__main__":
    main()