import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    S = input_data[0]
    n = len(S)
    
    # Construct the string T = S + '#' + reverse(S)
    # '#' is a separator not present in uppercase English letters
    rev_S = S[::-1]
    T = S + '#' + rev_S
    m = len(T)
    
    # Compute KMP pi array
    pi = [0] * m
    for i in range(1, m):
        j = pi[i-1]
        while j > 0 and T[i] != T[j]:
            j = pi[j-1]
        if T[i] == T[j]:
            j += 1
        pi[i] = j
    
    # The length of the longest suffix of S that is a prefix of rev_S
    # is given by pi[m-1]
    match_len = pi[m-1]
    
    # The part of rev_S that needs to be appended is rev_S[0 : n - match_len]
    # Because the suffix of S of length match_len matches the prefix of rev_S of length match_len.
    # We need to append the remaining characters of rev_S to complete the palindrome.
    # The palindrome is S + rev_S[0 : n - match_len]
    
    result = S + rev_S[:n - match_len]
    print(result)

if __name__ == '__main__':
    solve()