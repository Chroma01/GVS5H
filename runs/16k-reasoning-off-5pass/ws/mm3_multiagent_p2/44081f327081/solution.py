import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it))
    K = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    if N == 0:
        return

    max_a = max(A)
    M = max_a  # we only need up to the maximum value present

    # frequency of each value
    freq = [0] * (M + 1)
    for a in A:
        freq[a] += 1

    # cnt[d] = number of array elements divisible by d
    cnt = [0] * (M + 1)
    M1 = M + 1
    freq_local = freq
    cnt_local = cnt
    for d in range(1, M1):
        s = 0
        for m in range(d, M1, d):
            s += freq_local[m]
        cnt_local[d] = s

    # best[v] = largest divisor d of v with cnt[d] >= K
    best = [0] * (M1)
    best_local = best
    # Process d in increasing order; later (larger) d will overwrite earlier ones
    for d in range(1, M1):
        if cnt_local[d] >= K:
            # assign d to all multiples of d
            for m in range(d, M1, d):
                best_local[m] = d

    # Output answers
    out = []
    append = out.append
    for a in A:
        append(str(best[a]))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()