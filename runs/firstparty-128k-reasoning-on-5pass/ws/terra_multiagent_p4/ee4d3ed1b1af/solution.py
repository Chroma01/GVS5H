class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)
        first_star = p.find('*')
        second_star = p.find('*', first_star + 1)

        a = p[:first_star]
        b = p[first_star + 1:second_star]
        c = p[second_star + 1:]

        def occurrences(pattern: str):
            if not pattern:
                return list(range(n + 1))

            m = len(pattern)
            pi = [0] * m
            matched = 0

            for i in range(1, m):
                while matched > 0 and pattern[i] != pattern[matched]:
                    matched = pi[matched - 1]
                if pattern[i] == pattern[matched]:
                    matched += 1
                pi[i] = matched

            result = []
            matched = 0
            for i, ch in enumerate(s):
                while matched > 0 and ch != pattern[matched]:
                    matched = pi[matched - 1]
                if ch == pattern[matched]:
                    matched += 1
                if matched == m:
                    result.append(i - m + 1)
                    matched = pi[matched - 1]

            return result

        la, lb, lc = len(a), len(b), len(c)
        occ_a = occurrences(a)
        occ_b = occurrences(b)
        occ_c = occurrences(c)

        # latest_a[x]: largest start position of an a occurrence ending at or before x.
        a_starts = [False] * (n + 1)
        for pos in occ_a:
            a_starts[pos] = True

        latest_a = [-1] * (n + 1)
        best_start = -1
        for boundary in range(n + 1):
            start = boundary - la
            if start >= 0 and a_starts[start]:
                best_start = max(best_start, start)
            latest_a[boundary] = best_start

        # earliest_c[x]: smallest start position of a c occurrence starting at or after x.
        c_starts = [False] * (n + 1)
        for pos in occ_c:
            c_starts[pos] = True

        earliest_c = [n + 1] * (n + 1)
        best_start = n + 1
        for boundary in range(n, -1, -1):
            if c_starts[boundary]:
                best_start = boundary
            earliest_c[boundary] = best_start

        answer = n + 1

        for mid_start in occ_b:
            left_start = latest_a[mid_start]
            right_boundary = mid_start + lb

            if left_start == -1:
                continue

            right_start = earliest_c[right_boundary]
            if right_start == n + 1:
                continue

            answer = min(answer, right_start + lc - left_start)

        return answer if answer <= n else -1