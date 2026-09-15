class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        left, middle, right = p.split('*')

        def occurrences(text: str, pattern: str):
            """
            Returns all start indices where pattern occurs in text, in sorted order.
            Uses KMP for linear time. Empty patterns return an empty list because
            empty fragments are handled separately by the caller.
            """
            m = len(pattern)
            n = len(text)
            if m == 0 or m > n:
                return []

            # KMP prefix function.
            pi = [0] * m
            for i in range(1, m):
                j = pi[i - 1]
                while j > 0 and pattern[i] != pattern[j]:
                    j = pi[j - 1]
                if pattern[i] == pattern[j]:
                    j += 1
                pi[i] = j

            # KMP search.
            occ = []
            j = 0
            for i, ch in enumerate(text):
                while j > 0 and ch != pattern[j]:
                    j = pi[j - 1]
                if ch == pattern[j]:
                    j += 1
                    if j == m:
                        occ.append(i - m + 1)
                        j = pi[j - 1]
            return occ

        occ_left = occurrences(s, left) if left else []
        occ_mid = occurrences(s, middle) if middle else []
        occ_right = occurrences(s, right) if right else []

        # p == "**"
        if not left and not middle and not right:
            return 0

        # Every non-empty literal fragment must occur at least once.
        if left and not occ_left:
            return -1
        if middle and not occ_mid:
            return -1
        if right and not occ_right:
            return -1

        left_len = len(left)
        mid_len = len(middle)
        right_len = len(right)

        INF = 10**18
        ans = INF

        # Case 1: middle is empty, so we only need left before right.
        if not middle:
            if not left:
                return right_len if right else 0
            if not right:
                return left_len if left else 0

            i = 0
            latest_left = -1

            # Sweep right occurrences and keep the latest left occurrence
            # whose end is <= current right start.
            for start_right in occ_right:
                while i < len(occ_left) and occ_left[i] + left_len <= start_right:
                    latest_left = occ_left[i]
                    i += 1

                if latest_left != -1:
                    length = start_right + right_len - latest_left
                    if length < ans:
                        ans = length

            return ans if ans != INF else -1

        # Case 2: middle is non-empty.
        # If both sides are empty, the shortest match is exactly one middle occurrence.
        if not left and not right:
            return mid_len

        i_left = 0
        latest_left = -1
        i_right = 0

        len_occ_left = len(occ_left)
        len_occ_right = len(occ_right)

        # Sweep middle occurrences in increasing start order.
        for start_mid in occ_mid:
            if left:
                # Latest left occurrence ending at or before this middle start.
                while i_left < len_occ_left and occ_left[i_left] + left_len <= start_mid:
                    latest_left = occ_left[i_left]
                    i_left += 1

                if latest_left == -1:
                    continue

                start = latest_left
            else:
                # Leading star can be trimmed away in an optimal substring.
                start = start_mid

            threshold = start_mid + mid_len

            if right:
                # Earliest right occurrence starting at or after this middle end.
                while i_right < len_occ_right and occ_right[i_right] < threshold:
                    i_right += 1

                # Middle starts only increase, so no later middle can match right either.
                if i_right == len_occ_right:
                    break

                end = occ_right[i_right] + right_len
            else:
                # Trailing star can be trimmed away in an optimal substring.
                end = threshold

            length = end - start
            if length < ans:
                ans = length

        return ans if ans != INF else -1