
## ideation
The core difficulty is modeling repeated smoke generation correctly: smoke is created at the origin whenever the origin is empty, while all existing smoke moves together under each wind direction. A useful abstraction is to label each smoke batch by its creation time and express its position using cumulative wind displacement. The target question then becomes whether some earlier creation point corresponds to the required displacement.

Care is needed with time indexing: the initial origin position must be included before processing any wind, and the answer for step t is evaluated after the t-th movement and possible generation event. Coordinate signs must also match the statement: N decreases the row and W decreases the column.

The constraints require an O(N) or O(N log N) scan, while explicitly simulating all smoke cells can become quadratic or worse. Since only existence at one target cell is queried, storing all previously relevant cumulative positions is sufficient.

## worker: Implement the O(N) prefix-displacement solution: i
The cumulative wind displacement after time `t` is `(row, col)`. A smoke batch generated when the cumulative displacement was `(x, y)` is located at `(row - x, col - y)` at time `t`.

Therefore, smoke is at `(R, C)` exactly when `(row - R, col - C)` is among the previously visited cumulative displacement coordinates. Including `(0, 0)` handles the smoke initially present at the campfire. The algorithm runs in `O(N)` expected time and `O(N)` space.
