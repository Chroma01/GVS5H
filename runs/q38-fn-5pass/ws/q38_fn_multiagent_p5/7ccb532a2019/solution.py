class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1

        n = len(s)
        if n == 0:
            return 0

        # Frequencies above max(cnt) are never strictly better:
        # all present letters would be in deficit, and increasing f by 1
        # adds one insert per present letter while creating at most one
        # additional adjacent saving per present letter.
        upper = max(cnt)
        ans = n

        for f in range(1, upper + 1):
            # dp0: previous letter is absent in the final string
            # dp1: previous letter is present with frequency f
            dp0 = cnt[0]
            dp1 = abs(cnt[0] - f)

            for i in range(1, 26):
                c = cnt[i]
                pc = cnt[i - 1]

                best_prev = dp0 if dp0 < dp1 else dp1

                # Current letter absent: delete all original occurrences.
                # Its surplus can still be used by the next letter, which
                # will be accounted for in the next transition.
                ndp0 = best_prev + c

                if c < f:
                    # Current letter present and has a deficit.
                    deficit = f - c

                    # If previous letter is absent, all pc occurrences are surplus.
                    save_absent = pc if pc < deficit else deficit
                    val_absent = dp0 - save_absent

                    # If previous letter is present, only max(pc - f, 0) is surplus.
                    surplus_present = pc - f
                    if surplus_present > 0:
                        save_present = surplus_present if surplus_present < deficit else deficit
                    else:
                        save_present = 0
                    val_present = dp1 - save_present

                    ndp1 = (val_absent if val_absent < val_present else val_present) + deficit
                else:
                    # Current letter present with no deficit: no incoming change saves cost.
                    ndp1 = best_prev + (c - f)

                dp0, dp1 = ndp0, ndp1

            if dp0 < ans:
                ans = dp0
            if dp1 < ans:
                ans = dp1

            if ans == 0:
                return 0

        return ans