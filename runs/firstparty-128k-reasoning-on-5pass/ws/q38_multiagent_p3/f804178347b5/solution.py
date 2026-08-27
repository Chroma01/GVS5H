import sys
from array import array


def main():
    data = sys.stdin.buffer.read()
    if not data:
        return

    # Parse N.
    i = 0
    L = len(data)
    while i < L and data[i] <= 32:
        i += 1
    N = 0
    while i < L and 48 <= data[i] <= 57:
        N = N * 10 + (data[i] - 48)
        i += 1

    m = 3 ** N

    # Robustly read exactly m bits, whether they are contiguous or space-separated.
    bits = bytearray(m)
    cnt = 0
    for b in data[i:]:
        if b == 48 or b == 49:  # '0' or '1'
            bits[cnt] = b - 48
            cnt += 1
            if cnt == m:
                break
    del data

    # costs[v] = minimum leaf flips needed to toggle node v from its original value.
    # For leaves, this is always 1.
    costs = array('H', [1]) * m
    length = m

    # Bottom-up reduction of the ternary tree.
    while length > 1:
        new_len = length // 3
        new_bits = bytearray(new_len)
        new_costs = array('H', [0]) * new_len

        old_bits = bits
        old_costs = costs
        base = 0

        for j in range(new_len):
            b0 = old_bits[base]
            b1 = old_bits[base + 1]
            b2 = old_bits[base + 2]

            c0 = old_costs[base]
            c1 = old_costs[base + 1]
            c2 = old_costs[base + 2]

            s = b0 + b1 + b2

            # Parent bit is the majority of the three child bits.
            if s >= 2:
                new_bits[j] = 1
                # To toggle parent (1 -> 0), children already 0 are free;
                # children equal to 1 need their own toggle cost.
                x0 = c0 if b0 else 0
                x1 = c1 if b1 else 0
                x2 = c2 if b2 else 0
            else:
                # To toggle parent (0 -> 1), children already 1 are free;
                # children equal to 0 need their own toggle cost.
                x0 = c0 if not b0 else 0
                x1 = c1 if not b1 else 0
                x2 = c2 if not b2 else 0

            # Sum of the two smallest costs.
            if x0 <= x1:
                m1 = x0
                m2 = x1
            else:
                m1 = x1
                m2 = x0

            if x2 < m2:
                if x2 < m1:
                    m2 = m1
                    m1 = x2
                else:
                    m2 = x2

            new_costs[j] = m1 + m2
            base += 3

        bits = new_bits
        costs = new_costs
        length = new_len

    sys.stdout.write(str(costs[0]) + "\n")


if __name__ == "__main__":
    main()