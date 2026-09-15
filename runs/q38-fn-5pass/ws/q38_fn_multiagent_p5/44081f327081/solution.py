import sys
import gc
from math import gcd


def main():
    gc.disable()

    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    K = int(data[1])

    # If only one element is chosen, the GCD is the element itself.
    if K == 1:
        sys.stdout.buffer.write(b"\n".join(data[2:]) + b"\n")
        return

    # If all elements must be chosen, the answer is the GCD of all elements.
    if K == N:
        g = 0
        for tok in data[2:]:
            g = gcd(g, int(tok))
            if g == 1:
                break
        sys.stdout.buffer.write((str(g).encode() + b"\n") * N)
        return

    A = list(map(int, data[2:]))
    del data

    max_a = max(A)

    # All values are 1.
    if max_a == 1:
        sys.stdout.write("1\n" * N)
        return

    # freq[x] will first be the frequency of x, then the number of elements divisible by x.
    freq = [0] * (max_a + 1)
    f = freq

    for x in A:
        f[x] += 1

    # Not strictly needed for d >= 2, but keeps the meaning clear.
    f[1] = N

    ma1 = max_a + 1
    half = max_a // 2

    # Compute counts of multiples in-place.
    # For d <= max_a//2, multiples are > d except d itself, so ascending order
    # guarantees that f[m] for m > d is still the original frequency.
    # For d > max_a//2, the only multiple is d itself, so f[d] is already correct.
    #
    # Hybrid: use slice+sum for small d (mostly C-level work), and explicit
    # loops for larger d to avoid creating hundreds of thousands of tiny slices.
    TH = 10000
    if half >= 2:
        end_small = TH if TH < half else half

        for d in range(2, end_small + 1):
            f[d] = sum(f[d:ma1:d])

        for d in range(end_small + 1, half + 1):
            s = 0
            for m in range(d, ma1, d):
                s += f[m]
            f[d] = s

    # ans[x] = answer for value x.
    # Initialize with 1 because divisor 1 always qualifies (K <= N).
    ans = [1] * (max_a + 1)
    ans_list = ans

    # Assign answers from large divisors to small divisors.
    # The first assignment to a multiple is its largest qualifying divisor.
    for d in range(max_a, 1, -1):
        if f[d] >= K:
            if d > half:
                if ans_list[d] == 1:
                    ans_list[d] = d
            else:
                for m in range(d, ma1, d):
                    if ans_list[m] == 1:
                        ans_list[m] = d

    del freq, f

    # Output in chunks to avoid building one huge list of strings.
    write = sys.stdout.write
    ans_list = ans
    chunk_size = 100000

    for i in range(0, N, chunk_size):
        write("\n".join([str(ans_list[x]) for x in A[i:i + chunk_size]]))
        write("\n")


if __name__ == "__main__":
    main()