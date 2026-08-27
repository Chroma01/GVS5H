import sys
from array import array
from math import gcd

def main():
    raw = sys.stdin.buffer.read().split()
    if not raw:
        return

    n = int(raw[0])
    k = int(raw[1])

    values = array('I')
    max_value = 0
    for i in range(2, len(raw)):
        x = int(raw[i])
        values.append(x)
        if x > max_value:
            max_value = x
    del raw

    if k == 1:
        sys.stdout.write('\n'.join(map(str, values)))
        return

    if k == n:
        g = 0
        for x in values:
            g = gcd(g, x)
        sys.stdout.write((str(g) + '\n') * n)
        return

    freq = array('I', [0]) * (max_value + 1)
    present = bytearray(max_value + 1)

    for x in values:
        freq[x] += 1
        present[x] = 1

    limit = max_value + 1

    # Replace frequencies by the number of input elements divisible by d.
    for d in range(1, limit):
        total = 0
        for multiple in range(d, limit, d):
            total += freq[multiple]
        freq[d] = total

    answer = array('I', [0]) * (max_value + 1)

    # Descending order ensures the first assigned divisor is maximal.
    for d in range(max_value, 0, -1):
        if freq[d] < k:
            continue
        for multiple in range(d, limit, d):
            if present[multiple] and answer[multiple] == 0:
                answer[multiple] = d

    sys.stdout.write('\n'.join(str(answer[x]) for x in values))

if __name__ == "__main__":
    main()