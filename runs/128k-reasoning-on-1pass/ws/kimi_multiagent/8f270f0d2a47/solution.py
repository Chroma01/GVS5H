from collections import defaultdict


class Solution:
    def beautifulNumbers(self, l: int, r: int) -> int:
        return self._count_leq(r) - self._count_leq(l - 1)

    def _count_leq(self, x: int) -> int:
        """Count beautiful numbers in [1, x]."""
        if x <= 0:
            return 0
        digits = list(map(int, str(x)))

        # State: (digit_sum, digit_product, started) -> count.
        # 'tight' states still match the prefix of x; 'free' states are already smaller.
        tight = {(0, 1, False): 1}
        free = {}

        for bound in digits:
            new_tight = defaultdict(int)
            new_free = defaultdict(int)

            # Free states: next digit can be anything 0..9.
            for (s, p, started), cnt in free.items():
                if started:
                    for d in range(10):
                        new_free[(s + d, p * d, True)] += cnt
                else:
                    # Leading zero keeps the number "not started".
                    new_free[(0, 1, False)] += cnt
                    for d in range(1, 10):
                        new_free[(d, d, True)] += cnt

            # Tight states: next digit limited by `bound`.
            for (s, p, started), cnt in tight.items():
                for d in range(bound + 1):
                    if started or d != 0:
                        ns, np_, nst = s + d, p * d, True
                    else:
                        ns, np_, nst = 0, 1, False
                    if d == bound:
                        new_tight[(ns, np_, nst)] += cnt
                    else:
                        new_free[(ns, np_, nst)] += cnt

            tight = new_tight
            free = new_free

        ans = 0
        for states in (tight, free):
            for (s, p, started), cnt in states.items():
                if started and p % s == 0:
                    ans += cnt
        return ans