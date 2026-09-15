import sys
from math import gcd


def write_list(vals):
    write = sys.stdout.write
    buf = []
    append = buf.append
    for x in vals:
        append(str(x))
        if len(buf) >= 10000:
            write('\n'.join(buf))
            write('\n')
            buf.clear()
    if buf:
        write('\n'.join(buf))
        write('\n')


def write_repeated(val, n):
    write = sys.stdout.write
    s = str(val) + '\n'
    chunk_size = 10000
    chunk = s * chunk_size
    for _ in range(n // chunk_size):
        write(chunk)
    rem = n % chunk_size
    if rem:
        write(s * rem)


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = list(map(int, it))
    del data, it

    if K == 1:
        write_list(A)
        return

    if K == N:
        g = 0
        for x in A:
            g = gcd(g, x)
            if g == 1:
                break
        write_repeated(g, N)
        return

    M = max(A)
    if M == 1:
        write_repeated(1, N)
        return

    if sys.implementation.name == 'cpython':
        import gc
        gc.disable()

    freq = [0] * (M + 1)
    f = freq
    for x in A:
        f[x] += 1

    ans = [1] * (M + 1)
    a = ans
    M1 = M + 1
    k = K

    # Small divisors: use C-level slicing for counting and assignment.
    T = 256
    if T > M:
        T = M

    for d in range(2, T + 1):
        if sum(f[d::d]) >= k:
            a[d::d] = [d] * (M // d)

    start = T + 1

    # Split remaining divisors by the number of multiples they have.
    quarter = M // 4
    third = M // 3
    half = M // 2

    # For manual ranges, slice assignment is useful only when the slice is long enough.
    sa_limit = M // 128

    # floor(M / d) >= 4
    if start <= quarter:
        end = quarter
        for d in range(start, end + 1):
            s = f[d]
            if s < k:
                for m in range(d + d, M1, d):
                    s += f[m]
                    if s >= k:
                        break
            if s >= k:
                if d <= sa_limit:
                    a[d::d] = [d] * (M // d)
                else:
                    for m in range(d, M1, d):
                        a[m] = d
        start = end + 1

    # floor(M / d) == 3
    if start <= third:
        end = third
        for d in range(start, end + 1):
            d2 = d + d
            d3 = d2 + d
            s = f[d]
            if s < k:
                s += f[d2]
                if s < k:
                    s += f[d3]
            if s >= k:
                a[d] = d
                a[d2] = d
                a[d3] = d
        start = end + 1

    # floor(M / d) == 2
    if start <= half:
        end = half
        for d in range(start, end + 1):
            d2 = d + d
            s = f[d]
            if s < k:
                s += f[d2]
            if s >= k:
                a[d] = d
                a[d2] = d
        start = end + 1

    # floor(M / d) == 1
    if start <= M:
        for d in range(start, M1):
            if f[d] >= k:
                a[d] = d

    del freq, f

    write = sys.stdout.write
    buf = []
    append = buf.append
    ans_local = a
    for x in A:
        append(str(ans_local[x]))
        if len(buf) >= 10000:
            write('\n'.join(buf))
            write('\n')
            buf.clear()
    if buf:
        write('\n'.join(buf))
        write('\n')


if __name__ == '__main__':
    main()