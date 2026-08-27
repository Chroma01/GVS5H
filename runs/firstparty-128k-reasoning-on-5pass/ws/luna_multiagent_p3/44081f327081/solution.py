import sys
import math
from array import array


def write_direct(values):
    out = sys.stdout
    chunk = 100000
    for start in range(0, len(values), chunk):
        end = min(start + chunk, len(values))
        out.write("\n".join(str(values[i]) for i in range(start, end)))
        out.write("\n")


def write_constant(value, n):
    sys.stdout.write((str(value) + "\n") * n)


def write_answers(values, answer):
    out = sys.stdout
    chunk = 100000
    for start in range(0, len(values), chunk):
        end = min(start + chunk, len(values))
        out.write("\n".join(str(answer[values[i]]) for i in range(start, end)))
        out.write("\n")


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n, k = data[0], data[1]
    input_values = data[2:]

    values = array("I")
    maximum = 0
    overall_gcd = 0

    for x in input_values:
        values.append(x)
        if x > maximum:
            maximum = x
        overall_gcd = math.gcd(overall_gcd, x)

    if k == 1:
        write_direct(values)
        return

    if k == n:
        write_constant(overall_gcd, n)
        return

    freq = array("I", [0]) * (maximum + 1)
    for x in values:
        freq[x] += 1

    count = array("I", [0]) * (maximum + 1)
    limit = maximum + 1

    for d in range(1, limit):
        total = 0
        for multiple in range(d, limit, d):
            total += freq[multiple]
        count[d] = total

    answer = array("I", [0]) * limit

    for d in range(maximum, 0, -1):
        if count[d] < k:
            continue
        for multiple in range(d, limit, d):
            if freq[multiple] and answer[multiple] == 0:
                answer[multiple] = d

    write_answers(values, answer)


if __name__ == "__main__":
    solve()