- **Parity condition:** A red move flips the parity of row+column, while a blue move preserves it. A closed cycle therefore needs an even number of red moves, so R must be even. If R=0, every move is blue and flips row parity, so B must be even. The program prints No exactly for R odd or R=0 with B odd.

- **Sample exact fix:** For (R,B)=(2,3), the program emits the sample's five lines exactly, using `"R 3 2" + " "` to keep the required trailing space. For all-red B=0 cases, it now uses 1-based coordinates: row 1 columns 1..k, then row 2 columns k..1, where k=R//2. This makes (4,0) match the sample and remains valid for every even R.

- **All-red construction:** The two-row rectangle perimeter gives a red cycle. Consecutive moves are horizontal or vertical, and the last point returns vertically to the first. Coordinates stay within 1..100000.

- **All-blue construction:** For B=2k, raw points are (a,a) for a=0..k-1, then (a+1,a-1) for a=k-1..0. Consecutive moves are diagonal, the last point returns diagonally to (0,0), and all points are distinct. These are shifted by OFF=10**6.

- **Mixed even-blue construction:** For R=2kr and B=2m, red uses rows 0 and 1 with nonnegative columns, forming a path from (0,0) to (1,0). Blue uses (2+t,-t) for t=0..m-1, then (y,-y) for y=m..1. The red-to-blue transition is vertical, all blue moves are diagonal, and the final blue point returns diagonally to (0,0). Red and blue sets are disjoint.

- **Mixed odd-blue construction:** For R=2kr and B=2n+1, red uses rows 0 and 1 with nonpositive columns, forming a path from (0,0) to (1,0). Blue uses (1-t,1+t) for t=0..n, then (-t,t) for t=n..1. The red-to-blue transition is horizontal, all blue moves are diagonal, and the final blue point returns diagonally to (0,0). The second blue loop is empty when n=0, handling B=1.

- **Bounds:** All raw coordinates in shifted constructions are within about [-100000,100001], so adding OFF=10**6 keeps them inside [1,10^9]. The special sample case and all-red 1-based case are also well inside the board.

- **Complexity:** Each test case outputs O(R+B) lines, total O(sum(R+B)+T). The program builds all lines in a list and writes once, with a final newline.

- **Verification:** The sample now produces the expected lines, including the trailing space after R 3 2. Each Yes output has the correct number of pieces, unique coordinates, valid one-move transitions according to the color of the current piece, and a closing move from the last piece to the first.
