import sys
import numpy as np

def main():
    input = sys.stdin.readline
    N_line = input().strip()
    while N_line == '':
        N_line = input().strip()
    N = int(N_line)
    A = list(map(int, input().split()))
    maxA = max(A)
    size = maxA + 1

    # frequency array
    cnt = np.zeros(size, dtype=np.int64)
    for a in A:
        cnt[a] += 1

    # FFT size (next power of two >= 2*maxA+1)
    L = 1
    while L < 2 * maxA + 1:
        L <<= 1

    # real input array for FFT
    a = np.zeros(L, dtype=np.float64)
    a[:size] = cnt.astype(np.float64)

    # convolution via real FFT: rfft -> square -> irfft
    A_fft = np.fft.rfft(a)
    A_fft *= A_fft
    conv = np.fft.irfft(A_fft, n=L)  # float64 result

    # we only need up to 2*maxA (inclusive)
    needed = 2 * maxA + 1
    ordered = np.rint(conv[:needed]).astype(np.int64)  # ordered pair counts

    # free memory
    del a, A_fft, conv

    # build index array S = 0..2*maxA
    S = np.arange(needed, dtype=np.int64)

    # mask for odd sums
    odd_mask = (S & 1) == 1

    # unordered pair count array
    unordered = np.zeros(needed, dtype=np.int64)

    # for odd S: unordered = ordered // 2
    unordered[odd_mask] = ordered[odd_mask] // 2

    # for even S: unordered = (ordered + cnt[S//2]) // 2
    even_mask = ~odd_mask
    # cnt[S//2] is safe because S//2 <= maxA
    half = cnt[S[even_mask] // 2]   # fancy indexing returns int64 array
    unordered[even_mask] = (ordered[even_mask] + half) // 2

    # compute odd part for each S: odd = S // (S & -S)
    # For S=0, lowbit would be 0, but we never use it; we set lowbit[0]=1 to avoid div0
    lowbit = np.where(S == 0, np.int64(1), S & (-S))
    odd_part = S // lowbit

    # final answer
    ans = np.sum(unordered * odd_part, dtype=np.int64)
    print(int(ans))

if __name__ == "__main__":
    main()