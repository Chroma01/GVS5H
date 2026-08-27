import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]
    t = input_data[2]

    # Map to store the required transformation for each character in S
    # s_char -> t_char
    mapping = {}
    
    # Check feasibility and build the mapping
    # If a character in S appears at multiple positions, it must map to the same character in T.
    # If S[i] == S[j] but T[i] != T[j], it's impossible because a global replacement 
    # affects all occurrences of a character simultaneously.
    for i in range(n):
        char_s = s[i]
        char_t = t[i]
        
        if char_s in mapping:
            # If char_s was already mapped, it must map to the same char_t
            if mapping[char_s] != char_t:
                print("-1")
                return
        else:
            mapping[char_s] = char_t

    # Count the number of unique characters in S that need to be changed.
    # Each operation can target exactly one character in S and replace all its occurrences.
    # Since we cannot merge operations (e.g., changing 'a' to 'b' and then 'b' to 'c' 
    # doesn't help if 'a' needs to become 'c' and 'b' needs to become 'd' simultaneously 
    # without affecting other dependencies incorrectly), the minimum number of operations 
    # is simply the count of unique characters in S where mapping[char_s] != char_s.
    operations = 0
    for char_s in mapping:
        if mapping[char_s] != char_s:
            operations += 1
            
    print(operations)

if __name__ == '__main__':
    solve()