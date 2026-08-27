import random
import itertools
from functools import lru_cache

class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1
        p = [ord(c) - 97 for c in str2]
        pi = [0] * m
        for i in range(1, m):
            j = pi[i-1]
            while j > 0 and p[i] != p[j]:
                j = pi[j-1]
            if p[i] == p[j]:
                j += 1
            pi[i] = j
        pi_last = pi[m-1]
        trans = [[0]*26 for _ in range(m+1)]
        for q in range(m+1):
            row = trans[q]
            if q == 0:
                for ci in range(26):
                    row[ci] = 1 if ci == p[0] else 0
            else:
                fallback = trans[pi[q-1]]
                if q < m:
                    target = q + 1
                    pat_char = p[q]
                    for ci in range(26):
                        if ci == pat_char:
                            row[ci] = target
                        else:
                            row[ci] = fallback[ci]
                else:
                    for ci in range(26):
                        row[ci] = fallback[ci]
        bits = [1 << i for i in range(m)]
        all_next = [0] * m
        non_match_next = [0] * m
        for s in range(m):
            row = trans[s]
            mask_all = 0
            mask_non = 0
            for ci in range(26):
                fn = row[ci]
                if fn == m:
                    ns = pi_last
                else:
                    ns = fn
                    mask_non |= bits[ns]
                mask_all |= bits[ns]
            all_next[s] = mask_all
            non_match_next[s] = mask_non
        ok = [0] * (L + 1)
        ok[L] = (1 << m) - 1
        t_bit = bits[m-1]
        for pos in range(L - 1, -1, -1):
            ok_next = ok[pos + 1]
            idx = pos - (m - 1)
            if idx >= 0:
                if str1[idx] == 'T':
                    ok[pos] = t_bit if ((ok_next >> pi_last) & 1) else 0
                else:
                    masks = non_match_next
                    cur = 0
                    for s in range(m):
                        if masks[s] & ok_next:
                            cur |= bits[s]
                    ok[pos] = cur
            else:
                masks = all_next
                cur = 0
                for s in range(m):
                    if masks[s] & ok_next:
                        cur |= bits[s]
                ok[pos] = cur
            if ok[pos] == 0:
                return ""
        if not (ok[0] & 1):
            return ""
        ans = []
        state = 0
        for pos in range(L):
            idx = pos - (m - 1)
            req = str1[idx] if idx >= 0 else None
            ok_next = ok[pos + 1]
            row = trans[state]
            chosen = False
            for ci in range(26):
                fn = row[ci]
                if fn == m:
                    if req == 'F':
                        continue
                    ns = pi_last
                else:
                    if req == 'T':
                        continue
                    ns = fn
                if (ok_next >> ns) & 1:
                    ans.append(chr(97 + ci))
                    state = ns
                    chosen = True
                    break
            if not chosen:
                return ""
        return ''.join(ans)


def is_valid(word: str, str1: str, str2: str) -> bool:
    n = len(str1)
    m = len(str2)
    if len(word) != n + m - 1:
        return False
    for i, ch in enumerate(str1):
        if (ch == 'T') != (word[i:i + m] == str2):
            return False
    return True


def brute_force(str1: str, str2: str, alphabet: str):
    n = len(str1)
    m = len(str2)
    L = n + m - 1
    for tup in itertools.product(alphabet, repeat=L):
        w = ''.join(tup)
        ok = True
        for i, ch in enumerate(str1):
            if (ch == 'T') != (w[i:i + m] == str2):
                ok = False
                break
        if ok:
            return w
    return None


def check_expected(str1: str, str2: str, expected: str, label: str) -> bool:
    sol = Solution().generateString(str1, str2)
    if sol != expected:
        print(f"FAIL {label}: str1={str1!r} str2={str2!r} expected={expected!r} got={sol!r}")
        return False
    if sol and not is_valid(sol, str1, str2):
        print(f"FAIL {label}: invalid solution str1={str1!r} str2={str2!r} got={sol!r}")
        return False
    return True


def check_brute(str1: str, str2: str, alphabet: str, label: str) -> bool:
    sol = Solution().generateString(str1, str2)
    if sol and not is_valid(sol, str1, str2):
        print(f"FAIL {label}: invalid solution str1={str1!r} str2={str2!r} got={sol!r}")
        return False
    exp = brute_force(str1, str2, alphabet) or ""
    if sol != exp:
        print(f"FAIL {label}: str1={str1!r} str2={str2!r} expected={exp!r} got={sol!r}")
        return False
    return True


def main() -> None:
    examples = [
        ("TFTF", "ab", "ababa", "example1"),
        ("TFTF", "abc", "", "example2"),
        ("F", "d", "a", "example3"),
    ]
    for s1, s2, exp, label in examples:
        if not check_expected(s1, s2, exp, label):
            return

    edge_cases = [
        ("TFT", "a", "aba", "m1 mixed"),
        ("FFF", "a", "bbb", "m1 allF"),
        ("T", "z", "z", "m1 T z"),
        ("F", "z", "a", "m1 F z"),
        ("FTF", "b", "aba", "m1 mixed b"),
        ("TTT", "aa", "aaaa", "allT compatible"),
        ("TT", "ab", "", "allT incompatible"),
        ("TTT", "abc", "", "allT incompatible abc"),
        ("TT", "aaa", "aaaa", "allT aaa"),
        ("FFF", "aa", "abab", "allF aa"),
        ("FFF", "ab", "aaaa", "allF ab"),
        ("FFFF", "aaa", "aabaab", "allF aaa"),
        ("FFFF", "abc", "aaaaaa", "allF abc"),
        ("T", "abc", "abc", "n1 T abc"),
        ("F", "aaa", "aab", "n1 F aaa"),
        ("F", "abc", "aaa", "n1 F abc"),
        ("F", "a", "b", "n1 F a"),
        ("T", "a", "a", "n1 T a"),
    ]
    for s1, s2, exp, label in edge_cases:
        if not check_expected(s1, s2, exp, label):
            return

    # Exhaustive brute-force over the requested small range.  str2 is over
    # {'a','b'}; candidate words are searched over {'a','b','c'}.  One extra
    # letter is sufficient because any character outside str2 makes a window
    # unequal to str2, and 'c' is the smallest such extra letter.
    for n in range(1, 5):
        for m in range(1, 4):
            for s1_tuple in itertools.product("TF", repeat=n):
                for s2_tuple in itertools.product("ab", repeat=m):
                    s1 = ''.join(s1_tuple)
                    s2 = ''.join(s2_tuple)
                    if not check_brute(s1, s2, "abc", f"exhaustive n={n} m={m}"):
                        return

    print("PASS")


if __name__ == "__main__":
    main()