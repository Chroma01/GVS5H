import sys
from array import array
from bisect import bisect_right

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    q = data[0]
    queries = data[1:1 + q]

    limit = 10**6
    spf = array('I', [0]) * (limit + 1)

    for i in range(2, limit + 1):
        if spf[i] == 0:
            for j in range(i, limit + 1, i):
                if spf[j] == 0:
                    spf[j] = i

    values = []
    for x in range(2, limit + 1):
        y = x
        distinct = 0

        while y > 1:
            p = spf[y]
            distinct += 1
            if distinct > 2:
                break

            while y % p == 0:
                y //= p

        if distinct == 2:
            values.append(x * x)

    output = []
    for a in queries:
        output.append(str(values[bisect_right(values, a) - 1]))

    sys.stdout.write("\n".join(output))

if __name__ == "__main__":
    main()