import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    S = sum(A)
    T0 = (n + 1) * S          # sum over i<=j of (A_i + A_j)
    maxsum = 2 * max(A)

    total = 0                  # sum_{k>=1} T_k / 2^k
    LIMIT = 1 << 20
    M = 2
    while M <= maxsum:
        mask = M - 1
        half = M >> 1
        if M <= LIMIT:
            cnt = [0] * M
            sm = [0] * M
            for x in A:
                r = x & mask
                cnt[r] += 1
                sm[r] += x
            acc = 0
            for r in range(M):
                c = cnt[r]
                if c:
                    acc += sm[r] * cnt[(-r) & mask]
            dsum = sm[0] + sm[half]
        else:
            cnt = {}
            sm = {}
            for x in A:
                r = x & mask
                cnt[r] = cnt.get(r, 0) + 1
                sm[r] = sm.get(r, 0) + x
            acc = 0
            for r, c in cnt.items():
                acc += sm[r] * cnt.get((-r) & mask, 0)
            dsum = sm.get(0, 0) + sm.get(half, 0)

        Tk = acc + dsum
        k = M.bit_length() - 1
        total += Tk >> k
        M <<= 1

    print(T0 - total)

main()