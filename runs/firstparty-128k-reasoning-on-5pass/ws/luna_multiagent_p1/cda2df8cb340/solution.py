import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = data[1:1 + n]

    total_sum = sum(a)
    max_sum = 2 * max(a)

    # P_0: sum of A_i + A_j over all pairs i <= j.
    p_values = [(n + 1) * total_sum]

    def divisible_sum(modulus):
        mask = modulus - 1
        groups = {}

        for x in a:
            residue = x & mask
            group = groups.get(residue)
            if group is None:
                groups[residue] = [1, x]
            else:
                group[0] += 1
                group[1] += x

        result = 0

        for residue, (count, value_sum) in groups.items():
            opposite = (-residue) & mask

            if residue < opposite:
                other = groups.get(opposite)
                if other is not None:
                    other_count, other_sum = other
                    result += value_sum * other_count
                    result += other_sum * count
            elif residue == opposite:
                # Distinct pairs contribute once per element, while each
                # diagonal contributes twice its element value.
                result += (count + 1) * value_sum

        return result

    modulus = 2
    while modulus <= max_sum:
        p_values.append(divisible_sum(modulus))
        modulus <<= 1

    # No positive pair sum is divisible by a larger power of two.
    p_values.append(0)

    answer = 0
    for k in range(len(p_values) - 1):
        answer += (p_values[k] - p_values[k + 1]) // (1 << k)

    print(answer)


if __name__ == "__main__":
    main()