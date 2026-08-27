import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = sorted(map(int, data[1:1 + n]))

    # ------------------------------------------------------------------
    # Game reduction (proved in NOTES):
    #
    # State = (multiset of unopened indices, pool P of spendable tokens).
    #   * Opening index i (value v) removes it and adds v-1 to P.
    #   * Passing requires P > 0 and decrements P.
    #   * Opening the LAST unopened index wins immediately, so opening the
    #     (N-1)-th index loses (the opponent opens the last one and wins).
    #   * Hence the decisive state is (k=2 unopened, P=0): the player to
    #     move there loses.
    #
    # Total moves to reach that state:
    #       T' = (N-2) + sum_{i in claimed} (a_i - 1)
    # which is INVARIANT under pass/open interleaving (every token ever
    # added to the pool is eventually spent; the pool ends at 0).
    # Fennec wins iff T' is odd.
    #
    # The only strategic content is WHICH N-2 indices get claimed.
    # Claiming is always safe while k >= 3, and the first move must be a
    # claim (pool = 0).  A player who claims may pick any unopened index.
    # Exchange argument: claiming a smaller available index never hurts --
    # a smaller pool addition cannot give the opponent a usable extra pass
    # before the decisive state, and it keeps large-a indices (whose
    # B = a_i - 1 values would only help the opponent dodge) unopened.
    # Under optimal play the claimed set is the N-2 smallest indices, so
    #       T' = sum_{i=1}^{N-2} a_i      (a sorted ascending)
    # and Fennec wins iff this sum is odd.
    #
    # Verified against all samples:
    #   (1,2,9)          -> sum_{i<=1} = 1  odd  -> Fennec
    #   (25,29)          -> empty sum  = 0  even -> Snuke
    #   (1,2,2,9,9,25)   -> 1+2+2+9  = 14 even -> Snuke
    # Also: N=1 -> Fennec (opens the only index); N=2 -> Snuke (T'=0).
    # ------------------------------------------------------------------

    if n == 1:
        print("Fennec")
        return
    if n == 2:
        print("Snuke")
        return

    t = sum(a[:n - 2])
    print("Fennec" if t % 2 == 1 else "Snuke")

solve()