class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1

        word = [None] * L
        forced = [False] * L

        # Step 1: apply all 'T' constraints, detect conflicts
        for i, c in enumerate(str1):
            if c == 'T':
                for k in range(m):
                    pos = i + k
                    ch = str2[k]
                    if word[pos] is not None and word[pos] != ch:
                        return ""
                    word[pos] = ch
                    forced[pos] = True

        # Step 2: fill free positions with 'a'
        for i in range(L):
            if word[i] is None:
                word[i] = 'a'

        # Step 3: for each F-window, count positions that currently break it
        f_indices = [i for i, c in enumerate(str1) if c == 'F']
        breaker_cnt = {}
        for i in f_indices:
            cnt = 0
            for k in range(m):
                if word[i + k] != str2[k]:
                    cnt += 1
            breaker_cnt[i] = cnt

        # Step 4: repair F-windows left to right
        for i in f_indices:
            if breaker_cnt[i] > 0:
                continue
            # Window i currently matches str2 exactly; bump its latest free
            # position p (latest to preserve lexicographic minimality).
            p = -1
            for pos in range(i + m - 1, i - 1, -1):
                if not forced[pos]:
                    p = pos
                    break
            if p == -1:
                return ""

            # Forbidden chars at p: str2[p-i] (must break window i), plus
            # str2[p-j] for any earlier F-window j whose ONLY breaker is p
            # (changing p to str2[p-j] would re-break window j).
            forbidden = {str2[p - i]}
            lo = max(0, p - m + 1)
            for j in range(lo, i):
                if str1[j] == 'F' and breaker_cnt.get(j, 0) == 1:
                    if word[p] != str2[p - j]:
                        forbidden.add(str2[p - j])

            chosen = None
            for ci in range(26):
                c = chr(ord('a') + ci)
                if c not in forbidden:
                    chosen = c
                    break
            if chosen is None:
                return ""

            old = word[p]
            if chosen == old:
                continue  # cannot happen (old == str2[p-i] is forbidden)

            word[p] = chosen

            # Update breaker counts for all F-windows containing p
            for j in range(lo, min(n - 1, p) + 1):
                if str1[j] != 'F':
                    continue
                off = p - j
                was = (old != str2[off])
                now = (chosen != str2[off])
                if was and not now:
                    breaker_cnt[j] -= 1
                elif now and not was:
                    breaker_cnt[j] += 1

        # Step 5: final verification
        for i, c in enumerate(str1):
            if c == 'T':
                for k in range(m):
                    if word[i + k] != str2[k]:
                        return ""
            else:
                match = True
                for k in range(m):
                    if word[i + k] != str2[k]:
                        match = False
                        break
                if match:
                    return ""

        return "".join(word)