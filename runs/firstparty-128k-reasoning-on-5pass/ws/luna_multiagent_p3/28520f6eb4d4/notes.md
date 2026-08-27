- **Visibility condition:** For an observation point \((0,h)\), building \(i\) is visible only if the line to its top has a strictly larger slope than the line to every earlier building. Equality means the segment touches another building and is blocked.

- **Consecutive buildings suffice:** If all earlier buildings are visible, their slopes from the observation point increase with position. Therefore, for each building it is enough to compare it with the immediately preceding building.

- **Threshold:** For consecutive buildings \(i-1\) and \(i\), visibility requires
  \[
  \frac{H_i-h}{X_i}>\frac{H_{i-1}-h}{X_{i-1}},
  \]
  which is equivalent to
  \[
  h>\frac{X_iH_{i-1}-X_{i-1}H_i}{X_i-X_{i-1}}.
  \]

- **Answer:** The largest threshold is the maximum height at which visibility still fails. If every threshold is negative, height \(0\) already sees all buildings, so output `-1`. If the maximum threshold is zero, output `0`.

- **Exact comparison:** Store the maximum threshold as a numerator and positive denominator. Compare two fractions using cross multiplication, avoiding floating-point errors during computation.

- **Complexity:** One left-to-right pass, \(O(N)\) time and \(O(1)\) additional memory.
