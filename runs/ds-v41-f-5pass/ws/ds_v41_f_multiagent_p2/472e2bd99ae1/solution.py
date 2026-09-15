import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); K = int(data[1])
    A = sorted(map(int, data[2:2+N]), reverse=True)
    B = sorted(map(int, data[2+N:2+2*N]), reverse=True)
    C = sorted(map(int, data[2+2*N:2+3*N]), reverse=True)
    del data

    # Only the top M = min(N, K) of each sequence can influence the K-th value.
    M = K if K < N else N
    A = A[:M]; B = B[:M]; C = C[:M]
    M = len(A)

    a0 = A[0]; b0 = B[0]; c0 = C[0]
    BIG = 1 << 62            # > max possible value 3*10^18
    SH = 54                  # code uses 54 bits (18 per coordinate, M < 2^18)
    HM = (1 << 54) - 1
    MSK = (1 << 18) - 1
    I36 = 1 << 36
    I18 = 1 << 18

    heap = [((BIG - (a0*b0 + b0*c0 + c0*a0)) << SH)]
    push = heapq.heappush
    pop = heapq.heappop
    cnt = 0
    out = sys.stdout

    while True:
        key = pop(heap)
        cnt += 1
        if cnt == K:
            out.write(str(BIG - (key >> SH)))
            out.write("\n")
            return
        code = key & HM
        i = code >> 36
        j = (code >> 18) & MSK
        k = code & MSK
        # push (i+1, j, k) always
        if i + 1 < M:
            ni = i + 1
            bj = B[j]; ck = C[k]; an = A[ni]
            v = an*bj + bj*ck + ck*an
            push(heap, ((BIG - v) << SH) | (code + I36))
        if i == 0:
            # push (0, j+1, k) only when i == 0
            if j + 1 < M:
                nj = j + 1
                ck = C[k]; bn = B[nj]
                v = a0*bn + bn*ck + ck*a0
                push(heap, ((BIG - v) << SH) | (code + I18))
            # push (0, 0, k+1) only when i == j == 0
            if j == 0 and k + 1 < M:
                nk = k + 1
                cn = C[nk]
                v = a0*b0 + b0*cn + cn*a0
                push(heap, ((BIG - v) << SH) | (code + 1))

main()