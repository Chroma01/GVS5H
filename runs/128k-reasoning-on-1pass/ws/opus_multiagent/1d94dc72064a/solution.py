import sys
from functools import lru_cache
import itertools, random


def solve_closed_form(n, a):
    """Closed form derived and verified:
       N=1 -> Fennec; N=2 -> Snuke; N=3 -> Fennec iff some A_i odd;
       N>=4 -> Fennec iff #odd A_i is odd."""
    odd = sum(1 for x in a if x & 1)
    if n == 1:
        return "Fennec"
    if n == 2:
        return "Snuke"
    if n == 3:
        return "Fennec" if odd >= 1 else "Snuke"
    return "Fennec" if odd % 2 == 1 else "Snuke"


# ---------------------------------------------------------------------------
# Brute force verifier (only executed with "--test"; never during judging)
# ---------------------------------------------------------------------------
def brute(n, a):
    @lru_cache(maxsize=None)
    def win(V, p):
        # V: sorted tuple of untouched values, p: stall pool.
        # Returns True if the player to move wins.
        if len(V) == 1:
            return True  # advance the last index and win immediately
        for i in range(len(V)):
            if i > 0 and V[i] == V[i - 1]:
                continue
            nv = V[:i] + V[i + 1:]
            if not win(nv, p + V[i] - 1):
                return True
        if p > 0 and not win(V, p - 1):
            return True
        return False

    return "Fennec" if win(tuple(sorted(a)), 0) else "Snuke"


def run_tests():
    bad = 0
    for n in range(1, 6):
        for a in itertools.product(range(1, 6), repeat=n):
            b = brute(n, list(a))
            c = solve_closed_form(n, list(a))
            if b != c:
                bad += 1
                print("MISMATCH", n, a, "brute:", b, "formula:", c)
                if bad > 20:
                    return
    random.seed(12345)
    for _ in range(300):
        n = 6
        a = [random.randint(1, 4) for _ in range(n)]
        b = brute(n, a)
        c = solve_closed_form(n, a)
        if b != c:
            bad += 1
            print("MISMATCH", n, a, "brute:", b, "formula:", c)
    if bad == 0:
        print("all tests passed")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
        return
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    odd = 0
    for j in range(1, n + 1):
        if int(data[j]) & 1:
            odd += 1
    if n == 1:
        ans = "Fennec"
    elif n == 2:
        ans = "Snuke"
    elif n == 3:
        ans = "Fennec" if odd >= 1 else "Snuke"
    else:
        ans = "Fennec" if odd % 2 == 1 else "Snuke"
    sys.stdout.write(ans + "\n")


main()