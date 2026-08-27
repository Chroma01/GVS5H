import sys
import random
import string
from itertools import product

class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        N = n + m - 1                     # length of the required word

        # ------------------------------------------------------------
        # 1. forced positions caused by 'T'
        forced = [None] * N                # None = free, else a letter
        for i, ch in enumerate(str1):
            if ch == 'T':
                for j in range(m):
                    pos = i + j
                    c = str2[j]
                    cur = forced[pos]
                    if cur is None:
                        forced[pos] = c
                    elif cur != c:        # conflict between two 'T's
                        return ""

        # ------------------------------------------------------------
        # 2. handle every 'F' interval
        #    required_at_deadline[p] stores letters that must NOT appear at p
        required_at_deadline = [[] for _ in range(N)]

        for i, ch in enumerate(str1):
            if ch != 'F':
                continue
            satisfied = False
            max_free = -1                  # largest free position in this interval
            # scan the interval
            for j in range(m):
                pos = i + j
                req = str2[j]
                fc = forced[pos]
                if fc is not None:
                    if fc != req:         # forced mismatch -> already satisfied
                        satisfied = True
                        break
                    # else forced and equal -> cannot be used for breaking
                else:
                    if pos > max_free:    # remember the latest free position
                        max_free = pos
            if satisfied:
                continue                    # this interval already fine
            if max_free == -1:             # no free place to break it
                return ""
            # schedule this interval at its deadline (the largest free position)
            need = str2[max_free - i]      # character that would make the substring equal to str2
            required_at_deadline[max_free].append(need)

        # ------------------------------------------------------------
        # 3. construct the answer from left to right (lexicographically minimal)
        ans = [''] * N
        for p in range(N):
            fc = forced[p]
            reqs = required_at_deadline[p]
            if fc is not None:                     # forced character
                # it must differ from every required letter at this deadline
                for r in reqs:
                    if fc == r:
                        return ""
                ans[p] = fc
            else:
                if reqs:                            # this position is a deadline
                    forbidden = set(reqs)           # set of letters that are forbidden at this deadline
                    # smallest letter not in the forbidden set
                    chosen = None
                    for code in range(26):
                        cand = chr(ord('a') + code)
                        if cand not in forbidden:
                            chosen = cand
                            break
                    if chosen is None:               # no possible letter (all 26 forbidden)
                        return ""
                    ans[p] = chosen
                else:                               # completely free, no deadline
                    ans[p] = 'a'

        return ''.join(ans)


# ------------------------------------------------------------
# Helper functions for testing
# ------------------------------------------------------------
def is_feasible(word: str, str1: str, str2: str) -> bool:
    """Check whether `word` satisfies all constraints of str1/str2."""
    n = len(str1)
    m = len(str2)
    N = len(word)
    if N != n + m - 1:
        return False
    for i, ch in enumerate(str1):
        if word[i:i+m] == str2 and ch == 'T':
            return False
        if word[i:i+m] != str2 and ch == 'F':
            return False
    return True

def brute_force_small(str1: str, str2: str, alphabet):
    """Find lexicographically smallest feasible word using brute force (small cases)."""
    n = len(str1)
    m = len(str2)
    N = n + m - 1
    # generate all strings of length N over the given alphabet, in lexicographic order
    for letters in product(alphabet, repeat=N):
        w = ''.join(letters)
        if is_feasible(w, str1, str2):
            return w
    return ""

def test_random_small():
    """Run many random tests with small sizes and compare with brute force."""
    random.seed(42)
    alphabet = ['a', 'b', 'c', 'd']  # limited alphabet for brute force
    max_n = 5
    max_m = 3
    total_tests = 0
    mismatches = 0
    for n in range(1, max_n + 1):
        for m in range(1, max_m + 1):
            # generate all possible str1 patterns of length n
            for pat in product('TF', repeat=n):
                str1 = ''.join(pat)
                # generate random str2 with letters from alphabet
                str2 = ''.join(random.choice(alphabet) for _ in range(m))
                # run algorithm
                sol = Solution().generateString(str1, str2)
                # brute force
                brute = brute_force_small(str1, str2, alphabet)
                # validate algorithm's solution
                if sol != "":
                    if not is_feasible(sol, str1, str2):
                        print(f"FAIL: algorithm returned infeasible solution for str1={str1}, str2={str2}")
                        print(f"   got: {sol}")
                        mismatches += 1
                        continue
                # compare
                if sol != brute:
                    # Note: brute force uses limited alphabet; algorithm may produce a word outside it.
                    # To handle this, we accept algorithm's answer if it is feasible and no better word exists in the limited alphabet.
                    # But we can also check that brute force answer (if exists) is lexicographically <= algorithm's answer.
                    if brute != "" and sol != "" and brute < sol:
                        print(f"DIFF: algorithm not lexicographically minimal for str1={str1}, str2={str2}")
                        print(f"   brute: {brute}")
                        print(f"   algo : {sol}")
                        mismatches += 1
                    elif brute == "" and sol != "":
                        # brute says impossible, algorithm found a solution; check if solution really exists with full alphabet
                        # We cannot be sure with limited alphabet; we can test with full alphabet for this case.
                        # As a sanity check, we verify feasibility (already done) and that there is no solution in full alphabet? Hard.
                        # We'll just flag as potential issue.
                        print(f"DIFF: brute says impossible, algorithm gives solution for str1={str1}, str2={str2}")
                        print(f"   algo: {sol}")
                        mismatches += 1
                total_tests += 1
    print(f"Total small random tests: {total_tests}, mismatches: {mismatches}")

