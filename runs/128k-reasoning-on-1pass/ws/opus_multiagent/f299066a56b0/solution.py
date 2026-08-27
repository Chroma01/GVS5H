import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    if n < 2:
        sys.stdout.write("0\n")
        return

    h = n // 2
    # Tops can be restricted to the first h elements (indices 0..h-1) and
    # bottoms to the last h elements (indices n-h..n-1), since for any
    # feasible K (<= h) the optimal choice is tops = K smallest, bottoms =
    # K largest, matched in order.  Greedy two-pointer over the two sorted
    # lists yields the maximum matching.
    i = 0
    for j in range(n - h, n):
        if i >= h:
            break
        if 2 * A[i] <= A[j]:
            i += 1
    sys.stdout.write(str(i) + "\n")


main()