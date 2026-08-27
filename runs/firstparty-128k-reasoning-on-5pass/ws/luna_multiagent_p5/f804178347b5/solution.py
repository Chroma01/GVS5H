import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    s = b"".join(data[1:])

    # For each current subtree, c0/c1 are the minimum changes
    # needed to make its result 0/1 respectively.
    c0 = [0 if ch == 48 else 1 for ch in s]
    c1 = [1 - x for x in c0]

    while len(c0) > 1:
        m = len(c0)
        next0 = []
        next1 = []

        for i in range(0, m, 3):
            a0, b0, d0 = c0[i], c0[i + 1], c0[i + 2]
            a1, b1, d1 = c1[i], c1[i + 1], c1[i + 2]

            # At least two children must be 0.
            next0.append(min(
                a0 + b0 + d0,
                a0 + b0 + d1,
                a0 + b1 + d0,
                a1 + b0 + d0,
            ))

            # At least two children must be 1.
            next1.append(min(
                a1 + b1 + d1,
                a1 + b1 + d0,
                a1 + b0 + d1,
                a0 + b1 + d1,
            ))

        c0, c1 = next0, next1

    # Exactly one root state has cost zero without modifications.
    original = 0 if c0[0] == 0 else 1
    print(c1[0] if original == 0 else c0[0])

if __name__ == "__main__":
    solve()