def test_unsatisfiable_cases():
    """Handcrafted unsatisfiable cases."""
    # Example 2 from statement
    sol = Solution().generateString("TFTF", "abc")
    assert sol == "", f"Expected empty, got {sol}"
    # Two T's overlapping with different letters
    sol = Solution().generateString("TT", "ab")
    # i=0 forces 0='a',1='b'; i=1 forces 1='a',2='b' => conflict at pos1
    assert sol == "", f"Expected empty, got {sol}"
    # F interval with no free position
    # n=2, m=3, str1="TF", str2="abc"
    # T forces 0,1,2; F interval at i=1 covers positions 1,2,3.
    # positions 1,2 forced, 3 is free -> not impossible. Let's create impossible case:
    # str1="FF", str2="ab", n=2,m=2. No free positions? Actually each interval has one free position (i+0). So not impossible.
    # Need a case where all positions of an interval are forced and match required chars.
    # Example: n=2, m=2, str1="TF", str2="ab"
    # T at i=0 forces 0='a',1='b'.
    # F at i=1 covers positions 1,2. Forced[1]='b' matches required 'a'? No, required for i=1 pos1 = 'a', mismatch => satisfied.
    # Need both positions forced and equal.
    # Let n=3,m=2, str1="TTF", str2="ab"
    # i=0 T forces 0='a',1='b'
    # i=1 T forces 1='a',2='b' (conflict at pos1) -> returns empty already.
    # Better: n=3,m=2, str1="TFF", str2="ab"
    # T at i=0 forces 0='a',1='b'
    # F at i=1 covers 1,2: forced[1]='b' matches required 'a'? No mismatch => satisfied
    # F at i=2 covers 2,3: forced[2] is None (free), forced[3] is None (free) -> max_free=3, need='b', schedule.
    # So feasible.
    # Construct impossible: need an F interval where all positions are forced and equal to required.
    # Example: n=2, m=3, str1="TFF", str2="abc"
    # T at i=0 forces 0='a',1='b',2='c'
    # F at i=1 covers positions 1,2,3. forced[1]='b' matches required 'a'? No mismatch => satisfied
    # F at i=2 covers 2,3,4. forced[2]='c' matches required 'a'? No => satisfied
    # Not impossible.
    # Need an F interval where forced positions exactly match required for each offset.
    # Example: str1="FT", str2="a", m=1
    # i=0 F covers pos0; no forced -> can be satisfied.
    # Let's craft: n=2, m=2, str1="TF", str2="ab"
    # T at i=0 forces 0='a',1='b'
    # F at i=1 covers positions 1,2. forced[1]='b' matches required 'a'? No -> satisfied
    # Not impossible.
    # Actually we can force both positions of an interval and have them match.
    # Example: n=2,m=3, str1="TT", str2="abc"
    # i=0 forces 0='a',1='b',2='c'
    # i=1 forces 1='a',2='b',3='c' => conflict at 1 and 2, returns empty.
    # So we already have unsatisfiable detection.
    # Another unsatisfiable: an F interval with no free position and not already satisfied.
    # Example: n=2,m=2, str1="FF", str2="ab", but also have T that forces positions 0 and 1 equal to 'a','b' respectively.
    # Actually we need T that forces both positions of an F interval to match required.
    # Let's construct: n=2,m=2, str1="TF", str2="ab"
    # T at i=0 forces 0='a',1='b'
    # F at i=1 covers positions 1,2. forced[1]='b' matches required 'a'? No mismatch => satisfied.
    # To have forced positions matching required for both positions:
    # Need T at i=0 that forces positions 0,1 = 'a','b'
    # and F at i=1 that needs positions 1='a',2='b'.
    # So forced[1]='b' (from T) but required at i=1 pos1 = 'a'. That is mismatch => satisfied. Not impossible.
    # Need forced[1]='a' to match required, but forced[1] is 'b' due to T, so mismatch.
    # To have forced[1] match required, we need T that forces 1='a'. That would be a T at i=1 that forces 1='a',2='b'.
    # Then str1 = "TT"? But we already saw conflict.
    # So maybe unsatisfiable cases are only due to conflicting T's.
    # Let's just test a case where algorithm returns empty due to no free position.
    # Example: n=2,m=3, str1="FTF", str2="abc"
    # i=0 F covers 0,1,2. No forced -> max_free=2, need='c', schedule.
    # i=2 F covers 2,3,4. forced[2] is None (free), max_free=4, need='b', schedule.
    # Both have free positions.
    # Let's force positions to make no free position for some F.
    # Consider n=3,m=2, str1="TFF", str2="ab"
    # T at i=0 forces 0='a',1='b'
    # F at i=1 covers 1,2: forced[1]='b' matches required 'a'? No mismatch => satisfied
    # F at i=2 covers 2,3: both free -> schedule.
    # Not impossible.
    # Let's create n=2,m=2, str1="TT", str2="ab" (already unsatisfiable).
    # Also case where forced positions fill entire interval and match required.
    # Example: n=2,m=2, str1="TF", str2="ab"
    # T at i=0 forces 0='a',1='b'
    # F at i=1 covers 1,2. forced[1]='b' != required 'a' => satisfied. So not impossible.
    # Need forced[1] = required at i=1 = 'a', but T forces 'b'. So impossible? Actually that would be a conflict between T and F? No, it's not a conflict; the F interval would be satisfied because forced mismatch exists. So it's not impossible.
    # The only way an F interval can be impossible is if all its positions are forced and equal to required, and there is no free position to break it. That requires that the interval's positions are forced by T's to exactly match str2. So we need two overlapping T's that force the same substring but offset such that the second T's forced characters align with the first T's forced characters.
    # Example: n=3,m=2, str1="TTF", str2="ab"
    # i=0 T forces 0='a',1='b'
    # i=1 T forces 1='a',2='b' (conflict at 1) => returns empty.
    # So conflict detection catches this.
    # Another case: n=3,m=2, str1="TFT", str2="ab"
    # i=0 T forces 0='a',1='b'
    # i=2 T forces 2='a',3='b'
    # i=1 F covers 1,2. forced[1]='b' != required 'a' => satisfied.
    # So not impossible.
    # The algorithm's detection of impossible due to no free position seems to be triggered when an interval has no free positions and is not satisfied by forced mismatch. Let's construct such a case.
    # We need an interval [i, i+m-1] where every position pos has forced[pos] not None and forced[pos] == str2[pos-i]. And there is no forced mismatch.
    # This can happen if we have T's that force those positions accordingly, but they don't conflict.
    # Example: n=2,m=2, str1="TT", str2="ab"
    # i=0 T forces 0='a',1='b'
    # i=1 T forces 1='a',2='b' (conflict at 1) => already empty.
    # Need non-conflicting T's that together cover the interval fully.
    # Consider n=3,m=2, str1="TTT", str2="ab"
    # i=0 forces 0='a',1='b'
    # i=1 forces 1='a',2='b' (conflict) => empty.
    # So conflict.
    # Need to have T's that are offset such that they don't conflict but cover interval.
    # Example: n=3,m=2, str1="T?T"? Actually we need two T's at i=0 and i=2. i=0 forces 0='a',1='b'; i=2 forces 2='a',3='b'. That doesn't conflict.
    # Then F at i=1 covers positions 1,2. forced[1]='b' matches required 'a'? Actually required at i=1 pos1 = 'a', forced is 'b' => mismatch => satisfied. So not impossible.
    # To have forced[pos] == required for all positions in interval, we need forced[pos] = str2[pos-i] for all pos in [i,i+m-1].
    # Let's try n=3,m=3, str1="TTT", str2="abc"
    # i=0 forces 0='a',1='b',2='c'
    # i=1 forces 1='a',2='b',3='c' (conflict at 1,2) => empty.
    # So conflict.
    # Let's try n=3,m=3, str1="TFT", str2="abc"
    # i=0 forces 0='a',1='b',2='c'
    # i=2 forces 2='a',3='b',4='c' (conflict at 2) => empty.
    # So conflict.
    # It seems any overlapping T's that force a full interval without conflict will cause a conflict detection. Actually, if two T's overlap, they force overlapping positions to the same letters (must be same) else conflict. So they can be consistent if str2 is periodic with period equal to offset. For example, str2 = "aaaa", m=4, and T at i=0 forces positions 0-3 all 'a', T at i=1 forces positions 1-4 all 'a'. They are consistent (no conflict). Then F at i=0? Not needed.
    # Let's test: n=2,m=4, str1="TT", str2="aaaa"
    # i=0 forces 0='a',1='a',2='a',3='a'
    # i=1 forces 1='a',2='a',3='a',4='a' (consistent)
    # Now F interval at i=0? Not present. Actually we want an F interval that is fully forced and matches. Let's add F at i=0? But i=0 is T. Let's add F at i=2? n=3? Let's think.
    # We need an F interval where all positions are forced and match required. That can happen if we have a pattern of T's that cover the interval and str2 is constant.
    # Example: n=3,m=2, str1="TTF", str2="aa"
    # i=0 T forces 0='a',1='a'
    # i=1 T forces 1='a',2='a' (consistent)
    # i=2 F covers positions 2,3. forced[2]='a' matches required 'a' (since str2[0]='a'), forced[3] is free? Actually forced[3] is None (no T covering 3). So there is a free position.
    # Not impossible.
    # To have no free position, the interval must be fully covered by T's and match. So we need T's covering the interval without gaps. For interval length m, we need T's at positions such that they cover all positions. With overlapping T's, we can cover a stretch.
    # Example: n=3,m=2, str1="TTT", str2="aa"
    # i=0 forces 0,1 = 'a','a'
    # i=1 forces 1,2 = 'a','a'
    # i=2 forces 2,3 = 'a','a'
    # So positions 0,1,2,3 all forced to 'a'. Now if we have an F interval at i=2 (covers 2,3), both positions forced and match required => no free position, not satisfied => impossible.
    # Let's test: str1="TTTF", str2="aa"
    # n=4,m=2. i=0,1,2 are T, i=3 is F. Interval at i=3 covers positions 3,4. forced[3]='a', forced[4] is None? Actually T at i=2 forces 2,3. So forced[3]='a'. Position 4 is not forced (since T at i=2 only covers 2 and 3). So free position 4 exists. So not impossible.
    # To have no free position for F at i=3, we need T at i=3 as well? Actually we need T at i=2 to cover position 4? T at i=2 covers positions 2 and 3 only (m=2). To cover position 4, we need T at i=3. But i=3 is F. So cannot.
    # Let's try n=4,m=2, str1="TTTT", str2="aa". All T's. No F intervals, so not relevant.
    # Let's add an F at i=1: str1="TFTF", str2="aa". Let's see: i=0 T forces 0,1='a','a'; i=1 F covers 1,2. forced[1]='a' matches required 'a' (since str2[0]='a'), forced[2] is None (free). So not impossible.
    # To make forced[2] also forced, need T at i=2? Actually i=2 is T in original pattern? str1="TFTF", i=2 is T. Yes. So forced[2]='a'. Then interval at i=1 covers 1,2: forced[1]='a', forced[2]='a' both match required 'a','a'? Actually required at i=1: positions 1='a',2='a'. Both match. So no free position, interval not satisfied, algorithm should detect max_free==-1 and return empty.
    # Let's test that: str1="TFTF", str2="aa". n=4,m=2,N=5.
    # T at i=0 forces forced[0]='a', forced[1]='a'.
    # T at i=2 forces forced[2]='a', forced[3]='a'.
    # F at i=1 covers positions 1,2. forced[1]='a' matches required 'a' (str2[0]), forced[2]='a' matches required 'a' (str2[1]). No forced mismatch. max_free remains -1 (no free positions). So algorithm returns empty.
    # Indeed there is no solution: The word must have positions 0='a',1='a',2='a',3='a', position 4 free. Interval i=1 requires word[1..2] != "aa", but both are 'a', so cannot. So impossible.
    # Good. This case will be caught.
    # So test this case.
    sol = Solution().generateString("TFTF", "aa")
    assert sol == "", f"Expected empty for TFTF/aa, got {sol}"
    print("Unsatisfiable case tests passed.")

def test_performance():
    """Large random test to ensure performance is acceptable."""
    import time
    random.seed(123)
    n = 10000
    m = 500
    str1 = ''.join(random.choice('TF') for _ in range(n))
    # generate str2 with random letters
    str2 = ''.join(random.choice(string.ascii_lowercase) for _ in range(m))
    start = time.time()
    sol = Solution().generateString(str1, str2)
    elapsed = time.time() - start
    print(f"Performance test: n={n}, m={m}, time={elapsed:.3f}s, result length={len(sol)}")
    # Validate solution if not empty
    if sol:
        assert is_feasible(sol, str1, str2), "Algorithm produced infeasible solution in performance test"
        # Also check that it's lexicographically minimal? Hard to verify, but at least feasible.

if __name__ == "__main__":
    # Run unsatisfiable handcrafted tests
    test_unsatisfiable_cases()
    # Run random small tests comparing with brute force (limited alphabet)
    test_random_small()
    # Run performance test
    test_performance()