class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1
        s2 = [ord(ch) - 97 for ch in str2]

        # KMP prefix function for str2.
        pi = [0] * m
        for i in range(1, m):
            j = pi[i - 1]
            while j and s2[i] != s2[j]:
                j = pi[j - 1]
            if s2[i] == s2[j]:
                j += 1
            pi[i] = j

        # KMP automaton. States are 0..m, where state m means the last m
        # characters are exactly str2.
        trans = [[0] * 26 for _ in range(m + 1)]
        for q in range(m):
            if q:
                row = trans[pi[q - 1]].copy()
            else:
                row = [0] * 26
            row[s2[q]] = q + 1
            trans[q] = row
        trans[m] = trans[pi[m - 1]].copy()

        states = m + 1
        all_mask = (1 << states) - 1
        match_mask = 1 << m
        non_match_mask = all_mask ^ match_mask
        state_bit = [1 << q for q in range(states)]

        # pred[r] = bitset of states that can reach r by one character.
        pred = [0] * states
        for q in range(states):
            bq = state_bit[q]
            for r in trans[q]:
                pred[r] |= bq

        # Byte-chunk table for fast union of predecessor bitsets.
        chunks = (states + 7) // 8
        table = []
        for k in range(chunks):
            base = k * 8
            tbl = [0] * 256
            for val in range(1, 256):
                lb = val & -val
                b = lb.bit_length() - 1
                idx = base + b
                prev = val ^ lb
                if idx < states:
                    tbl[val] = tbl[prev] | pred[idx]
                else:
                    tbl[val] = tbl[prev]
            table.append(tbl)

        def pred_union(allowed: int) -> int:
            res = 0
            k = 0
            x = allowed
            while x:
                byte = x & 255
                if byte:
                    res |= table[k][byte]
                x >>= 8
                k += 1
            return res

        can_match = pred[m]
        can_non_match = pred_union(non_match_mask)

        # masks[p] constrains the automaton state after reading position p.
        masks = [all_mask] * L
        for i, ch in enumerate(str1):
            p = i + m - 1
            masks[p] = match_mask if ch == 'T' else non_match_mask

        # good[p] = states before position p from which suffix p..L-1 is feasible.
        good = [0] * (L + 1)
        good[L] = all_mask

        for p in range(L - 1, -1, -1):
            allowed = good[p + 1] & masks[p]
            if allowed == 0:
                break

            if allowed == all_mask:
                gp = all_mask
            elif allowed == match_mask:
                gp = can_match
            elif allowed == non_match_mask:
                gp = can_non_match
            else:
                gp = pred_union(allowed)

            good[p] = gp
            if gp == 0:
                break

        if (good[0] & 1) == 0:
            return ""

        # Greedy lexicographic reconstruction using the feasibility DP.
        ans = []
        state = 0
        for p in range(L):
            allowed = good[p + 1] & masks[p]
            row = trans[state]
            for c in range(26):
                r = row[c]
                if allowed & state_bit[r]:
                    ans.append(chr(97 + c))
                    state = r
                    break
            else:
                return ""

        return "".join(ans)


def _is_generated(word: str, str1: str, str2: str) -> bool:
    if len(word) != len(str1) + len(str2) - 1:
        return False
    m = len(str2)
    for i, ch in enumerate(str1):
        if (word[i:i + m] == str2) != (ch == 'T'):
            return False
    return True


def _brute_generate(str1: str, str2: str, alphabet=None) -> str:
    n = len(str1)
    m = len(str2)
    L = n + m - 1

    if alphabet is None:
        # Exact reduced alphabet: any outside character can be replaced by
        # 'a' or 'b' that mismatches str2 at that position, preserving all
        # T/F constraints and not increasing lexicographic order.
        alphabet = sorted(set(str2) | {'a', 'b'})
    else:
        alphabet = sorted(alphabet)

    word = []

    def dfs(pos: int):
        if pos == L:
            return ''.join(word)

        for ch in alphabet:
            word.append(ch)

            # A window becomes complete exactly at its end position.
            if pos >= m - 1:
                start = pos - m + 1
                if start < n:
                    sub = ''.join(word[start:])
                    if (sub == str2) != (str1[start] == 'T'):
                        word.pop()
                        continue

            res = dfs(pos + 1)
            if res is not None:
                return res
            word.pop()

        return None

    res = dfs(0)
    return res if res is not None else ''


