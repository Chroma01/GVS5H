import sys
import math


def write_values(vals, mapping=None):
    write = sys.stdout.write
    out = []
    append = out.append

    if mapping is None:
        for x in vals:
            append(str(x))
            if len(out) >= 100000:
                write("\n".join(out))
                write("\n")
                out.clear()
    else:
        mp = mapping
        for x in vals:
            append(str(mp[x]))
            if len(out) >= 100000:
                write("\n".join(out))
                write("\n")
                out.clear()

    if out:
        write("\n".join(out))
        write("\n")


def main():
    it = map(int, sys.stdin.buffer.read().split())
    try:
        N = next(it)
    except StopIteration:
        return
    K = next(it)
    A = list(it)
    del it

    if K == 1:
        write_values(A)
        return

    if K == N:
        gcd = math.gcd
        g = 0
        for x in A:
            g = gcd(g, x)
            if g == 1:
                break
        sys.stdout.write((str(g) + "\n") * N)
        return

    M = max(A)
    freq = [0] * (M + 1)
    f = freq
    rem = 0

    for x in A:
        if f[x] == 0:
            rem += 1
        f[x] += 1

    if rem == 1:
        sys.stdout.write((str(A[0]) + "\n") * N)
        return

    M1 = M + 1
    rng = range

    # best[v] == 0  : present value v, answer not assigned yet
    # best[v] == -1 : absent value, never needs assignment
    # best[v] > 0   : answer already assigned
    best = [0 if f[i] else -1 for i in rng(M1)]
    b = best

    k = K
    unassigned_max = M

    for g in rng(M, 0, -1):
        # No unassigned present value can have a divisor larger than itself.
        if g > unassigned_max:
            continue

        s = 0
        for m in rng(g, M1, g):
            s += f[m]
            if s >= k:
                # g is valid. Assign it to all still-unassigned present multiples.
                for m2 in rng(g, M1, g):
                    if not b[m2]:
                        b[m2] = g
                        rem -= 1
                        if rem == 0:
                            break

                if rem == 0:
                    break
                break

        if s >= k:
            if rem == 0:
                break

            # Lower the maximum unassigned present value after assignments.
            while unassigned_max > 0 and (f[unassigned_max] == 0 or b[unassigned_max]):
                unassigned_max -= 1

    del freq, f
    write_values(A, b)


if __name__ == "__main__":
    main()