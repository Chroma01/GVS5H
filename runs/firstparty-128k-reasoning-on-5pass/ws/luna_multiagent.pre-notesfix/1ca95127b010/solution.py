import sys


def canonical_form(s: bytes, x: int, y: int):
    """
    Normalize using the oriented rewrite rule

        1^y 0^x -> 0^x 1^y.

    The rule strictly decreases the binary string lexicographically.
    Since its pattern has no nontrivial self-overlap, the rewrite system
    is confluent, so equal normal forms are equivalent to mutual
    reachability.

    A pair of runs 1^a 0^b can be reduced in bulk. If

        a = q*y + r
        b = p*x + s,

    then all possible exchanges between these two runs produce

        1^r 0^(p*x) 1^(q*y) 0^s.

    Only the boundary immediately to the left can become reducible.
    """

    stack = []

    def append_run(bit, length):
        if length <= 0:
            return
        if stack and stack[-1][0] == bit:
            stack[-1][1] += length
        else:
            stack.append([bit, length])

    def normalize_suffix():
        while len(stack) >= 2:
            bit1, cnt1 = stack[-2]
            bit2, cnt2 = stack[-1]

            if bit1 != 1 or bit2 != 0 or cnt1 < y or cnt2 < x:
                break

            rem1 = cnt1 % y
            moved1 = cnt1 - rem1
            moved0 = cnt2 - (cnt2 % x)
            rem0 = cnt2 % x

            stack.pop()
            stack.pop()

            append_run(1, rem1)
            append_run(0, moved0)
            append_run(1, moved1)
            append_run(0, rem0)

    previous = -1
    count = 0

    for c in s:
        bit = c - 48
        if bit == previous:
            count += 1
        else:
            if previous != -1:
                append_run(previous, count)
                normalize_suffix()
            previous = bit
            count = 1

    if previous != -1:
        append_run(previous, count)
        normalize_suffix()

    return tuple((bit, length) for bit, length in stack)


def solve():
    input = sys.stdin.buffer.readline

    n, x, y = map(int, input().split())
    s = input().strip()
    t = input().strip()

    if s == t:
        print("Yes")
        return

    if x + y > n:
        print("No")
        return

    # For x = y = 1, the operation swaps adjacent unequal bits.
    # Therefore every arrangement with the same number of ones is reachable.
    if x == 1 and y == 1:
        print("Yes" if s.count(b"1") == t.count(b"1") else "No")
        return

    print("Yes" if canonical_form(s, x, y) == canonical_form(t, x, y) else "No")


if __name__ == "__main__":
    solve()