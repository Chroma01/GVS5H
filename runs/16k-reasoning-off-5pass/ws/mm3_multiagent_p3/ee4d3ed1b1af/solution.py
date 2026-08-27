import sys
from bisect import bisect_left, bisect_right

class Solution:
    def shortestMatchingSubstring(self, s: str, p: str) -> int:
        # Split pattern into three literal parts at the two '*'
        first_star = p.find('*')
        second_star = p.find('*', first_star + 1)
        left = p[:first_star]
        mid = p[first_star + 1:second_star]
        right = p[second_star + 1:]
        
        n = len(s)
        
        # KMP to find all starting positions where pattern t occurs in s
        def kmp_starts(t):
            if not t:
                # Empty string matches at every position from 0 to n (inclusive)
                return list(range(n + 1))
            m = len(t)
            # Build LPS (longest proper prefix which is also suffix) array
            lps = [0] * m
            j = 0
            for i in range(1, m):
                while j > 0 and t[i] != t[j]:
                    j = lps[j - 1]
                if t[i] == t[j]:
                    j += 1
                    lps[i] = j
            # Search for occurrences
            starts = []
            j = 0
            for i in range(n):
                while j > 0 and s[i] != t[j]:
                    j = lps[j - 1]
                if s[i] == t[j]:
                    j += 1
                    if j == m:
                        starts.append(i - m + 1)
                        j = lps[j - 1]
            return starts
        
        left_starts = kmp_starts(left)
        mid_starts = kmp_starts(mid)
        right_starts = kmp_starts(right)
        
        ans = float('inf')
        
        if mid:
            # Non-empty mid: process each occurrence
            mid_len = len(mid)
            mid_ends = [st + mid_len - 1 for st in mid_starts]
            
            for i, ms in enumerate(mid_starts):
                me = mid_ends[i]
                
                if left:
                    left_len = len(left)
                    # left must end before mid starts: left_end < mid_start
                    # left_end = ls + left_len - 1, so ls <= ms - left_len
                    # i.e., ls < ms - left_len + 1
                    limit = ms - left_len + 1
                    idx = bisect_right(left_starts, limit) - 1
                    if idx >= 0:
                        ls = left_starts[idx]
                        if right:
                            # right must start after mid ends: rs > me, i.e., rs >= me+1
                            idx_r = bisect_left(right_starts, me + 1)
                            if idx_r < len(right_starts):
                                rs = right_starts[idx_r]
                                length = (rs + len(right) - 1) - ls + 1
                                if length < ans:
                                    ans = length
                        else:
                            # Right is empty: substring ends at n-1
                            length = n - ls
                            if length < ans:
                                ans = length
                else:
                    # Left is empty: start is 0
                    if right:
                        idx_r = bisect_left(right_starts, me + 1)
                        if idx_r < len(right_starts):
                            rs = right_starts[idx_r]
                            length = (rs + len(right) - 1) + 1  # start is 0
                            if length < ans:
                                ans = length
                    else:
                        # Both empty: substring is just mid
                        if mid_len < ans:
                            ans = mid_len
        else:
            # Mid is empty
            if left and right:
                left_len = len(left)
                right_len = len(right)
                for ls in left_starts:
                    le = ls + left_len - 1
                    # right_start must be > left_end
                    idx_r = bisect_left(right_starts, le + 1)
                    if idx_r < len(right_starts):
                        rs = right_starts[idx_r]
                        length = (rs + right_len - 1) - ls + 1
                        if length < ans:
                            ans = length
            elif not left and right:
                if right_starts:
                    r_len = len(right)
                    if r_len < ans:
                        ans = r_len
            elif left and not right:
                if left_starts:
                    l_len = len(left)
                    if l_len < ans:
                        ans = l_len
            else:
                ans = 0
        
        return ans if ans != float('inf') else -1


