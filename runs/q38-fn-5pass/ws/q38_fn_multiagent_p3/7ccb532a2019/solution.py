class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1

        n = len(s)

        # Already good: every present character has the same frequency.
        present = [c for c in cnt if c]
        if len(set(present)) <= 1:
            return 0

        # Frequencies larger than max(cnt) are never strictly better.
        max_f = max(cnt)
        ans = n  # delete everything (also a safe upper bound)

        for f in range(1, max_f + 1):
            # State for letter 0:
            # drop = minimum cost up to this letter if this letter is removed
            # keep = minimum cost up to this letter if this letter is kept with frequency f
            c = cnt[0]
            drop = c
            diff = c - f
            keep = diff if diff >= 0 else -diff
            prev_c = c

            for i in range(1, 26):
                c = cnt[i]

                # If current letter is removed, it has no deficit, so no incoming saving.
                best_prev = drop if drop < keep else keep
                new_drop = best_prev + c

                diff = c - f
                if diff >= 0:
                    # Current letter has no deficit; incoming changes cannot save.
                    new_keep = best_prev + diff
                else:
                    deficit = -diff

                    # Saving if previous letter was removed:
                    # all previous occurrences are surplus.
                    save_drop = prev_c if prev_c < deficit else deficit

                    # Saving if previous letter was kept:
                    # only occurrences above f are surplus.
                    surplus = prev_c - f
                    if surplus <= 0:
                        save_keep = 0
                    else:
                        save_keep = surplus if surplus < deficit else deficit

                    best_keep = drop - save_drop
                    alt_keep = keep - save_keep
                    if alt_keep < best_keep:
                        best_keep = alt_keep

                    new_keep = best_keep + deficit

                drop, keep = new_drop, new_keep
                prev_c = c

            cost = drop if drop < keep else keep
            if cost < ans:
                ans = cost
                if ans == 0:
                    return 0

        return ans