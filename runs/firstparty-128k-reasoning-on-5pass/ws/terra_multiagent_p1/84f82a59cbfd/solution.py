import sys
from bisect import bisect_right

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    q = data[0]
    queries = data[1:1 + q]

    limit = 1_000_000
    distinct_count = bytearray(limit + 1)

    for p in range(2, limit + 1):
        if distinct_count[p] == 0:
            for multiple in range(p, limit + 1, p):
                distinct_count[multiple] += 1

    values = []
    for m in range(2, limit + 1):
        if distinct_count[m] == 2:
            values.append(m * m)

    output = []
    for a in queries:
        output.append(str(values[bisect_right(values, a) - 1]))

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    main()