import sys
from array import array


def main():
    it = map(int, sys.stdin.buffer.read().split())
    n = next(it)
    k = next(it)
    values = array('I', it)
    del it

    if k == 1:
        write = sys.stdout.write
        chunk_size = 100000
        for start in range(0, n, chunk_size):
            write('\n'.join(map(str, values[start:start + chunk_size])) + '\n')
        return

    maximum = max(values)
    freq = array('I', [0]) * (maximum + 1)

    remaining = 0
    for x in values:
        if freq[x] == 0:
            remaining += 1
        freq[x] += 1

    ans = array('I', [0]) * (maximum + 1)

    # Descending divisors ensure that the first feasible divisor assigned
    # to a value is its largest possible answer.
    for d in range(maximum, 0, -1):
        count = 0

        # Stop counting as soon as d is known to be feasible.
        # This avoids slices and can save substantial work for small K.
        for multiple in range(d, maximum + 1, d):
            count += freq[multiple]
            if count >= k:
                break

        if count < k:
            continue

        for multiple in range(d, maximum + 1, d):
            if freq[multiple] and ans[multiple] == 0:
                ans[multiple] = d
                remaining -= 1

        if remaining == 0:
            break

    write = sys.stdout.write
    chunk_size = 100000
    for start in range(0, n, chunk_size):
        end = min(n, start + chunk_size)
        write('\n'.join(str(ans[values[i]]) for i in range(start, end)) + '\n')


if __name__ == "__main__":
    main()