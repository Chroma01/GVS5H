class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1

        # Step 1: Initialize answer array with None (unassigned)
        ans = [None] * L

        # Step 2: Apply all 'T' constraints
        for i, ch in enumerate(str1):
            if ch == 'T':
                for k in range(m):
                    pos = i + k
                    if ans[pos] is not None:
                        if ans[pos] != str2[k]:
                            return ""
                    else:
                        ans[pos] = str2[k]

        # Step 3: Analyze 'F' constraints
        # forbidden[p] will hold a set of letters that are forbidden at position p
        forbidden = [set() for _ in range(L)]

        for i, ch in enumerate(str1):
            if ch == 'F':
                # Count None positions in window [i, i+m-1]
                none_positions = []
                for k in range(m):
                    pos = i + k
                    if ans[pos] is None:
                        none_positions.append((pos, k))

                if len(none_positions) == 0:
                    # Window is fully determined, check it is not equal to str2
                    window = ans[i:i+m]
                    if window == list(str2):
                        return ""
                elif len(none_positions) == 1:
                    # Exactly one free position; mark the corresponding str2 letter as forbidden
                    pos, k = none_positions[0]
                    forbidden[pos].add(str2[k])
                # If >=2, no immediate restriction from this F

        # Step 4: Assign the smallest allowed letter to each None position
        for p in range(L):
            if ans[p] is None:
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    if c not in forbidden[p]:
                        ans[p] = c
                        break
                else:
                    # All 26 letters forbidden → impossible
                    return ""

        # Step 5: Final verification that no F window equals str2
        for i, ch in enumerate(str1):
            if ch == 'F':
                window = ans[i:i+m]
                if window == list(str2):
                    return ""

        return "".join(ans)