def _run_validation() -> None:
    import random
    import sys
    from itertools import product

    sys.setrecursionlimit(10000)
    sol = Solution()
    failures = []
    tests = []
    seen = set()

    def add_test(a: str, b: str) -> None:
        if (a, b) not in seen:
            seen.add((a, b))
            tests.append((a, b))

    edge_tests = [
        ('TFTF', 'ab'), ('TFTF', 'abc'), ('F', 'd'),
        ('T', 'd'), ('T', 'z'), ('F', 'z'), ('FF', 'a'), ('TF', 'a'),
        ('FT', 'a'), ('TT', 'a'), ('T', 'ab'), ('F', 'ab'),
        ('TT', 'ab'), ('TT', 'aa'), ('TTT', 'aaa'), ('TFT', 'aa'),
        ('TFT', 'aaa'), ('TFF', 'aa'), ('TFF', 'ab'), ('FFT', 'ab'),
        ('TFFF', 'ab'), ('FFFT', 'ab'), ('FFF', 'ab'), ('FFF', 'a'),
        ('TFT', 'ab'), ('TFTF', 'aa'), ('T', 'aaa'), ('TT', 'aaa'),
        ('FTF', 'aaa'), ('FF', 'aaaa'), ('TFF', 'abc'), ('FFT', 'abc'),
        ('TFFTF', 'ab'), ('TFT', 'ababa'), ('TFT', 'abab'),
        ('TT', 'ababa'), ('TFT', 'aaaaa'),
    ]
    for a, b in edge_tests:
        add_test(a, b)

    # Exhaustive small binary cases.
    for n in range(1, 4):
        for m in range(1, 4):
            for mask in range(1 << n):
                str1 = ''.join('T' if (mask >> i) & 1 else 'F' for i in range(n))
                for s2mask in range(1 << m):
                    str2 = ''.join('a' if (s2mask >> i) & 1 else 'b' for i in range(m))
                    add_test(str1, str2)

    # Exhaustive very small ternary cases.
    for n in range(1, 3):
        for m in range(1, 3):
            for mask in range(1 << n):
                str1 = ''.join('T' if (mask >> i) & 1 else 'F' for i in range(n))
                for tup in product('abc', repeat=m):
                    add_test(str1, ''.join(tup))

    # Seeded random cases.
    random.seed(123456789)
    for _ in range(250):
        n = random.randint(1, 5)
        m = random.randint(1, 4)
        str1 = ''.join(random.choice('TF') for _ in range(n))
        chars = 'ab' if random.random() < 0.7 else 'abc'
        if random.random() < 0.2:
            str2 = random.choice(chars) * m
        else:
            str2 = ''.join(random.choice(chars) for _ in range(m))
        add_test(str1, str2)

    for _ in range(80):
        n = random.randint(1, 6)
        m = random.randint(1, 5)
        str1 = ''.join(random.choice('TF') for _ in range(n))
        str2 = ''.join(random.choice('ab') for _ in range(m))
        add_test(str1, str2)

    for str1, str2 in tests:
        expected = _brute_generate(str1, str2)
        got = sol.generateString(str1, str2)
        if got != expected:
            failures.append((str1, str2, got, expected))
        elif got and not _is_generated(got, str1, str2):
            failures.append((str1, str2, got, 'invalid'))

    # Full lowercase brute-force cross-check for very small lengths.
    full_alphabet = 'abcdefghijklmnopqrstuvwxyz'
    full_tests = []
    for str1 in ('F', 'T', 'FF', 'TF', 'FT', 'TT', 'FFF', 'TFT', 'FTF', 'TFF'):
        for str2 in ('a', 'b', 'z', 'ab', 'ba', 'aa', 'abc', 'aaa', 'aba', 'zzz'):
            if len(str1) + len(str2) - 1 <= 3:
                full_tests.append((str1, str2))

    for str1, str2 in full_tests:
        expected = _brute_generate(str1, str2, full_alphabet)
        got = sol.generateString(str1, str2)
        if got != expected:
            failures.append((str1, str2, got, expected))
        elif got and not _is_generated(got, str1, str2):
            failures.append((str1, str2, got, 'invalid'))

    if failures:
        print('FAIL')
        print(f'{len(failures)} failing test(s)')
        for item in failures[:10]:
            print(item)
    else:
        print(f'PASS ({len(tests) + len(full_tests)} tests)')


if __name__ == '__main__':
    _run_validation()