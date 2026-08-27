import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    s = input_data[0]
    n = len(s)
    
    # If the string is empty, nothing to do (though constraints say length >= 1)
    if n == 0:
        print("")
        return

    # We want to find the longest palindromic prefix of s.
    # This is equivalent to finding the longest prefix of s that is also a suffix of reverse(s).
    # We construct a string T = s + '#' + reverse(s).
    # The KMP prefix function pi[i] stores the length of the longest proper prefix of T[0..i]
    # that is also a suffix of T[0..i].
    # The value pi[len(T)-1] will give us the length of the longest prefix of s that matches a suffix of reverse(s).
    
    # Use a separator that is not in 'A'-'Z'. '#' is safe.
    rev_s = s[::-1]
    t = s + '#' + rev_s
    m = len(t)
    
    pi = [0] * m
    for i in range(1, m):
        j = pi[i-1]
        while j > 0 and t[i] != t[j]:
            j = pi[j-1]
        if t[i] == t[j]:
            j += 1
        pi[i] = j
    
    # The length of the longest palindromic prefix
    longest_pal_prefix_len = pi[m-1]
    
    # The part of s that is NOT part of the palindromic prefix needs to be reversed and appended.
    # The suffix to append is s[longest_pal_prefix_len : ]
    suffix_to_append = s[longest_pal_prefix_len:]
    result = s + suffix_to_append[::-1]
    
    print(result)

if __name__ == '__main__':
    solve()