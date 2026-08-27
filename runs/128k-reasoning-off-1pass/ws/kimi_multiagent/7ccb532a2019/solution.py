class Solution:
    def makeStringGood(self, s: str) -> int:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1

        n = len(s)
        maxc = max(cnt)
        ans = n  # delete everything (k = 0 case)

        # For target frequency k, every letter must end with count 0 or k.
        # Base cost per letter: cnt[i] (inactive) or |cnt[i]-k| (active).
        # Only adjacent transfers i -> i+1 give strict savings:
        #   transfer costs 1 (one change) vs delete + insert costing 2,
        #   so each unit transferred across edge (i, i+1) saves exactly 1.
        #   Longer moves cost (j-i) >= 2 = delete+insert, never strictly better.
        # supply_i  = cnt[i] if inactive else max(0, cnt[i]-k)
        # demand_i  = 0 if inactive else max(0, k-cnt[i])
        # savings on edge (i-1, i) = min(supply_{i-1}, demand_i), independent per edge.
        for k in range(1, maxc + 1):
            # dpA / dpI: min cost up to previous letter, with previous letter active/inactive
            dpA = abs(cnt[0] - k)
            dpI = cnt[0]
            for i in range(1, 26):
                c = cnt[i]
                p = cnt[i - 1]
                supA = p - k if p > k else 0   # previous active supply
                supI = p                        # previous inactive supply
                demA = k - c if k > c else 0    # current demand if active
                baseA = c - k if c > k else k - c
                baseI = c
                newA = baseA + min(dpA - min(supA, demA),
                                   dpI - min(supI, demA))
                newI = baseI + min(dpA, dpI)    # inactive: demand 0, no savings
                dpA, dpI = newA, newI
            cur = dpA if dpA < dpI else dpI
            if cur < ans:
                ans = cur

        return ans