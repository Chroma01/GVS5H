import sys

def compute_pi(P):
    """Compute the KMP failure function (pi array) for string P."""
    m = len(P)
    pi = [0] * m
    k = 0
    for q in range(1, m):
        while k > 0 and P[k] != P[q]:
            k = pi[k-1]
        if P[k] == P[q]:
            k += 1
        pi[q] = k
    return pi

def solve():
    # Read input from stdin
    s = sys.stdin.readline().strip()
    if not s:
        return
    
    n = len(s)
    # If the string is already a palindrome, the answer is the string itself
    # But we'll use the general method which handles this case too.
    
    # Construct P = S + '#' + reverse(S)
    # Using a separator that is not in S (S contains only uppercase English letters)
    rev_s = s[::-1]
    P = s + '#' + rev_s
    
    # Compute the pi array for P
    pi = compute_pi(P)
    
    # The last value in pi array gives the length of the longest prefix of P
    # that is also a suffix of P.
    # Since P = S + '#' + rev_S, the suffix of P corresponds to a prefix of rev_S,
    # which is a suffix of S reversed.
    # The prefix of P corresponds to a prefix of S.
    # So pi[-1] is the length of the longest prefix of S that matches a suffix of rev_S.
    # This is equivalent to the length of the longest palindromic suffix of S.
    longest_pal_suffix_len = pi[-1]
    
    # The part of S that is not covered by the longest palindromic suffix
    # is S[0 : n - longest_pal_suffix_len]
    # We need to append the reverse of this part to S.
    prefix_to_append = s[:n - longest_pal_suffix_len]
    result = s + prefix_to_append[::-1]
    
    print(result)

if __name__ == '__main__':
    solve()