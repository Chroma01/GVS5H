class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        n = len(s)
        a, b, c = p.split('*')

        def find_occurrences(pattern: str):
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

        def build_next(pattern: str):
            if not pattern:
                return None

            occurrence = bytearray(n + 1)
            for pos in find_occurrences(pattern):
                occurrence[pos] = 1

            nxt = [n + 1] * (n + 2)
            for i in range(n, -1, -1):
                if occurrence[i]:
                    nxt[i] = i
                else:
                    nxt[i] = nxt[i + 1]
            return nxt

        starts_a = find_occurrences(a)
        next_b = build_next(b)
        next_c = build_next(c)

        len_a, len_b, len_c = len(a), len(b), len(c)
        answer = n + 1

        for start_a in starts_a:
            boundary_b = start_a + len_a

            if len_b == 0:
                start_b = boundary_b
            else:
                start_b = next_b[boundary_b]
                if start_b > n:
                    continue

            boundary_c = start_b + len_b

            if len_c == 0:
                start_c = boundary_c
            else:
                start_c = next_c[boundary_c]
                if start_c > n:
                    continue

            answer = min(answer, start_c + len_c - start_a)

        return answer if answer <= n else -1