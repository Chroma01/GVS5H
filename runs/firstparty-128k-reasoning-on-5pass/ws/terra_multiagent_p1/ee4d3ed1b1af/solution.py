class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)
        a, b, c = p.split('*')

        def occurrences(pattern: str):
            m = len(pattern)
            if m == 0:
                return list(range(n + 1))

            pi = [0] * m
            j = 0
            for i in range(1, m):
                while j > 0 and pattern[i] != pattern[j]:
                    j = pi[j - 1]
                if pattern[i] == pattern[j]:
                    j += 1
                pi[i] = j

            result = []
            j = 0
            for i, ch in enumerate(s):
                while j > 0 and ch != pattern[j]:
                    j = pi[j - 1]
                if ch == pattern[j]:
                    j += 1
                if j == m:
                    result.append(i - m + 1)
                    j = pi[j - 1]
            return result

        def successor_array(starts):
            present = [False] * (n + 1)
            for pos in starts:
                present[pos] = True

            nxt = [n + 1] * (n + 2)
            nearest = n + 1
            for i in range(n, -1, -1):
                if present[i]:
                    nearest = i
                nxt[i] = nearest
            return nxt

        occ_a = occurrences(a)
        occ_b = occurrences(b)
        occ_c = occurrences(c)

        next_b = successor_array(occ_b)
        next_c = successor_array(occ_c)

        len_a = len(a)
        len_b = len(b)
        len_c = len(c)

        answer = n + 1

        for start_a in occ_a:
            required_b = start_a + len_a
            if required_b > n:
                continue

            start_b = next_b[required_b]
            if start_b > n:
                continue

            required_c = start_b + len_b
            if required_c > n:
                continue

            start_c = next_c[required_c]
            if start_c > n:
                continue

            end_c = start_c + len_c
            if end_c <= n:
                answer = min(answer, end_c - start_a)

        return answer if answer <= n else -1