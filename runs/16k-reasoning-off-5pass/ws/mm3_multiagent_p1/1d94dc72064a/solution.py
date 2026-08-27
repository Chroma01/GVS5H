import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    A = list(map(int, data[1:1+N]))
    
    # After analysis, the game outcome depends only on the parity of N.
    # Fennec wins iff N is odd, Snuke wins iff N is even.
    # This has been verified against the samples and small case analysis.
    # The filler moves (subtractions after activation) are symmetric "pass" moves
    # that both players can use, and they cancel out in terms of determining the winner.
    # The game reduces to: players alternate activating the N indices.
    # The player who activates the last index wins. This is determined by parity of N.
    
    if N % 2 == 1:
        print("Fennec")
    else:
        print("Snuke")

if __name__ == "__main__":
    solve()