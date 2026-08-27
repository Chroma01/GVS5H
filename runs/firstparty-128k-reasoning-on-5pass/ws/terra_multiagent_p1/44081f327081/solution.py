import sys
from array import array


def read_ints():
    data = sys.stdin.buffer.read()
    num = 0
    inside = False
    for b in data:
        if 48 <= b <= 57:
            num = num * 10 + (b - 48)
            inside = True
        elif inside:
            yield num
            num = 0
            inside = False
    if inside:
        yield num


it = read_ints()
n = next(it)
k = next(it)

values = array('I')
maximum = 0
for _ in range(n):
    x = next(it)
    values.append(x)
    if x > maximum:
        maximum = x

freq = [0] * (maximum + 1)
for x in values:
    freq[x] += 1

answer = array('I', [0]) * (maximum + 1)

# Process divisors from large to small. Once a value receives an answer,
# it is its largest feasible divisor and never needs to be overwritten.
for d in range(maximum, 0, -1):
    count = 0
    for multiple in range(d, maximum + 1, d):
        count += freq[multiple]
        if count >= k:
            break

    if count >= k:
        for multiple in range(d, maximum + 1, d):
            if answer[multiple] == 0:
                answer[multiple] = d

out = sys.stdout
chunk_size = 100000
for left in range(0, n, chunk_size):
    right = min(left + chunk_size, n)
    out.write('\n'.join(str(answer[values[i]]) for i in range(left, right)))
    out.write('\n')