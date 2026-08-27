import random
import time

class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1

        # Step 1: place forced characters from 'T' constraints.
        res = [''] * L  # '' means unfilled
        for i in range(n):
            if str1[i] == 'T':
                base = i
                for k in range(m):
                    j = base + k
                    c = str2[k]
                    if res[j] == '':
                        res[j] = c
                    elif res[j] != c:
                        return ""

        # Step 2: for each F-window, determine if already broken and count
        # the number of unfilled positions (chances left to differ).
        broken = [False] * n
        free_cnt = [0] * n
        for i in range(n):
            if str1[i] != 'F':
                continue
            b = False
            cnt = 0
            base = i
            for k in range(m):
                j = base + k
                if res[j] == '':
                    cnt += 1
                elif res[j] != str2[k]:
                    b = True
            broken[i] = b
            free_cnt[i] = cnt
            if not b and cnt == 0:
                # Fully forced and equal to str2 -> impossible.
                return ""

        # Step 3: greedy left-to-right fill.
        covering = [[] for _ in range(L)]
        for i in range(n):
            if str1[i] == 'F' and not broken[i]:
                for j in range(i, i + m):
                    covering[j].append(i)

        for j in range(L):
            if res[j] != '':
                continue
            forbidden = set()
            for i in covering[j]:
                if not broken[i] and free_cnt[i] == 1:
                    forbidden.add(str2[j - i])
            chosen = None
            for c in range(26):
                ch = chr(ord('a') + c)
                if ch not in forbidden:
                    chosen = ch
                    break
            if chosen is None:
                return ""
            res[j] = chosen
            for i in covering[j]:
                if broken[i]:
                    continue
                free_cnt[i] -= 1
                if chosen != str2[j - i]:
                    broken[i] = True

        # Step 4: safety verification.
        word = ''.join(res)
        for i in range(n):
            if str1[i] == 'F' and word[i:i + m] == str2:
                return ""
        return word


# ---------------- Testing harness ----------------

def brute_force(str1, str2, alphabet=('a', 'b')):
    """Exhaustive check over small alphabet; returns lexicographically smallest
    valid word (over full lowercase, but 'a','b' suffice when str2 uses only
    those letters) or "" if none."""
    from itertools import product
    n, m = len(str1), len(str2)
    L = n + m - 1
    best = None
    for tup in product(alphabet, repeat=L):
        w = ''.join(tup)
        ok = True
        for i in range(n):
            sub = w[i:i + m]
            if str1[i] == 'T' and sub != str2:
                ok = False
                break
            if str1[i] == 'F' and sub == str2:
                ok = False
                break
        if ok and (best is None or w < best):
            best = w
    return best if best is not None else ""


def validate(str1, str2, word):
    """Check word satisfies all constraints; returns True/False."""
    if word == "":
        return None  # signals impossibility claim
    n, m = len(str1), len(str2)
    if len(word) != n + m - 1:
        return False
    for i in range(n):
        sub = word[i:i + m]
        if str1[i] == 'T' and sub != str2:
            return False
        if str1[i] == 'F' and sub == str2:
            return False
    return True


