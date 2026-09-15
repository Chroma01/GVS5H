class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        freq = [0] * 26
        for ch in s:
            freq[ord(ch) - 97] += 1

        maxf = max(freq)
        ans = n  # delete every character (target count k = 0)

        for k in range(maxf + 1):
            # dp0: min cost through letters 0..i if current letter's final count is 0
            # dpk: min cost through letters 0..i if current letter's final count is k
            dp0 = freq[0]
            dpk = abs(freq[0] - k)

            for i in range(1, 26):
                fi = freq[i]
                prev_f = freq[i - 1]

                # Current target is 0: no deficit, so it cannot absorb a change.
                new0 = fi + min(dp0, dpk)

                # Current target is k: deficit is how many chars we must supply.
                deficit = k - fi
                if deficit < 0:
                    deficit = 0

                # Previous target was 0: all prev_f characters are surplus.
                save0 = prev_f if prev_f < deficit else deficit

                # Previous target was k: only prev_f - k characters are surplus.
                surplus_k = prev_f - k
                if surplus_k < 0:
                    surplus_k = 0
                savek = surplus_k if surplus_k < deficit else deficit

                newk = abs(fi - k) + min(dp0 - save0, dpk - savek)

                dp0, dpk = new0, newk

            cost = dp0 if dp0 < dpk else dpk
            if cost < ans:
                ans = cost

        return ans