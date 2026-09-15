class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1

        n = len(s)
        ans = n

        # Try every possible positive final frequency f.
        # f > n is never optimal: keeping only a most frequent letter
        # at its current frequency costs n - max_count, which is better.
        for f in range(1, n + 1):
            # State 0: current letter is absent in the final string.
            # State 1: current letter is present with final frequency f.
            dp_abs = cnt[0]
            dp_pres = abs(cnt[0] - f)

            for i in range(1, 26):
                c = cnt[i]
                prev_c = cnt[i - 1]

                # If current letter is absent, it has no deficit, so no
                # adjacent-change saving can end at it.
                new_abs = c + (dp_abs if dp_abs < dp_pres else dp_pres)

                # If current letter is present, its baseline cost is |c - f|.
                # Its deficit is max(f - c, 0), which can be filled by changes
                # from the previous letter.
                if c >= f:
                    base = c - f
                    deficit = 0
                else:
                    base = f - c
                    deficit = base

                # Previous letter absent: all prev_c characters are excess.
                save = prev_c if prev_c < deficit else deficit
                best = dp_abs - save

                # Previous letter present: excess is max(prev_c - f, 0).
                excess = prev_c - f
                if excess > 0:
                    save = excess if excess < deficit else deficit
                    val = dp_pres - save
                else:
                    val = dp_pres

                if val < best:
                    best = val

                new_pres = base + best
                dp_abs, dp_pres = new_abs, new_pres

            cost = dp_abs if dp_abs < dp_pres else dp_pres
            if cost < ans:
                ans = cost
                if ans == 0:
                    return 0

        return ans