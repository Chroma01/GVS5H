import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    values = data[1:]

    if n < 3:
        print(0)
        return

    maximum = max(values)

    # Store f[x] at bit position 20*x.  Since every convolution
    # coefficient is at most N <= 10^6 < 2^20, no carries cross fields.
    packed = bytearray((5 * maximum) // 2 + 1)
    for x in values:
        pos = 2 * x + (x >> 1)  # floor(20*x / 8)
        packed[pos] = 1 << (4 if x & 1 else 0)

    encoded = int.from_bytes(packed, "little")
    del packed

    squared = encoded * encoded
    del encoded

    # Coefficient of degree 2*b starts at bit 40*b, i.e. byte 5*b.
    # Extra bytes make accesses near the final coefficient safe.
    result_bytes = squared.to_bytes(5 * maximum + 3, "little")

    total = 0
    for b in values:
        pos = 5 * b
        coefficient = (
            result_bytes[pos]
            | (result_bytes[pos + 1] << 8)
            | ((result_bytes[pos + 2] & 15) << 16)
        )
        total += coefficient - 1

    print(total // 2)


if __name__ == "__main__":
    main()