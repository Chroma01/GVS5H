from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        CAP = 10**18  # anything >= k (k <= 1e15) is "big enough"

        # Capped factorial table: fact[i] = min(i!, CAP)
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i
            if fact[i] > CAP:
                fact[i] = CAP

        def capped_mul(a: int, b: int) -> int:
            if a >= CAP or b >= CAP:
                return CAP
            m = a * b
            return m if m < CAP else CAP

        odds = [x for x in range(1, n + 1) if x % 2 == 1]
        evens = [x for x in range(1, n + 1) if x % 2 == 0]
        o, e = len(odds), len(evens)

        # Total number of alternating permutations.
        # Parity pattern is forced by the first element's parity.
        # If n is odd (o == e + 1), must start with odd.
        # If n is even (o == e), can start with either parity.
        if o == e:
            total = capped_mul(2, capped_mul(fact[o], fact[e]))
        else:
            total = capped_mul(fact[o], fact[e])

        if k > total:
            return []

        result = []
        ro, re = o, e  # remaining odds / evens
        # required parity for next position: None means free (only at position 0 when n even)
        need = None  # 1 = odd, 0 = even
        if o != e:
            need = 1  # n odd -> must start with odd

        for pos in range(n):
            if need is None:
                candidates = sorted(odds + evens)  # free first choice (n even)
            elif need == 1:
                candidates = odds
            else:
                candidates = evens

            chosen = None
            for c in list(candidates):
                p = c & 1
                # tentatively place c
                if p == 1:
                    ro -= 1
                else:
                    re -= 1
                block = capped_mul(fact[ro], fact[re])
                if k > block:
                    k -= block
                    # undo
                    if p == 1:
                        ro += 1
                    else:
                        re += 1
                else:
                    chosen = c
                    break

            # chosen must exist because k <= total and blocks partition the rest
            result.append(chosen)
            if chosen & 1:
                odds.remove(chosen)
                need = 0
            else:
                evens.remove(chosen)
                need = 1

        return result