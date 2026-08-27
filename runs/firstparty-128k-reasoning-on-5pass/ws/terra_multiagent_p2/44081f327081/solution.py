import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    k = data[1]
    values = data[2:]
    del data

    limit = max(values)

    freq = [0] * (limit + 1)
    for x in values:
        freq[x] += 1

    divisible_count = [0] * (limit + 1)

    for d in range(1, limit + 1):
        divisible_count[d] = sum(freq[d::d])

    answer_for_value = [0] * (limit + 1)

    for d in range(limit, 0, -1):
        if divisible_count[d] >= k:
            for multiple in range(d, limit + 1, d):
                if freq[multiple] and answer_for_value[multiple] == 0:
                    answer_for_value[multiple] = d

    sys.stdout.write('\n'.join(map(str, (answer_for_value[x] for x in values))))
    sys.stdout.write('\n')

if __name__ == "__main__":
    main()