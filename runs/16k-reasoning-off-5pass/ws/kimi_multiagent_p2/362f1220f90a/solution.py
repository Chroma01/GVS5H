class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1

        # forced[p] = character forced at position p by some 'T' window, or None
        forced = [None] * L

        # 1) Apply all 'T' constraints, detecting conflicts
        for i in range(n):
            if str1[i] == 'T':
                for j in range(m):
                    p = i + j
                    c = str2[j]
                    if forced[p] is not None and forced[p] != c:
                        return ""
                    forced[p] = c

        # 2) For each 'F' window, find its last free position (or validate if fully forced)
        #    Group window start indices by their last free position.
        last_free_groups = [[] for _ in range(L)]
        for i in range(n):
            if str1[i] == 'F':
                last_free = -1
                end = i + m - 1
                for p in range(end, i - 1, -1):
                    if forced[p] is None:
                        last_free = p
                        break
                if last_free == -1:
                    # Window fully forced: it must differ from str2
                    same = True
                    for j in range(m):
                        if forced[i + j] != str2[j]:
                            same = False
                            break
                    if same:
                        return ""
                else:
                    last_free_groups[last_free].append(i)

        # 3) Greedy left-to-right fill
        word = [None] * L
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        for p in range(L):
            if forced[p] is not None:
                word[p] = forced[p]
                continue

            forbidden = set()
            for i in last_free_groups[p]:
                # Window [i, i+m-1], p is its last free position.
                # All other positions are determined (earlier free ones set, later ones forced).
                # Check whether everything except position p matches str2.
                off = p - i
                rest_match = True
                # Check prefix part word[i..p-1] vs str2[0..off-1]
                for j in range(off):
                    if word[i + j] != str2[j]:
                        rest_match = False
                        break
                # Check suffix part word[p+1..i+m-1] vs str2[off+1..m-1] (all forced)
                if rest_match:
                    for j in range(off + 1, m):
                        if forced[i + j] != str2[j]:
                            rest_match = False
                            break
                if rest_match:
                    forbidden.add(str2[off])

            chosen = None
            for c in alphabet:
                if c not in forbidden:
                    chosen = c
                    break
            if chosen is None:
                return ""
            word[p] = chosen

        return "".join(word)