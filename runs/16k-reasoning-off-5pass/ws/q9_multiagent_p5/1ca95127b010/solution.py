import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    N = int(input_data[0])
    X = int(input_data[1])
    Y = int(input_data[2])
    S = input_data[3]
    T = input_data[4]

    # Helper function to decompose string into blocks
    def get_blocks(s):
        if not s:
            return []
        blocks = []
        current_char = s[0]
        count = 1
        for c in s[1:]:
            if c == current_char:
                count += 1
            else:
                blocks.append((current_char, count))
                current_char = c
                count = 1
        blocks.append((current_char, count))
        return blocks

    blocks_S = get_blocks(S)
    blocks_T = get_blocks(T)

    # If the number of blocks differs, the residue sequence cannot match
    if len(blocks_S) != len(blocks_T):
        print("No")
        return

    # Check total counts of '0's and '1's
    # The operations preserve the total count of 0s and 1s.
    # If counts differ, transformation is impossible.
    count_0_S = S.count('0')
    count_1_S = S.count('1')
    count_0_T = T.count('0')
    count_1_T = T.count('1')

    if count_0_S != count_0_T or count_1_S != count_1_T:
        print("No")
        return

    # Check residue sequence
    # The "residue" of a block is the part of its length that cannot be part of a swap operation.
    # For a block of '0's, the residue length is length % X.
    # For a block of '1's, the residue length is length % Y.
    # The sequence of residues must be identical in both S and T because residues cannot move past each other.
    for (c1, l1), (c2, l2) in zip(blocks_S, blocks_T):
        if c1 != c2:
            print("No")
            return
        if c1 == '0':
            if l1 % X != l2 % X:
                print("No")
                return
        else:
            if l1 % Y != l2 % Y:
                print("No")
                return

    print("Yes")

if __name__ == '__main__':
    solve()