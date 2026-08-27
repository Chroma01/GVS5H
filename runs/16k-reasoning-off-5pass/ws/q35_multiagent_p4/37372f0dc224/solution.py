import sys

def solve():
    s = sys.stdin.readline().strip()
    if not s:
        return
    
    n = len(s)
    if n == 0:
        print("")
        return
    
    # If the string is already a palindrome, the shortest palindrome with prefix S is S itself.
    # But we need to find the longest palindromic suffix.
    # We use KMP's prefix function on T = S + '#' + reverse(S)
    
    r = s[::-1]
    t = s + '#' + r
    m = len(t)
    
    # Compute the prefix function (pi array) for t
    pi = [0] * m
    for i in range(1, m):
        j = pi[i-1]
        while j > 0 and t[i] != t[j]:
            j = pi[j-1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j
    
    # The last value in pi array gives the length of the longest prefix of t
    # that is also a suffix of t. Since t ends with r (reverse of s),
    # this is the length of the longest prefix of r that is a suffix of s.
    # A prefix of r is the reverse of a suffix of s.
    # So if the length is L, it means the suffix of s of length L is a palindrome.
    l = pi[m-1]
    
    # The part of s that is not part of the palindromic suffix is s[0 : n-l]
    # We need to append the reverse of this part to s.
    suffix_to_append = s[:n-l][::-1]
    result = s + suffix_to_append
    print(result)

if __name__ == '__main__':
    solve()