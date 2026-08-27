import sys
import numpy as np

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N = data[0]
    A = np.array(data[1:], dtype=np.int64)

    max_a = int(A.max())
    max_sum = max_a * 2

    # frequencies of the original values
    freq = np.bincount(A, minlength=max_a + 1).astype(np.int32)

    # ------------------------------------------------------------
    # 1. convolution freq * freq  (ordered pairs)
    L = 1 << (max_sum + 1).bit_length()          # power of two >= max_sum+1
    a = np.zeros(L, dtype=np.float64)
    a[:max_a + 1] = freq

    A_fft = np.fft.rfft(a)
    A_fft *= A_fft
    np.fft.irfft(A_fft, n=L, out=a)               # result stays in a
    del A_fft

    # ordered pair counts G(s) for s = 0 .. max_sum
    G = np.rint(a[:max_sum + 1]).astype(np.int64)
    del a

    # ------------------------------------------------------------
    # 2. transform to unordered pairs C(s) = (G(s) + D(s)) // 2
    D = np.zeros(max_sum + 1, dtype=np.int32)
    D[0::2] = freq                                 # D[2k] = freq[k]
    G += D                                          # broadcast to int64
    G //= 2
    del D

    # ------------------------------------------------------------
    # 3. odd part of every possible sum
    s_arr = np.arange(max_sum + 1, dtype=np.int32)
    lowbit = s_arr & -s_arr
    odd = np.zeros_like(s_arr, dtype=np.int32)
    odd[1:] = s_arr[1:] // lowbit[1:]               # f(0) = 0, not used later

    # ------------------------------------------------------------
    # 4. final answer
    ans = int(np.sum(odd.astype(np.int64) * G))
    print(ans)


if __name__ == "__main__":
    solve()