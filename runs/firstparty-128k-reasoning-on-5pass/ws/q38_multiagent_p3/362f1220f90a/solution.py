class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1

        # Prefix function for str2.
        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j > 0 and str2[i] != str2[j]:
                j = pi[j - 1]
            if str2[i] == str2[j]:
                j += 1
            pi[i] = j

        pat = [ord(ch) - 97 for ch in str2]
        bits = [1 << q for q in range(m + 1)]

        # KMP automaton. State m means the last m characters equal str2.
        trans = [[0] * 26 for _ in range(m + 1)]
        trans[0][pat[0]] = 1
        for q in range(1, m + 1):
            trans[q] = trans[pi[q - 1]].copy()
            if q < m:
                trans[q][pat[q]] = q + 1

        # next_mask[q]: states reachable from q by one lowercase character.
        next_mask = [0] * (m + 1)
        for q in range(m + 1):
            mask = 0
            for nq in trans[q]:
                mask |= bits[nq]
            next_mask[q] = mask

        all_mask = (1 << (m + 1)) - 1
        full_mask = bits[m]
        nonfull_mask = all_mask ^ full_mask

        # States that can move to the full-match state in one character.
        can_full = 0
        for q in range(m + 1):
            if next_mask[q] & full_mask:
                can_full |= bits[q]

        # filter[pos] is the mask of allowed states after writing word[pos].
        filters = [all_mask] * L
        for i, ch in enumerate(str1):
            filters[i + m - 1] = full_mask if ch == 'T' else nonfull_mask

        # dp[pos]: bitmask of KMP states before word[pos] that can be completed.
        dp = [0] * (L + 1)
        dp[L] = all_mask
        range_states = range(m + 1)
        nm = next_mask

        for pos in range(L - 1, -1, -1):
            allowed = dp[pos + 1] & filters[pos]
            if allowed == 0:
                return ""

            # If every non-full state is allowed, every current state can move
            # to some non-full state because the alphabet has 26 letters.
            if allowed == all_mask or allowed == nonfull_mask:
                dp[pos] = all_mask
                continue

            # If only the full state is allowed, use the precomputed preimage.
            if allowed == full_mask:
                if can_full == 0:
                    return ""
                dp[pos] = can_full
                continue

            mask = 0
            for q in range_states:
                if nm[q] & allowed:
                    mask |= bits[q]
            if mask == 0:
                return ""
            dp[pos] = mask

        if not (dp[0] & 1):
            return ""

        letters = [chr(97 + c) for c in range(26)]
        ans = []
        q = 0

        # Greedily reconstruct the lexicographically smallest valid string.
        for pos in range(L):
            allowed = dp[pos + 1] & filters[pos]
            row = trans[q]
            for c in range(26):
                nq = row[c]
                if allowed & bits[nq]:
                    ans.append(letters[c])
                    q = nq
                    break
            else:
                return ""

        return "".join(ans)