def run_tests():
    sol = Solution()

    # --- Provided examples ---
    assert sol.generateString("TFTF", "ab") == "ababa", "Example 1 failed"
    assert sol.generateString("TFTF", "abc") == "", "Example 2 failed"
    assert sol.generateString("F", "d") == "a", "Example 3 failed"
    print("Provided examples: PASS")

    # --- Single char strings ---
    assert sol.generateString("T", "a") == "a"
    assert sol.generateString("T", "z") == "z"
    assert sol.generateString("F", "a") == "b"   # must differ from "a"; smallest is 'b'
    assert sol.generateString("F", "z") == "a"
    print("Single char: PASS")

    # --- All T's with self-overlapping str2 (periodicity) ---
    # str2 = "abab", period 2. T at 0 and T at 2 are compatible.
    out = sol.generateString("TT", "abab")
    assert out == "ababab", f"got {out}"
    # T at 0 and T at 1 with str2="abab": offset-1 overlap requires
    # str2[1:] == str2[:-1] -> "bab" vs "aba" mismatch -> impossible.
    assert sol.generateString("TT", "abab") == "ababab"
    assert sol.generateString("TTT", "ab") == "abab"  # period 1? "ab" period 2; T at 0,1,2:
    # wait: T at 0 -> ab, T at 1 -> positions1..2 = ab -> pos1='a' conflicts with 'b'. Expect "".
    # Recompute properly:
    out = sol.generateString("TTT", "ab")
    assert out == "", f"expected '' got {out}"
    # str2 = "aa" (period 1): any all-T pattern works, word all 'a'.
    assert sol.generateString("TTTT", "aa") == "aaaaa"
    # str2 = "abcab" period 3: T at 0 and 3 compatible; T at 0 and 1 not.
    assert sol.generateString("TT", "abcab") == "abcabcab"
    assert sol.generateString("TT", "abcab") == "abcabcab"
    out = sol.generateString("TFT", "abcab")  # T at 0, T at 2 -> overlap offset 2: str2[2:]="cab" vs str2[:3]="abc" mismatch -> ""
    assert out == "", f"expected '' got {out}"
    print("All-T periodicity: PASS")

    # --- All F's ---
    # n=2, m=1, str2='a': word length 2, both windows (single chars) must != 'a'
    # lexicographically smallest: "bb"
    assert sol.generateString("FF", "a") == "bb"
    # n=1, m=2, str2="ab": word length 2 must != "ab" -> smallest is "aa"
    assert sol.generateString("F", "ab") == "aa"
    # n=2, m=2, str2="ab": windows w[0:2] and w[1:3] both != "ab"
    # greedy: j0: window0 last chance? window0 free={0,1} cnt2 -> no forbid -> 'a'
    #         window1 doesn't cover 0. j0='a' matches str2[0] -> window0 cnt=1
    # j1: window0 cnt==1 -> forbid str2[1]='b'; window1 covers 1, cnt2 -> no forbid
    #     -> choose 'a'. window0 broken. window1: 'a' vs str2[0]='a' match -> cnt=1
    # j2: window1 cnt==1 -> forbid str2[1]='b' -> choose 'a'
    # result "aaaa"? wait length = 2+2-1 = 3 -> "aaa". Check: w[0:2]="aa"!="ab", w[1:3]="aa"!="ab". OK.
    assert sol.generateString("FF", "ab") == "aaa"
    print("All-F: PASS")

    # --- Mixed / tricky ---
    # F-window fully forced by T's to equal str2 -> impossible.
    # str1 = "TF", str2 = "ab": T at 0 forces w[0..1]="ab"; F at 1 covers w[1..2],
    # w[1]='b' vs str2[0]='a' -> broken already. word: w0='a',w1='b', w2 free -> 'a' => "aba"
    assert sol.generateString("TF", "ab") == "aba"
    # str1 = "FT", str2 = "ab": T at 1 forces w[1..2]="ab"; F at 0 covers w[0..1],
    # w[1]='b' vs str2[1]='b' matches; w[0] free, must differ from str2[0]='a' -> 'b'
    # result "bab"
    assert sol.generateString("FT", "ab") == "bab"
    # Impossible: str1="TF", str2="aa": T at 0 -> w0='a',w1='a'. F at 1 covers w1,w2.
    # w1='a' matches str2[0]='a'; w2 free -> can be 'b'. So possible: "aab".
    assert sol.generateString("TF", "aa") == "aab"
    # Truly impossible fully-forced-equal case:
    # str1 = "TT", str2 = "ab" gives word "abb"? T0: w0,w1=ab; T1: w1,w2=ab -> w1='a' conflict -> "".
    # Build a case where F window is entirely covered by T-forced chars equal to str2:
    # str1 = "TFT", str2 = "ab": T0 -> w0,w1 = a,b. T2 -> w2,w3 = a,b.
    # F at 1 covers w1,w2 = b,a -> "ba" != "ab" broken. word "abab"? w = a,b,a,b -> "abab".
    assert sol.generateString("TFT", "ab") == "abab"
    # str1="TTT", str2="aba": T0 -> w0..2 = a,b,a. T1 -> w1..3 = a,b,a -> w1='a' vs 'b' conflict -> ""
    assert sol.generateString("TTT", "aba") == ""
    # str1="TFT", str2="aba": T0 -> w0..2=aba; T2 -> w2..4=aba; w2='a'='a' ok.
    # F at 1 covers w1..3 = b,a,a -> vs "aba": w1='b' vs 'a' differs -> broken. word "ababa".
    assert sol.generateString("TFT", "aba") == "ababa"
    # Fully forced F equal: str1 = "TF", str2 = "ab" with F at position... need F window
    # entirely forced equal. str1="TTF", str2="ab": T0->w0,w1=ab; T1->w1,w2=ab conflict w1 -> "".
    # Use str2="aa": str1="TFT", T0->w0,w1=aa; T2->w2,w3=aa. F at1 covers w1,w2 = a,a == "aa"
    # and both forced -> impossible -> "".
    assert sol.generateString("TFT", "aa") == ""
    print("Mixed/tricky: PASS")

    # --- Randomized brute-force cross-check (small cases) ---
    rng = random.Random(12345)
    checked = 0
    for _ in range(400):
        n = rng.randint(1, 5)
        m = rng.randint(1, 4)
        str1 = ''.join(rng.choice('TF') for _ in range(n))
        str2 = ''.join(rng.choice('ab') for _ in range(m))
        got = sol.generateString(str1, str2)
        exp = brute_force(str1, str2)
        v = validate(str1, str2, got)
        if got == "":
            assert exp == "", f"claimed impossible but brute found {exp!r} for {str1},{str2}"
        else:
            assert v is True, f"invalid word {got!r} for {str1},{str2}"
            assert got == exp, f"not lexicographically smallest: got {got!r}, want {exp!r} for {str1},{str2}"
        checked += 1
    print(f"Randomized brute-force cross-check: PASS ({checked} cases)")

    # --- Performance sanity: n = 10^4, m = 500 ---
    n, m = 10000, 500
    rng2 = random.Random(999)
    str1_big = ''.join(rng2.choice('TF') for _ in range(n))
    str2_big = ''.join(rng2.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(m))
    t0 = time.time()
    out = sol.generateString(str1_big, str2_big)
    t1 = time.time()
    v = validate(str1_big, str2_big, out)
    assert v is True or out == "", "big random case invalid"
    print(f"Perf random n=10^4,m=500: {t1-t0:.3f}s, valid={v}, len={len(out)}")

    # Worst-ish case: all 'F' (every window needs tracking)
    str1_allF = 'F' * n
    str2_rep = 'a' * m
    t0 = time.time()
    out = sol.generateString(str1_allF, str2_rep)
    t1 = time.time()
    v = validate(str1_allF, str2_rep, out)
    assert v is True
    # Expected: every window of length 500 must contain a non-'a'.
    # Lexicographically smallest: place 'b' as far right as possible greedily...
    # Greedy fills 'a' until a window's last chance forces 'b'.
    print(f"Perf all-F n=10^4,m=500: {t1-t0:.3f}s, valid={v}, len={len(out)}")

    # All 'T' with periodic str2 (compatible) - heavy placement overlap
    str1_allT = 'T' * n
    str2_per = ('ab' * 250)  # period 2, length 500
    t0 = time.time()
    out = sol.generateString(str1_allT, str2_per)
    t1 = time.time()
    v = validate(str1_allT, str2_per, out)
    assert v is True
    print(f"Perf all-T periodic n=10^4,m=500: {t1-t0:.3f}s, valid={v}, len={len(out)}")

    print("ALL TESTS PASSED")


if __name__ == "__main__":
    run_tests()