
## ideation
The core difficulty is that replacing a letter changes every occurrence of that letter simultaneously, so the transformation must first be consistent: every occurrence of a given source letter must correspond to the same target letter. After consistency is established, each non-identity mapping is an edge from a source letter to its target. Edges can form chains, but directed cycles cannot be executed directly because each replacement would destroy the letter needed by a later replacement. A temporary letter is needed to break every cycle. Such a letter must not appear in the final string T; otherwise its temporary occurrences could not all be eliminated. Since the alphabet has only 26 letters, this condition can be checked directly.

Important pitfalls include counting only distinct non-identity source letters, not positions; treating self-mappings as no operation; detecting cycles only among non-identity mappings; and recognizing that a mapping conflict immediately makes the answer impossible. If T contains all 26 letters, no temporary letter exists, so any nontrivial cycle makes the transformation impossible. Acyclic mappings remain executable in reverse dependency order without extra operations.

## worker: Implement the functional-graph solution: validate 
The source-to-target mapping must be consistent for every character in `S`; otherwise the transformation is impossible.

Each distinct non-identity mapping requires one operation. A directed cycle cannot be performed directly, so each cycle requires one additional temporary letter. Such a letter exists exactly when some lowercase letter is absent from `T`. If all 26 letters occur in `T`, any nontrivial cycle is impossible.
