import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M = data[0], data[1]
    A = data[2:2 + N]

    # Fenwick tree over values 0..M-1, stored at indices 1..M.
    bit = [0] * (M + 1)
    inv = 0

    for i, x in enumerate(A):
        idx = x + 1

        # Count previous elements <= x.
        s = 0
        j = idx
        while j > 0:
            s += bit[j]
            j -= j & -j

        # Previous elements > x form inversions with current element.
        inv += i - s

        # Add current value.
        j = idx
        while j <= M:
            bit[j] += 1
            j += j & -j

    # delta[v] = total change when elements with original value v wrap.
    # For 1-indexed position p, contribution is 2*p - N - 1.
    delta = [0] * M
    for p, x in enumerate(A, 1):
        delta[x] += 2 * p - N - 1

    out = [str(inv)]
    cur = inv

    # From k to k+1, elements with current value M-1 wrap.
    # Current value M-1 corresponds to original value M-1-k.
    for k in range(M - 1):
        cur += delta[M - 1 - k]
        out.append(str(cur))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()