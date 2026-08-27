import sys

# Increase recursion depth just in case, though we use an iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    # Using sys.stdin.read().split() handles whitespace and newlines robustly
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return
    
    s = input_data[0]
    n = len(s)
    
    # Edge case: single character is already a palindrome
    if n == 1:
        print(s)
        return

    # We want to find the longest suffix of S that is also a prefix of reverse(S).
    # Let S^R be the reverse of S. We are looking for the longest string X such that:
    # S ends with X AND S^R starts with X.
    # This is equivalent to finding the longest proper prefix of (S + '#' + S^R) 
    # that is also a suffix of (S + '#' + S^R).
    
    rev_s = s[::-1]
    # Use a separator that is not an uppercase English letter. 
    # '#' is safe as per constraints.
    separator = '#'
    t = s + separator + rev_s
    
    m = len(t)
    pi = [0] * m
    
    # Compute KMP prefix function (pi array)
    # pi[i] is the length of the longest proper prefix of t[0...i] 
    # that is also a suffix of t[0...i].
    for i in range(1, m):
        j = pi[i-1]
        while j > 0 and t[i] != t[j]:
            j = pi[j-1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j
    
    # The value pi[m-1] gives the length of the longest suffix of t that is also a prefix of t.
    # Since t ends with S^R, this suffix must be a suffix of S^R (which is a prefix of S reversed)
    # and a prefix of t (which starts with S).
    # Thus, pi[m-1] is the length of the longest suffix of S that matches a prefix of S^R.
    overlap_len = pi[m-1]
    
    # The shortest palindrome is S concatenated with the part of S^R that is NOT covered by the overlap.
    # The overlap covers the last 'overlap_len' characters of S (which match the first 'overlap_len' of S^R).
    # We need to append the first (n - overlap_len) characters of S^R.
    
    append_len = n - overlap_len
    result = s + rev_s[:append_len]
    
    print(result)

if __name__ == '__main__':
    solve()