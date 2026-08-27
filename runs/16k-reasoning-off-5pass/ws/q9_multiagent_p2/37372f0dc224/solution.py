import sys

# Increase recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read input from stdin
    s = sys.stdin.readline().strip()
    
    # Edge case: empty string (though constraints say length >= 1)
    if not s:
        return

    # Construct T = S + '#' + reverse(S)
    # '#' is a separator not present in uppercase English letters
    rev_s = s[::-1]
    t = s + '#' + rev_s
    
    n = len(t)
    pi = [0] * n
    
    # Compute KMP prefix function (pi array)
    # pi[i] is the length of the longest proper prefix of t[0...i] 
    # that is also a suffix of t[0...i].
    for i in range(1, n):
        j = pi[i-1]
        while j > 0 and t[i] != t[j]:
            j = pi[j-1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j
    
    # The length of the longest suffix of S that is a prefix of reverse(S)
    # is given by pi[n-1].
    match_len = pi[n-1]
    
    # The number of characters to append is len(S) - match_len
    # We append the first (len(S) - match_len) characters of reverse(S)
    # which corresponds to the part of reverse(S) that doesn't overlap with the suffix of S.
    append_len = len(s) - match_len
    suffix_to_append = rev_s[:append_len]
    
    result = s + suffix_to_append
    print(result)

if __name__ == '__main__':
    solve()