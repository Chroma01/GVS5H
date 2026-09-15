import sys
from heapq import heappush, heappop


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, K = data[0], data[1]
    A = data[2:2 + N]
    B = data[2 + N:2 + 2 * N]
    C = data[2 + 2 * N:2 + 3 * N]
    del data

    write = sys.stdout.write

    if K == 1:
        a = max(A)
        b = max(B)
        c = max(C)
        write(str(a * b + b * c + c * a) + "\n")
        return

    def compress(arr, K):
        arr.sort(reverse=True)
        vals = []
        mults = []
        va = vals.append
        ma = mults.append

        it = iter(arr)
        prev = next(it)
        cnt = 1
        dup = False

        for v in it:
            if v == prev:
                cnt += 1
            else:
                va(prev)
                ma(cnt if cnt < K else K)
                if cnt > 1:
                    dup = True
                prev = v
                cnt = 1

        va(prev)
        ma(cnt if cnt < K else K)
        if cnt > 1:
            dup = True

        return vals, mults, dup

    va, ma, dup_a = compress(A, K)
    del A
    vb, mb, dup_b = compress(B, K)
    del B
    vc, mc, dup_c = compress(C, K)
    del C

    dims = [
        (len(va), va, ma, dup_a),
        (len(vb), vb, mb, dup_b),
        (len(vc), vc, mc, dup_c),
    ]
    dims.sort(key=lambda t: t[0], reverse=True)

    lx, X, mx, dup_x = dims[0]
    ly, Y, my, dup_y = dims[1]
    lz, Z, mz, dup_z = dims[2]
    del dims, va, vb, vc, ma, mb, mc

    root_val = X[0] * Y[0] + Y[0] * Z[0] + Z[0] * X[0]

    all_one = not (dup_x or dup_y or dup_z)
    if all_one:
        mx = my = mz = None

    max_len = max(lx, ly, lz)
    SHIFT = max(1, (max_len - 1).bit_length())
    MASK = (1 << SHIFT) - 1
    CODE_BITS = 3 * SHIFT
    CODE_MASK = (1 << CODE_BITS) - 1
    DOUBLE_SHIFT = 2 * SHIFT
    I_INC = 1 << DOUBLE_SHIFT
    J_INC = 1 << SHIFT

    heap = [((-root_val) << CODE_BITS)]
    push = heappush
    pop = heappop

    remaining = K
    val = root_val

    while heap:
        key = pop(heap)
        val = -(key >> CODE_BITS)

        if remaining == 1:
            write(str(val) + "\n")
            return

        code = key & CODE_MASK
        k = code & MASK
        j = (code >> SHIFT) & MASK
        i = code >> DOUBLE_SHIFT

        if all_one:
            cnt = 1
        else:
            cnt = mx[i]
            if cnt < remaining:
                cnt *= my[j]
                if cnt < remaining:
                    cnt *= mz[k]

        if cnt >= remaining:
            write(str(val) + "\n")
            return

        remaining -= cnt

        x = X[i]
        y = Y[j]
        z = Z[k]

        ni = i + 1
        if ni < lx:
            nval = val + (X[ni] - x) * (y + z)
            push(heap, ((-nval) << CODE_BITS) + (code + I_INC))

        if i == 0:
            nj = j + 1
            if nj < ly:
                nval = val + (Y[nj] - y) * (x + z)
                push(heap, ((-nval) << CODE_BITS) + (code + J_INC))

            if j == 0:
                nk = k + 1
                if nk < lz:
                    nval = val + (Z[nk] - z) * (x + y)
                    push(heap, ((-nval) << CODE_BITS) + (code + 1))

    # Should be unreachable because the capped total multiplicity is at least K.
    write(str(val) + "\n")


if __name__ == "__main__":
    solve()