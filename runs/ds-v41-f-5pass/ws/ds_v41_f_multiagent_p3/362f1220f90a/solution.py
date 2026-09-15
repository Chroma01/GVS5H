import random
from itertools import product

class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        L = n + m - 1
        FREE = '#'
        ans = [FREE] * L

        # Pass 1: enforce every 'T' constraint exactly.
        for i in range(n):
            if str1[i] == 'T':
                for j in range(m):
                    k = i + j
                    c = str2[j]
                    cur = ans[k]
                    if cur != FREE and cur != c:
                        return ""
                    ans[k] = c

        # Pass 2: enforce every 'F' constraint, left to right.
        for i in range(n):
            if str1[i] == 'F':
                matched = True
                for j in range(m):
                    cur = ans[i + j]
                    if cur == FREE:
                        if str2[j] != 'a':
                            matched = False
                            break
                    elif cur != str2[j]:
                        matched = False
                        break
                if matched:
                    # Break the equality at the rightmost free slot.
                    for j in range(m - 1, -1, -1):
                        k = i + j
                        if ans[k] == FREE:
                            ans[k] = 'b'
                            break
                    else:
                        return ""

        # Pass 3: all remaining free positions become 'a'.
        return ''.join('a' if c == FREE else c for c in ans)


def brute(str1, str2, alphabet):
    """Independent reference: enumerate in lexicographic order, return first valid."""
    n, m = len(str1), len(str2)
    L = n + m - 1
    for chars in product(alphabet, repeat=L):
        word = ''.join(chars)
        ok = True
        for i in range(n):
            sub = word[i:i+m]
            if str1[i] == 'T':
                if sub != str2:
                    ok = False
                    break
            else:
                if sub == str2:
                    ok = False
                    break
        if ok:
            return word
    return ""


def run_exhaustive(alphabet, max_n, max_m):
    total = 0
    mismatches = []
    for n in range(1, max_n + 1):
        for str1_tuple in product('TF', repeat=n):
            str1 = ''.join(str1_tuple)
            for m in range(1, max_m + 1):
                for str2_tuple in product(alphabet, repeat=m):
                    str2 = ''.join(str2_tuple)
                    total += 1
                    g = Solution().generateString(str1, str2)
                    b = brute(str1, str2, alphabet)
                    if g != b:
                        mismatches.append((str1, str2, b, g))
    return total, mismatches


def run_random(num_cases, max_n, max_m, alphabet, seed):
    random.seed(seed)
    total = 0
    mismatches = []
    for _ in range(num_cases):
        n = random.randint(1, max_n)
        m = random.randint(1, max_m)
        str1 = ''.join(random.choice('TF') for _ in range(n))
        str2 = ''.join(random.choice(alphabet) for _ in range(m))
        total += 1
        g = Solution().generateString(str1, str2)
        b = brute(str1, str2, alphabet)
        if g != b:
            mismatches.append((str1, str2, b, g))
    return total, mismatches


def run_targeted(target_str2s, max_n):
    total = 0
    mismatches = []
    for str2 in target_str2s:
        for n in range(1, max_n + 1):
            for str1_tuple in product('TF', repeat=n):
                str1 = ''.join(str1_tuple)
                total += 1
                g = Solution().generateString(str1, str2)
                b = brute(str1, str2, 'ab')  # targets only use a,b
                if g != b:
                    mismatches.append((str1, str2, b, g))
    return total, mismatches


if __name__ == "__main__":
    total_all = 0
    mismatches_all = []

    t, mm = run_exhaustive('ab', 5, 4)
    total_all += t
    mismatches_all.extend(mm)
    print(f"Exhaustive {{a,b}} n<=5 m<=4: {t} cases, {len(mm)} mismatches")

    t, mm = run_exhaustive('abc', 5, 3)
    total_all += t
    mismatches_all.extend(mm)
    print(f"Exhaustive {{a,b,c}} n<=5 m<=3: {t} cases, {len(mm)} mismatches")

    t, mm = run_random(50, 8, 8, 'ab', 12345)
    total_all += t
    mismatches_all.extend(mm)
    print(f"Random {{a,b}} n<=8 m<=8: {t} cases, {len(mm)} mismatches")

    t, mm = run_random(50, 6, 4, 'abc', 67890)
    total_all += t
    mismatches_all.extend(mm)
    print(f"Random {{a,b,c}} n<=6 m<=4: {t} cases, {len(mm)} mismatches")

    targets = ["aab", "aabb", "aabbb", "aba", "baa", "ab", "ba", "aa", "bb", "a", "b"]
    t, mm = run_targeted(targets, 7)
    total_all += t
    mismatches_all.extend(mm)
    print(f"Targeted probes n<=7: {t} cases, {len(mm)} mismatches")

    print(f"TOTAL: {total_all} cases, {len(mismatches_all)} mismatches")
    if mismatches_all:
        print("Counterexamples:")
        for str1, str2, expected, got in mismatches_all[:10]:
            print(f"  str1={str1!r}, str2={str2!r}, expected={expected!r}, got={got!r}")
    else:
        print("0 mismatches")