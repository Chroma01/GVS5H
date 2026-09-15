class Solution:
    def makeStringGood(self, s: str) -> int:
        freq = [0] * 26
        for ch in s:
            freq[ord(ch) - 97] += 1

        n = len(s)
        maxf = max(freq)

        # T = 0 means deleting every character.
        ans = n

        # Final positive frequency T must be <= maxf:
        # if T > maxf, reducing T by 1 helps every kept letter.
        for T in range(1, maxf + 1):
            # dp0: best cost up to previous letter if previous final count is 0
            # dpT: best cost up to previous letter if previous final count is T
            dp0 = freq[0]
            dpT = abs(freq[0] - T)

            for i in range(1, 26):
                f = freq[i]
                fp = freq[i - 1]

                base0 = f
                baseT = abs(f - T)

                # Current letter can receive from previous letter only if it has a deficit.
                deficitT = T - f if f < T else 0

                # Previous letter can send to current only if it has a surplus.
                surplus0 = fp
                surplusT = fp - T if fp > T else 0

                # Current final count 0: no deficit, so no incoming saving.
                ndp0 = min(dp0, dpT) + base0

                # Current final count T: subtract saved delete+insert pair(s).
                ndpT = min(
                    dp0 + baseT - min(surplus0, deficitT),
                    dpT + baseT - min(surplusT, deficitT)
                )

                dp0, dpT = ndp0, ndpT

            ans = min(ans, dp0, dpT)

        return ans