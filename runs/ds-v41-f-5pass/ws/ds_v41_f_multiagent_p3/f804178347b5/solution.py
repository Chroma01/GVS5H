import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    a = b''.join(data[1:])

    # At a leaf: cost to force value 0 is 0 if bit is '0' else 1;
    # cost to force value 1 is the opposite; original value equals cost-to-0.
    dp0 = [0 if ch == 48 else 1 for ch in a]  # ch is a byte (int)
    dp1 = [1 - x for x in dp0]
    vals = dp0[:]  # original majority value of each subtree

    for _ in range(n):
        it0 = iter(dp0)
        it1 = iter(dp1)
        itv = iter(vals)
        nd0 = []
        nd1 = []
        nv = []
        ap0 = nd0.append
        ap1 = nd1.append
        apv = nv.append
        for a0, b0, c0, a1, b1, c1, u, v, w in zip(
            it0, it0, it0, it1, it1, it1, itv, itv, itv
        ):
            # Force this node to 0: at least two children must be 0.
            ap0(a0 + b0 + c0 - max(a0, b0, c0))
            # Force this node to 1: at least two children must be 1.
            ap1(a1 + b1 + c1 - max(a1, b1, c1))
            # Original value: majority of the three original child values.
            apv(1 if u + v + w >= 2 else 0)
        dp0, dp1, vals = nd0, nd1, nv

    root = vals[0]
    # Cost to force the root to the opposite of its original value.
    print(dp1[0] if root == 0 else dp0[0])


main()