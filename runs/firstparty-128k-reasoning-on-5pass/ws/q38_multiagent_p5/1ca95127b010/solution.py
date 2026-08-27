import sys
from collections import deque


def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    X = int(data[1])
    Y = int(data[2])
    S = data[3]
    T = data[4]

    # If no operation can be applied, the strings must already be equal.
    if X + Y > N:
        print("Yes" if S == T else "No")
        return

    # Invariant 1: ordered positions of '1' modulo X.
    if X == 1:
        if S.count(b"1") != T.count(b"1"):
            print("No")
            return
    else:
        a = [i % X for i, ch in enumerate(S, 1) if ch == 49]  # ord('1')
        b = [i % X for i, ch in enumerate(T, 1) if ch == 49]
        if a != b:
            print("No")
            return
        del a, b

    # Invariant 2: ordered positions of '0' modulo Y.
    if Y == 1:
        if S.count(b"0") != T.count(b"0"):
            print("No")
            return
    else:
        a = [i % Y for i, ch in enumerate(S, 1) if ch == 48]  # ord('0')
        b = [i % Y for i, ch in enumerate(T, 1) if ch == 48]
        if a != b:
            print("No")
            return

    print("Yes")


def stress_test(max_n: int = 10) -> bool:
    """
    Optional local stress test.

    Run with:
        python program.py stress

    It exhaustively BFSes all 2^N strings for N <= max_n and all X, Y,
    then checks that:
      - every connected component has a single invariant, and
      - every invariant belongs to a single connected component.
    """
    for N in range(1, max_n + 1):
        total = 1 << N
        for X in range(1, N + 1):
            for Y in range(1, N + 1):
                masks = []
                limit = N - X - Y + 1
                for i in range(limit):
                    m0X = ((1 << X) - 1) << i
                    m1Y = ((1 << Y) - 1) << (i + X)
                    m1Y_first = ((1 << Y) - 1) << i
                    m0X_next = ((1 << X) - 1) << (i + Y)
                    masks.append((m0X, m1Y, m1Y_first, m0X_next))

                comp = [-1] * total
                comp_inv = {}
                inv_comp = {}

                for start in range(total):
                    if comp[start] != -1:
                        continue

                    cid = len(comp_inv)
                    q = deque([start])
                    comp[start] = cid

                    while q:
                        st = q.popleft()

                        ones = []
                        zeros = []
                        for pos in range(1, N + 1):
                            if (st >> (pos - 1)) & 1:
                                ones.append(pos % X)
                            else:
                                zeros.append(pos % Y)
                        inv = (tuple(ones), tuple(zeros))

                        prev_inv = comp_inv.get(cid)
                        if prev_inv is None:
                            comp_inv[cid] = inv
                        elif prev_inv != inv:
                            print(f"counterexample N={N} X={X} Y={Y} state={st:0{N}b}")
                            return False

                        prev_comp = inv_comp.get(inv)
                        if prev_comp is None:
                            inv_comp[inv] = cid
                        elif prev_comp != cid:
                            print(f"counterexample N={N} X={X} Y={Y} state={st:0{N}b}")
                            return False

                        for m0X, m1Y, m1Y_first, m0X_next in masks:
                            # Operation A: 0^X 1^Y -> 1^Y 0^X
                            if (st & m0X) == 0 and (st & m1Y) == m1Y:
                                ns = st | m1Y_first
                                ns &= ~m0X_next
                                if comp[ns] == -1:
                                    comp[ns] = cid
                                    q.append(ns)

                            # Operation B: 1^Y 0^X -> 0^X 1^Y
                            if (st & m1Y_first) == m1Y_first and (st & m0X_next) == 0:
                                ns = st & ~m0X
                                ns |= m1Y
                                if comp[ns] == -1:
                                    comp[ns] = cid
                                    q.append(ns)

    print("stress test passed")
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stress":
        stress_test()
    else:
        solve()