import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    # Game analysis:
    # The game ends exactly when the last unvisited index is chosen for the
    # first time; the player making that move wins.  Each index i contributes
    # one forced "first visit" move plus (A_i - 1) optional "stall" moves that
    # become available only after i is first visited.
    #
    # Analyzing the reduced game (counter = unvisited indices, pool = stall
    # tokens, where stall-wars reduce to parity battles and taking a new index
    # i flips the pool parity by (A_i - 1) mod 2), the outcome is determined
    # by the parity of the total number of moves under optimal play:
    #   - If N is odd, Fennec (first player) can always force the last
    #     first-visit to land on his turn.
    #   - If N is even, Snuke's mirroring strategy wins for him unless Fennec
    #     can break the mirror parity, which is possible exactly when the
    #     number of odd A_i is odd (an odd A_i contributes an even number of
    #     stall tokens, letting Fennec flip the parity at the crucial moment).
    odd = sum(1 for x in A if x & 1)
    fennec_wins = (n % 2 == 1) or (odd % 2 == 1)
    print("Fennec" if fennec_wins else "Snuke")

if __name__ == "__main__":
    main()