import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    A = list(map(int, data[1:]))

    # Ensure the sizes are sorted (the problem statement guarantees this,
    # but sorting does not hurt and protects against malformed input)
    A.sort()

    i = 0          # pointer to the current top (smaller) mochi
    j = 0          # pointer to the smallest possible bottom (larger) mochi
    count = 0      # number of kagamimochi formed

    while i < n:
        # The bottom must be a different mochi, so j must be ahead of i
        if j <= i:
            j = i + 1

        # Find the first bottom that is at least twice the top
        while j < n and A[j] < 2 * A[i]:
            j += 1

        if j == n:          # no suitable bottom left
            break

        # Pair i (top) with j (bottom)
        count += 1
        i += 1
        j += 1

    sys.stdout.write(str(count))

if __name__ == "__main__":
    solve()