# ---------------- Comprehensive test suite ----------------
def run_tests():
    sol = Solution()
    test_cases = [
        # Provided examples
        ("TFTF", "ab", "ababa"),
        ("TFTF", "abc", ""),
        ("F", "d", "a"),
        # Additional edge cases
        # All T, single character str2
        ("TTT", "a", "aaa"),
        # All F, single character str2 - we can fill all with 'a' except need to avoid window "a" everywhere.
        # For n=3, m=1, L=3. Each F window is a single char. We need no window == "a".
        # Smallest string is "bbb" (all positions can be 'a' except then window equals "a").
        # Wait: each position is its own window. If we set any position to 'a', its F window would be 'a' which is forbidden.
        # So we must fill all with 'b'. Lexicographically smallest is "bbb".
        ("FFF", "a", "bbb"),
        # All F, str2 length > 1, m=2
        # L = n + m - 1. For n=2, m=2, L=3. Windows: [0:2] and [1:3]. Need both != "ab".
        # No T constraints. We can try smallest string "aaa". Window1="aa"!="ab", Window2="aa"!="ab" → valid.
        ("FF", "ab", "aaa"),
        # Overlapping T conflict: str1="TT", str2="ab" and "ba" -> different str2 but problem has single str2.
        # Overlap conflict: T at 0 forces "ab", T at 1 forces "ab" (str2="ab") → ans[0]=a, ans[1]=b, ans[2]=b.
        # No conflict. Let's make a conflict: str1="TT", str2="ab" and str2 "ba"? Not possible with single str2.
        # Conflict arises when overlapping T windows force different letters on same position.
        # Example: str1="TT", str2="ab". T at 0 → word[0..1]="ab". T at 1 → word[1..2]="ab".
        # Position 1 is forced to 'b' by first and 'a' by second → conflict.
        ("TT", "ab", ""),
        # m=1, mix of T and F
        # str1="TF", str2="a". T forces word[0]='a'. F at index 1: window word[1] != 'a'. Smallest is 'a' for position 1? No, 'a' forbidden, so 'b'.
        # L=2. word="ab". Check: T window word[0]='a' OK. F window word[1]='b' != 'a' OK.
        ("TF", "a", "ab"),
        # n=1, m=1, T
        ("T", "z", "z"),
        # n=1, m=1, F
        ("F", "z", "a"),
        # Larger overlapping, lexicographic check
        # str1="TFTFTF", str2="ab". L=6+2-1=7? n=6, m=2, L=7.
        # T at 0: [0..1]="ab" → ans[0]='a', ans[1]='b'
        # F at 1: window [1..2]. ans[1]='b' (fixed), ans[2]=None. none_count=1, k=1, forbidden at pos 2: str2[1]='b'.
        # T at 2: [2..3]="ab" → ans[2]='a', ans[3]='b'. (Note: pos 2 was None, now set to 'a', which is allowed because 'b' was forbidden.)
        # F at 3: window [3..4]. ans[3]='b', ans[4]=None. none_count=1, k=1, forbidden at pos 4: 'b'.
        # T at 4: [4..5]="ab" → ans[4]='a', ans[5]='b'.
        # F at 5: window [5..6]. ans[5]='b', ans[6]=None. none_count=1, k=1, forbidden at pos 6: 'b'.
        # All assigned: "abababa". Check F windows:
        #   F1: word[1..2]="ba" != "ab" OK.
        #   F3: word[3..4]="ba" != "ab" OK.
        #   F5: word[5..6]="ba" != "ab" OK.
        # Lexicographically smallest? All positions forced, so "abababa".
        ("TFTFTF", "ab", "abababa"),
        # Case where forbidden set causes impossibility for a free position
        # str1="F", str2="ab" → L=1+2-1=2. No T. F window [0..1] != "ab". None_count=2, no restriction.
        # Smallest string: "aa" (since 'a' is not forbidden). Check: window "aa" != "ab" OK. So "aa".
        ("F", "ab", "aa"),
        # str1="FFF", str2="a" → L=3. All windows of length 1 must not be 'a'. So all positions must not be 'a'. Smallest is "bbb".
        ("FFF", "a", "bbb"),
        # Larger m, no conflict
        # str1="T", str2="abc" → word="abc"
        ("T", "abc", "abc"),
        # str1="F", str2="abc" → L=3. No T. F window [0..2] != "abc". None_count=3. Smallest "aaa". Check: "aaa" != "abc" OK.
        ("F", "abc", "aaa"),
        # Complex: some T force positions, F windows have one free position that must avoid str2 char
        # str1="TFF", str2="ab". T at 0: [0..1]="ab". F at 1: [1..2]. ans[1]='b', ans[2]=None. none=1, k=1, forbid 'b' at pos 2.
        # F at 2: [2..3]. ans[2]=None, ans[3]=None. none=2, no restriction.
        # Positions: ans[0]='a', ans[1]='b', ans[2]=None (forbid {'b'}), ans[3]=None.
        # Assign pos 2: smallest not 'b' is 'a'. Assign pos 3: 'a'.
        # Result: "abaa". Check F windows:
        #   F1: word[1..2]="ba" != "ab" OK.
        #   F2: word[2..3]="aa" != "ab" OK.
        # Lexicographically smallest? Could we have used 'a' at pos 2? Yes, 'a' is allowed. So "abaa".
        ("TFF", "ab", "abaa"),
        # Similar but str2 contains 'a' so forbid at pos 2 would be 'a'? Let's see:
        # str1="TFF", str2="aa". T at 0: [0..1]="aa". F at 1: [1..2]. ans[1]='a', ans[2]=None. none=1, k=1, forbid 'a' at pos 2.
        # F at 2: [2..3]. none=2, no restriction.
        # pos 2: forbid {'a'}, pick 'b'. pos 3: 'a' (smallest).
        # Result: "aaba". Check:
        #   F1: word[1..2]="ab" != "aa" OK.
        #   F2: word[2..3]="ba" != "aa" OK.
        # Could we have picked 'a' at pos 2? No, forbidden. So "aaba" is lexicographically smallest.
        ("TFF", "aa", "aaba"),
        # Impossible because all letters forbidden for a position
        # str1="F", str2="a". m=1, L=1. F window [0..0] != "a". none=1, k=0, forbid 'a' at pos 0.
        # pos 0: all letters? Only 'a' forbidden, can pick 'b'..'z'. Smallest 'b'. Result "b".
        # Not impossible. To make impossible, need forbid all 26 letters. That requires many F windows each with exactly one free position and the str2 character covers all 26? No, str2 is fixed, so at most one forbidden letter per position.
        # To forbid all 26 letters, we need a single position that is the only free position in 26 different F windows, each forcing a different letter? But str2 is fixed, so each F window forbids the same letter at that position (the letter at offset k within str2). So at most one letter forbidden per position.
        # So a position can never have all 26 letters forbidden by this logic alone. The only impossibility is conflict in T or F window already equal to str2.
        # However, we can have a position that is forced by T but also the F windows... actually if T forces it, it won't be None.
        # So the only way a position is None and all 26 letters are forbidden is impossible under this construction, but the problem might have such cases?
        # Actually, if a position is the only free position in many F windows, each F window forbids str2[k] for that position. Since str2 is the same string, all those F windows would forbid the same letter (because offset k is determined by which F window). So only one letter forbidden.
        # Thus the greedy will never fail in step 4 unless there's a bug. But we keep the check.
        # Another impossible case: F window fully determined equals str2. Already handled.
        # So let's test a case where F window is fully determined and equals str2:
        # str1="T", str2="ab". T at 0 forces [0..1]="ab". No F. Result "ab".
        # str1="TF", str2="ab". T at 0: [0..1]="ab". F at 1: [1..2]. ans[1]='b', ans[2]=None. none=1, forbid 'b' at pos 2. pos 2: 'a'. Result "aba". Check F: "ba"!="ab" OK.
        # To make F fully determined and equal to str2: need T windows to set the window exactly to str2, and that index is F.
        # str1="TF", str2="ab". T at 0 sets [0..1]="ab". F at 1: window [1..2] is partially None unless forced. Not fully determined.
        # Make str1="TT", str2="ab". T0: [0..1]="ab". T1: [1..2]="ab". Conflict at pos 1 → "".
        # Make str1="FT", str2="ab". F0: [0..1] != "ab". T1: [1..2]="ab". So pos1='b', pos2='b'. F0: window [0..1] has pos0=None, pos1='b'. none=1, forbid 'a' at pos0. pos0: 'a'? No, 'a' forbidden, so 'b'? But then window "bb" != "ab" OK. So "bbb". Check: T1 window [1..2]="bb"!="ab"! Wait, T1 requires word[1..2]==str2="ab". But we have pos1='b', pos2='b' → "bb" != "ab". So conflict: T1 forces pos1='b' and pos2='b'? No, T1 at index 1 means window starting at 1: word[1..2] == str2 => word[1]='a', word[2]='b'. But F0 didn't set pos1. Let's re-evaluate:
        # str1="FT", str2="ab".
        # T at index 1: pos1 = 1+0=1 → 'a'; pos2 = 1+1=2 → 'b'. So ans[1]='a', ans[2]='b'.
        # F at index 0: window [0..1]. ans[0]=None, ans[1]='a'. none=1, k=1, forbid str2[1]='b' at pos0. So pos0: 'a' (smallest not 'b').
        # Result: "aab". Check: T window [1..2]="ab" OK. F window [0..1]="aa" != "ab" OK.
        ("FT", "ab", "aab"),
        # Case where F window is fully determined and equals str2 → impossible
        # Need an F window whose all positions are forced by T to exactly str2.
        # str1="TT", str2="ab". T0 forces [0..1]="ab". T1 forces [1..2]="ab". Conflict at pos1.
        # str1="TTT", str2="ab". T0: [0..1]="ab". T1: [1..2]="ab". T2: [2..3]="ab". So ans = "abab". No F.
        # Add F somewhere: str1="TFT", str2="ab". T0: [0..1]="ab". F1: window [1..2]. T2: [2..3]="ab". So ans[0]='a', ans[1]='b', ans[2]='a', ans[3]='b'. F1 window [1..2]="ba" != "ab" OK.
        # To make F window equal to str2, we need the T constraints to set it exactly. For example, str1="TF", str2="ab". T0 sets [0..1]="ab". F1 window [1..2] is not fully determined (pos2=None). Not fully.
        # What if we have two T that set the window? str1="TTF", str2="ab". T0: [0..1]="ab". T1: [1..2]="ab". Conflict.
        # str1="TFT", str2="aba"? m=3. T0: [0..2]="aba". F1: [1..3]. T2: [2..4]="aba". So ans[0]='a', ans[1]='b', ans[2]='a', ans[3]=None, ans[4]='a'. F1 window [1..3]: ans[1]='b', ans[2]='a', ans[3]=None. none=1, k=2, forbid str2[2]='a' at pos3. pos3: 'b'. Result "ababa". Check: F1 window [1..3]="bab" != "aba" OK.
        # To make F window fully determined and equal, need T constraints to cover all its positions. For example, str1="TFT", str2="ab". T0: [0..1]="ab". F1: [1..2]. T2: [2..3]="ab". So ans[0]='a', ans[1]='b', ans[2]='a', ans[3]='b'. F1 window [1..2]="ba" != "ab" OK.
        # Try to make F window exactly str2: need word[i..i+m-1] == str2 for some i with str1[i]='F'. That means all those positions are forced to match str2. But if they are forced by T, that's fine. The issue is if they are forced by other T windows and happen to equal str2, then we have a conflict because the F requires it to be not equal. So:
        # str1="TFT", str2="ab". T0: [0..1]="ab". T2: [2..3]="ab". Then window [1..2] is not fully determined (pos1='b', pos2='a' from T0 and T2? Wait, T2 sets pos2='a', pos3='b'. T0 sets pos0='a', pos1='b'. So ans[1]='b', ans[2]='a'. So window [1..2]="ba" != "ab". OK.
        # To make it "ab", we need ans[1]='a' and ans[2]='b'. But T0 forces ans[1]='b', T2 forces ans[2]='a'. Conflict. So cannot happen.
        # Another: str1="FTT", str2="ab". F0: [0..1]. T1: [1..2]="ab". T2: [2..3]="ab". So ans[1]='a', ans[2]='b', ans[3]='b'. F0 window [0..1]: ans[0]=None, ans[1]='a'. none=1, k=1, forbid 'b' at pos0. pos0: 'a'. Result "aabb". Check: F0 "aa" != "ab" OK.
        # To make F0 equal "ab", we need ans[0]='a', ans[1]='b'. But T1 forces ans[1]='a'. Conflict.
        # So a fully determined F window equaling str2 would require conflicting T constraints, which we already catch. But what if no T, but F window is fully determined by... nothing? Impossible.
        # Actually, the only way an F window is fully determined is if T constraints cover all its positions. If they cover all positions and the result is str2, then there is a T index that forces that window? Not necessarily, but the positions are forced. If the forced values equal str2, then the F window equals str2, which violates the F condition. So we return "".
        # Example: str1="FTF", str2="ab". F0: [0..1]. T1: [1..2]="ab". F2: [2..3]. So ans[1]='a', ans[2]='b'. F0 window [0..1]: ans[0]=None, ans[1]='a'. none=1, forbid 'b' at pos0. F2 window [2..3]: ans[2]='b', ans[3]=None. none=1, forbid 'a' at pos3. pos0: 'a', pos3: 'b'. Result "aabb". Check F0: "aa" != "ab" OK. F2: "bb" != "ab" OK.
        # Let's construct a case where T forces a window to exactly str2, and that window is an F index.
        # str1="TFTF", str2="ab". T0: [0..1]="ab". F1: [1..2]. T2: [2..3]="ab". F3: [3..4]. So ans[0]='a', ans[1]='b', ans[2]='a', ans[3]='b'. F1 window [1..2]="ba" != "ab". F3 window [3..4]="b?" with pos4=None. none=1, forbid 'a' at pos4. pos4='b'. Result "ababb". Check: F3 "bb" != "ab" OK.
        # Not fully determined.
        # To get fully determined F, need T indices that cover the F window without gaps. For F at index i, we need T at i, i+1, ..., i+m-1? No, T at j covers positions j..j+m-1. To cover window i..i+m-1, we need T at i (covers i..i+m-1) or combination. Actually T at i covers the whole window. So if str1[i]='T' and str1[i]='F', conflict. So F window cannot be covered by a single T at same index. But can be covered by multiple T that overlap. For example, T at i and T at i+1 cover i..i+m. But we need exactly i..i+m-1. T at i covers i..i+m-1. So if we have T at i, it covers the F window at i entirely. But then str1[i] is both T and F, impossible. So an F window can only be fully determined by T's that start at indices other than i. For example, T at i-1 covers i-1..i+m-2. Not enough. T at i+1 covers i+1..i+m. Too far. So an F window at i can be fully determined only if there are T's that cover all its positions. Since each T covers m consecutive positions, to cover i..i+m-1 without a T at i, we need T's starting at i-1, i-2, etc. But i-1 covers up to i+m-2. To cover i+m-1, need T at i+m-1? That covers i+m-1..i+2m-2, which includes i+m-1 but also others. But we only care about the window i..i+m-1. Actually, we can have T at i+1 covering i+1..i+m, which includes i+1..i+m-1, and T at i covering i..i, but we don't have T at i. So we can cover the window with T at i+1, i+2, ..., i+m-1? Each T at j covers j..j+m-1. The union of windows starting at i+1, i+2, ..., i+m-1 covers (i+1)..(i+2m-2). The intersection of all these windows is (i+m-1)..(i+m-1) (the last position). So to cover the whole window i..i+m-1, we need T at i-1, i-2, ..., i-m+1? That would be many. But in any case, if the positions are forced to match str2, then the F window equals str2, which is forbidden. But can it be forced to match str2 without conflict? Yes, if the forced values are exactly str2. For example, str1="TT", str2="ab". T0: [0..1]="ab". T1: [1..2]="ab". Conflict at pos1. So no.
        # Another: str1="TTT", str2="ab". T0, T1, T2. L=4. ans: pos0='a', pos1='b' (from T0), pos1='a' (from T1) -> conflict. So T0 and T1 conflict.
        # What if str2 has same char? str2="aa". T0: [0..1]="aa". T1: [1..2]="aa". No conflict: ans[0]='a', ans[1]='a', ans[2]='a'. So ans="aaa". Now if we have F at index 0? str1="FT", str2="aa". F0: [0..1]. T1: [1..2]="aa". So ans[1]='a', ans[2]='a'. F0 window [0..1]: ans[0]=None, ans[1]='a'. none=1, forbid 'a' at pos0. So pos0 must not be 'a'. Smallest is 'b'. Result "baa". Check: F0 "ba" != "aa" OK.
        # To make F0 fully determined and equal to "aa", we need ans[0]='a', ans[1]='a'. But T1 forces ans[1]='a'. If we also have T0? Then str1[0]='T' and 'F', impossible.
        # So it seems impossible to have a fully determined F window equaling str2 without conflict, but we should still check.
        # Let's try: str1="TFT", str2="aa". T0: [0..1]="aa". F1: [1..2]. T2: [2..3]="aa". So ans[0]='a', ans[1]='a', ans[2]='a', ans[3]='a'. F1 window [1..2]="aa" which equals str2! So this should be impossible.
        # Let's test this case:
        ("TFT", "aa", ""),
        # Indeed: T0 forces "aa", T2 forces "aa", so window [1..2] is "aa", which is an F window (index 1). So return "".
    ]

    all_passed = True
    for idx, (s1, s2, expected) in enumerate(test_cases, 1):
        result = sol.generateString(s1, s2)
        status = "PASS" if result == expected else "FAIL"
        if result != expected:
            all_passed = False
        print(f"Test {idx}: str1={s1!r}, str2={s2!r} -> got {result!r}, expected {expected!r} [{status}]")

    print("\nAll tests passed!" if all_passed else "\nSome tests failed.")


if __name__ == "__main__":
    run_tests()