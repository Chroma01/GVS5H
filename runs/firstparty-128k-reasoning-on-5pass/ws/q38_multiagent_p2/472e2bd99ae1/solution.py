import sys
from heapq import heappush, heappop, heapreplace


def main():
    write = sys.stdout.write
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    K = data[1]
    p = 2
    A = data[p:p + N]
    p += N
    B = data[p:p + N]
    p += N
    C = data[p:p + N]
    del data

    if K == 1:
        a0 = max(A)
        b0 = max(B)
        c0 = max(C)
        ans = a0 * b0 + b0 * c0 + c0 * a0
        write(str(ans) + "\n")
        return

    A.sort(reverse=True)
    B.sort(reverse=True)
    C.sort(reverse=True)

    M = N if N < K else K
    if M < N:
        del A[M:]
        del B[M:]
        del C[M:]

    if K == M * M * M:
        a = A[-1]
        b = B[-1]
        c = C[-1]
        ans = a * b + b * c + c * a
        write(str(ans) + "\n")
        return

    A0 = A[0]
    root = A0 * B[0] + B[0] * C[0] + C[0] * A0

    dA = [A[i] - A[i + 1] for i in range(M - 1)]
    dB = [B[i] - B[i + 1] for i in range(M - 1)]
    dC = [C[i] - C[i + 1] for i in range(M - 1)]
    del A

    b = (M - 1).bit_length()
    bits = 3 * b
    id_mask = (1 << bits) - 1
    coord_mask = (1 << b) - 1
    shift1 = b
    shift2 = 2 * b
    step_i = 1 << shift2
    step_j = 1 << shift1

    dA0 = dA[0]

    hp = [0]
    push = heappush
    pop = heappop
    replace = heapreplace

    m1 = M - 1
    B_list = B
    C_list = C
    dA_list = dA
    dB_list = dB
    dC_list = dC
    A0_val = A0
    root_val = root
    bits_val = bits
    idmask = id_mask
    cmask = coord_mask
    s1 = shift1
    s2 = shift2
    si = step_i
    sj = step_j

    for _ in range(K - 1):
        key = hp[0]
        diff = key >> bits_val
        idx = key & idmask
        i = idx >> s2

        if i == 0:
            k = idx & cmask
            j = idx >> s1
            bj = B_list[j]
            ck = C_list[k]

            replace(hp, ((diff + dA0 * (bj + ck)) << bits_val) | (idx + si))

            if j < m1:
                push(hp, ((diff + dB_list[j] * (A0_val + ck)) << bits_val) | (idx + sj))
            if j == 0 and k < m1:
                push(hp, ((diff + dC_list[k] * (A0_val + bj)) << bits_val) | (idx + 1))
        elif i < m1:
            k = idx & cmask
            j = (idx >> s1) & cmask
            bj = B_list[j]
            ck = C_list[k]

            replace(hp, ((diff + dA_list[i] * (bj + ck)) << bits_val) | (idx + si))
        else:
            pop(hp)

    key = pop(hp)
    ans = root_val - (key >> bits_val)
    write(str(ans) + "\n")


if __name__ == "__main__":
    main()