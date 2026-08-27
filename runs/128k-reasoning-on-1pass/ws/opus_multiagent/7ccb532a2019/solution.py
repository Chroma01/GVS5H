class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - 97] += 1

        mx = max(cnt)
        best = n  # delete everything (empty string is vacuously good)

        for t in range(1, mx + 1):
            # state after processing letter 0 ('a'); surplus charged on transition
            c0 = cnt[0]
            dp_keep = t - c0 if t > c0 else 0   # deficit of 'a' must be pure inserts
            dp_drop = 0
            sk = c0 - t if c0 > t else 0        # surplus if 'a' kept
            sd = c0                             # surplus if 'a' dropped

            for i in range(1, 26):
                ci = cnt[i]
                dk = t - ci if t > ci else 0    # deficit if kept
                # cost to reach keep-state at i
                a = dp_keep + (sk if sk > dk else dk)
                b = dp_drop + (sd if sd > dk else dk)
                nk = a if a < b else b
                # cost to reach drop-state at i (deficit 0)
                a2 = dp_keep + sk
                b2 = dp_drop + sd
                nd = a2 if a2 < b2 else b2

                dp_keep = nk
                dp_drop = nd
                sk = ci - t if ci > t else 0
                sd = ci

            # 'z' surplus can only be deleted
            r1 = dp_keep + sk
            r2 = dp_drop + sd
            r = r1 if r1 < r2 else r2
            if r < best:
                best = r

        return best