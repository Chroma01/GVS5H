import sys
import numpy as np

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    # read the set of distinct integers
    S = np.fromiter((int(next(it)) for _ in range(n)), dtype=np.int64, count=n)

    max_val = int(S.max())

    # length of FFT (power of two > 2*max_val)
    size = 1
    while size <= max_val * 2:
        size <<= 1

    # characteristic array P[i] = 1 iff i ∈ S
    arr = np.zeros(size, dtype=np.float64)
    arr[S] = 1.0

    # convolution C = P * P  (C[s] = number of ordered pairs with sum s)
    spectrum = np.fft.rfft(arr)                # forward FFT
    conv = np.fft.irfft(spectrum * spectrum, n=size)  # inverse FFT
    conv = np.rint(conv).astype(np.int64)      # round to nearest integer

    # for each middle element B we need unordered pairs {A, C} with A + C = 2·B
    # unordered count = (C[2·B] - 1) // 2
    twice = S * 2
    ordered = conv[twice]                     # C[2·B] for all B
    unordered = (ordered - 1) // 2
    ans = int(unordered.sum())

    sys.stdout.write(str(ans))

if __name__ == "__main__":
    solve()