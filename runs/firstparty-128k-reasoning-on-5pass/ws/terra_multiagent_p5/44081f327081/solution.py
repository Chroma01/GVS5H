import sys
from array import array


def int_stream(data):
    value = 0
    in_number = False
    for c in data:
        if 48 <= c <= 57:
            value = value * 10 + c - 48
            in_number = True
        elif in_number:
            yield value
            value = 0
            in_number = False
    if in_number:
        yield value


def main():
    data = sys.stdin.buffer.read()
    it = int_stream(data)

    n = next(it)
    k = next(it)
    a = array('I', it)

    del data
    del it

    if k == 1:
        sys.stdout.write('\n'.join(map(str, a)))
        sys.stdout.write('\n')
        return

    maximum = max(a)
    freq = [0] * (maximum + 1)

    for x in a:
        freq[x] += 1

    valid = bytearray(maximum + 1)
    limit = maximum + 1

    for d in range(1, limit):
        count = 0
        for multiple in range(d, limit, d):
            count += freq[multiple]
            if count >= k:
                valid[d] = 1
                break

    answer = array('I', [0]) * limit

    for d in range(maximum, 0, -1):
        if valid[d]:
            for multiple in range(d, limit, d):
                if freq[multiple] and answer[multiple] == 0:
                    answer[multiple] = d

    sys.stdout.write('\n'.join(str(answer[x]) for x in a))
    sys.stdout.write('\n')


if __name__ == "__main__":
    main()