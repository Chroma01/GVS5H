import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    n = int(input_data[0])
    a = list(map(int, input_data[1:]))

    # dp[i] represents the maximum score obtainable from the prefix a[0...i-1]
    # The recurrence relation is:
    # dp[i] = max(dp[i-1], dp[i-2] + abs(a[i-1] - a[i-2]))
    #
    # Explanation:
    # When considering the prefix of length i (elements a[0]...a[i-1]):
    # 1. We can choose not to pair a[i-1] with a[i-2] in the last operation involving the end of the prefix.
    #    In this case, the best score is simply the best score for the prefix of length i-1.
    #    Note: This "skipping" effectively allows a[i-1] to be left unpaired or paired with an earlier element
    #    after intermediate elements are removed. The structure of the problem (removing adjacent pairs)
    #    implies that any valid matching can be decomposed this way.
    # 2. We can choose to pair a[i-1] with a[i-2]. The score gained is abs(a[i-1] - a[i-2]).
    #    The remaining problem is to find the max score for the prefix of length i-2.
    #
    # This DP works because removing adjacent elements brings previously non-adjacent elements together.
    # By allowing "skipping" (dp[i-1]), we account for the possibility that the last element is not paired
    # with its immediate left neighbor in the original array, but rather with someone further left after
    # the elements between them have been removed. The optimal substructure holds.

    if n == 0:
        print(0)
        return
    if n == 1:
        print(0)
        return

    # dp array of size n+1
    dp = [0] * (n + 1)
    
    # Base cases
    dp[0] = 0
    dp[1] = 0
    
    for i in range(2, n + 1):
        # Option 1: Skip pairing a[i-1] with a[i-2]
        # The max score is the same as for the prefix of length i-1
        opt1 = dp[i-1]
        
        # Option 2: Pair a[i-1] with a[i-2]
        # The score is abs(a[i-1] - a[i-2]) plus the max score for the prefix of length i-2
        opt2 = dp[i-2] + abs(a[i-1] - a[i-2])
        
        dp[i] = max(opt1, opt2)
        
    print(dp[n])

if __name__ == '__main__':
    solve()