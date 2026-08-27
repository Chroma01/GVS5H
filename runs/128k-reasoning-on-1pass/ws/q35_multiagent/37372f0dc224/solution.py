import sys

def solve():
    # Read input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    S = input_data[0]
    N = len(S)
    
    # Construct T = S_rev + '#' + S
    # The '#' acts as a unique separator to prevent matching across S and S_rev incorrectly
    S_rev = S[::-1]
    T = S_rev + '#' + S
    M = len(T)
    
    # Compute KMP prefix function (pi array)
    # pi[i] is the length of the longest proper prefix of T[0...i] 
    # that is also a suffix of T[0...i]
    pi = [0] * M
    for i in range(1, M):
        j = pi[i-1]
        while j > 0 and T[i] != T[j]:
            j = pi[j-1]
        if T[i] == T[j]:
            j += 1
        pi[i] = j
    
    # The last value in the pi array gives the length of the longest prefix of T
    # that is also a suffix of T. Since T starts with S_rev and ends with S,
    # this corresponds to the longest string that is a prefix of S_rev and a suffix of S.
    # This string is necessarily a palindrome, and its length k is the length of
    # the longest palindromic suffix of S.
    k = pi[M-1]
    
    # To form the shortest palindrome with S as prefix, we append the reverse of
    # the non-palindromic prefix of S.
    # The non-palindromic prefix is S[0 : N-k]
    prefix_to_append = S[:N-k]
    result = S + prefix_to_append[::-1]
    
    print(result)

if __name__ == '__main__':
    solve()