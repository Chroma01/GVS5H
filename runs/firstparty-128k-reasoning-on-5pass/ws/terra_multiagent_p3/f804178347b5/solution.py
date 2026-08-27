import sys
from array import array


def main():
    tokens = sys.stdin.buffer.read().split()
    if not tokens:
        return

    n = int(tokens[0])
    s = b"".join(tokens[1:])

    # c0[i], c1[i]: minimum flips needed to make subtree i evaluate to 0 or 1.
    c0 = array('I', (ch == ord('1') for ch in s))
    c1 = array('I', (ch == ord('0') for ch in s))

    for _ in range(n):
        size = len(c0) // 3
        next0 = array('I', [0]) * size
        next1 = array('I', [0]) * size

        for i in range(size):
            j = 3 * i

            a, b, c = c0[j], c0[j + 1], c0[j + 2]
            next0[i] = a + b + c - max(a, b, c)

            a, b, c = c1[j], c1[j + 1], c1[j + 2]
            next1[i] = a + b + c - max(a, b, c)

        c0, c1 = next0, next1

    if c0[0] == 0:
        print(c1[0])
    else:
        print(c0[0])


if __name__ == "__main__":
    main()