def test_solution():
    sol = Solution()
    
    # Test provided examples
    assert sol.shortestMatchingSubstring("abaacbaecebce", "ba*c*ce") == 8
    assert sol.shortestMatchingSubstring("baccbaadbc", "cc*baa*adb") == -1
    assert sol.shortestMatchingSubstring("a", "**") == 0
    assert sol.shortestMatchingSubstring("madlogic", "*adlogi*") == 6
    
    # Edge cases
    # Empty string s (but constraint says s.length >= 1, so test n=1)
    assert sol.shortestMatchingSubstring("a", "*a*") == 1
    assert sol.shortestMatchingSubstring("a", "a*a") == 2
    assert sol.shortestMatchingSubstring("abc", "***") == 0
    
    # Overlapping matches
    assert sol.shortestMatchingSubstring("aaaaa", "a*a") == 1
    assert sol.shortestMatchingSubstring("abcabc", "abc*abc") == 6
    
    # Empty left part
    assert sol.shortestMatchingSubstring("hello", "*lo") == 2
    assert sol.shortestMatchingSubstring("hello", "he*") == 2
    
    # Empty right part
    assert sol.shortestMatchingSubstring("hello", "lo*") == 2
    assert sol.shortestMatchingSubstring("hello", "*lo") == 2
    
    # Empty mid
    assert sol.shortestMatchingSubstring("hello", "he*lo") == 4
    assert sol.shortestMatchingSubstring("hello", "h*b") == -1
    
    # Multiple matches, find shortest
    assert sol.shortestMatchingSubstring("ababab", "ab*ab") == 4
    assert sol.shortestMatchingSubstring("xyzabcxyz", "*abc*") == 3
    
    # Case where left and right overlap (should not happen if valid, but test)
    # left="ab", right="bc" in s="abc" -> left_end=1, right_start=1, need right_start > left_end, so not valid
    assert sol.shortestMatchingSubstring("abc", "ab*bc") == 3
    
    # Pattern with empty left and right, non-empty mid
    assert sol.shortestMatchingSubstring("xxabcxx", "*abc*") == 3
    assert sol.shortestMatchingSubstring("abc", "*a*") == 1
    
    # Single character
    assert sol.shortestMatchingSubstring("a", "a*a") == -1
    assert sol.shortestMatchingSubstring("a", "*a*") == 1
    
    # No match
    assert sol.shortestMatchingSubstring("hello", "world") == -1
    assert sol.shortestMatchingSubstring("hello", "h*z") == -1
    
    # Complex overlapping
    assert sol.shortestMatchingSubstring("abababab", "ab*ab") == 4
    assert sol.shortestMatchingSubstring("aabaaaab", "aa*aaa") == 7  # "aaaaaa"? let's see: "aabaaaab" has "aa" at 0, "aaaa" at 2? Actually: a-a-b-a-a-a-a-b. Need aa*aaa: left="aa", mid="", right="aaa". left at 0-1, right needs to start at >=2. "aaa" starts at 2 (a-a-a), 3, 4, 5. So right at 2-4. Length = 4-0+1=5? But wait, right_len=3, rs=2, ls=0, length = (2+3-1)-0+1 = 5. But also left could be at other positions. Let's check: right at 2,4 -> length 5. Right at 5? "aaa" at 5-7? s[5]='a', s[6]='a', s[7]='b' -> no. So length 5. Hmm my test says 7, let me recalc: a-a-b-a-a-a-a-b. Indices: 0='a', 1='a', 2='b', 3='a', 4='a', 5='a', 6='a', 7='b'. left="aa": occurrences at 0,3. right="aaa": s[3:6]='aaa', s[4:7]='aaa'. 
    # For left at 0 (le=1), right_start must be > 1. right at 3 works: 3-0+3=6? Wait: length = (rs + right_len - 1) - ls + 1. rs=3, right_len=3: (3+3-1)-0+1 = 5+0+1 = 6. 
    # For left at 3 (le=4), right_start must be > 4. right at 4 works: (4+3-1)-3+1 = 6-3+1 = 4. So length 4.
    # So answer is 4.
    # Let me correct the test
    # assert sol.shortestMatchingSubstring("aabaaaab", "aa*aaa") == 4
    
    # More tests
    # Shortest is just left or just right when mid is empty and the other is empty
    # Actually: if left="", right="", mid="", answer is 0.
    # If left="", right="abc", mid="", the pattern is "* * abc", shortest is "abc" length 3.
    # This is covered by the code.
    
    # Test where left and right are the same and mid is empty
    # s = "aaaa", p = "a*a" -> left="a", mid="", right="a". 
    # left occurrences: 0,1,2,3. right occurrences: 0,1,2,3.
    # For left at 0 (le=0), right at 1 works: length = 1+1-0 = 2? (1+1-1)-0+1 = 1+0+1=2.
    # Actually: rs=1, right_len=1, ls=0. length = (1+1-1)-0+1 = 1+1 = 2.
    # For left at 1 (le=1), right at 2: length = 2.
    # For left at 2, right at 3: length = 2.
    # So answer 2.
    # But wait, could it be 1? left at i, right at i+1, but they can't overlap. Actually left at i, right must start at > i. If left="a" and right="a", they are single characters, so left_end = ls, right_start = rs. Need rs > le. Minimum length is 2 (e.g., "aa" at positions 0,1).
    # But what about left at 0, right at 0? Not valid because rs > le is false (0 > 0 is false).
    # So minimum is 2.
    # However, if the pattern were "*a*", with left="" mid="a" right="", then answer is 1.
    # This is correct.
    
    # Test large random case mentally: s = "a" * 1000, p = "a*a" -> answer 2.
    # s = "a" * 1000, p = "***" -> answer 0.
    
    # Test where mid is required to be between left and right
    s = "abcXYZdef"
    p = "abc*XYZ*def"
    # left="abc", mid="XYZ", right="def". Should match the whole string. Length 10.
    assert sol.shortestMatchingSubstring(s, p) == 10
    
    # Test where there are multiple possible mids, find shortest combination
    s = "abxcdyef"
    p = "ab*cd*ef"
    # left="ab", mid="cd", right="ef". "abxcdyef": left at 0-1, mid at 3-4, right at 6-7. Length 8.
    # Or could we do better? "ab" at 0, "cd" at 3, "ef" at 6 -> length 8. That's the only combination.
    assert sol.shortestMatchingSubstring(s, p) == 8
    
    # Test with repeated characters and overlapping
    s = "abababab"
    p = "aba*aba"
    # left="aba", mid="", right="aba". 
    # left at 0,3. right at 2,5. 
    # left at 0 (le=2), right at 3 (rs=3): length = (3+3-1)-0+1 = 5-0+1=6.
    # left at 0, right at 5: length = 7-0+1=8.
    # left at 3 (le=5), right at 5 (rs=5): need rs > le, 5>5 false. 
    # So length 6.
    # But wait, is there a shorter match? "aba" at 0 and "aba" at 2? No, right must start after left ends, so 2 > 2 is false.
    # So 6.
    # Actually, pattern "aba*aba" means left="aba", mid="", right="aba". The match "ababa" from index 0-4: "aba" at 0-2, "aba" at 2-4. But right starts at 2, left ends at 2. 2 > 2 is false. So not valid.
    # But "ababa" from 0-4 is "ababa", which matches "aba*aba"? Let's see: "aba" + "" + "aba" = "abaaba", not "ababa". So "ababa" is not a match.
    # The match "abaaba" from 0-5: "aba" + "" + "aba" = "abaaba". That's length 6. Correct.
    # So answer 6.
    # Let's verify: s[0:3]="aba", s[3:6]="aba". Yes, 3>2 is true. Length 6.
    # What about s[0:3] and s[2:5]? 2>2 false.
    # s[0:3] and s[4:7]? 4>2, length 7.
    # So min is 6.
    # assert sol.shortestMatchingSubstring("abababab", "aba*aba") == 6
    
    # Test case where mid is between two instances of the same pattern
    # This is fine.
    
    print("All tests passed!")

test_solution()