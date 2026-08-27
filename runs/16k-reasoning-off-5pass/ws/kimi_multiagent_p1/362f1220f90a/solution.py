class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1

        # forced[j] = character forced at position j by some T-window, or None
        forced = [None] * L

        # Propagate T constraints
        for i, ch in enumerate(str1):
            if ch == 'T':
                for k in range(m):
                    j = i + k
                    c = str2[k]
                    if forced[j] is None:
                        forced[j] = c
                    elif forced[j] != c:
                        return ""

        # For each F-window starting at i, compute lastBreak[i]:
        # the last position p in [i, i+m-1] such that the window can be broken at p,
        # i.e. forced[p] is None or forced[p] != str2[p-i].
        # If no such position exists -> infeasible.
        lastBreak = [-1] * n  # only meaningful for F indices
        # bucket[j] = list of F-window start indices whose lastBreak == j
        bucket = [[] for _ in range(L)]

        for i, ch in enumerate(str1):
            if ch == 'F':
                lb = -1
                # scan window from right to left to find last breakable position
                for p in range(i + m - 1, i - 1, -1):
                    k = p - i
                    fp = forced[p]
                    if fp is None or fp != str2[k]:
                        lb = p
                        break
                if lb == -1:
                    return ""
                lastBreak[i] = lb
                bucket[lb].append(i)

        word = [None] * L

        # Active F-windows state:
        # A window i is "matching" while word[i..j] == str2[0..j-i] so far and not broken.
        # We maintain a deque of active matching windows covering the current position.
        # When we place c at j, windows with str2[j-i] != c become broken.
        from collections import deque

        active = deque()  # window starts i (F) that are unbroken and i <= j
        broken = [False] * n  # broken status per F window

        for j in range(L):
            # add newly starting F windows
            if j < n and str1[j] == 'F':
                active.append(j)
            # remove windows that ended before j
            while active and active[0] + m - 1 < j:
                active.popleft()

            if forced[j] is not None:
                c = forced[j]
                word[j] = c
                # update active windows
                new_active = deque()
                for i in active:
                    k = j - i
                    if str2[k] != c:
                        broken[i] = True
                    else:
                        # still matching; if window ends here -> infeasible
                        if i + m - 1 == j:
                            return ""
                        new_active.append(i)
                active = new_active
            else:
                # free position: determine forbidden chars from windows whose
                # lastBreak == j (must break now) and that are still unbroken/matching
                forbidden = set()
                if bucket[j]:
                    for i in bucket[j]:
                        if not broken[i]:
                            # window i must be broken at j: c != str2[j-i]
                            forbidden.add(str2[j - i])
                # choose smallest c not forbidden
                c = None
                for cand in range(26):
                    cc = chr(ord('a') + cand)
                    if cc not in forbidden:
                        c = cc
                        break
                if c is None:
                    return ""
                word[j] = c
                # update active windows
                new_active = deque()
                for i in active:
                    k = j - i
                    if str2[k] != c:
                        broken[i] = True
                    else:
                        if i + m - 1 == j:
                            # window completed as exact match -> this c invalid
                            # This can only happen if c was forced to match, but c is
                            # free here; however forbidden logic should have prevented
                            # it when lastBreak == j. If lastBreak > j it can't be that
                            # window ends at j (j is last position => lastBreak <= j).
                            # So this indicates infeasibility.
                            return ""
                        new_active.append(i)
                active = new_active

        # Final verification pass
        s = ''.join(word)
        for i, ch in enumerate(str1):
            sub = s[i:i + m]
            if ch == 'T':
                if sub != str2:
                    return ""
            else:
                if sub == str2:
                    return ""
        return s