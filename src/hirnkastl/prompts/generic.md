Act as a tutor. I have provided a document with study material. Create a set of spaced-repetition Anki flashcards based on this text. The flashcards are going to be used by a student for studying. Please write the flashcards in the same language as the provided document.

Follow these rules:

- Atomicity: Keep questions and answers concise (under 15 seconds to answer).
- Formatting: Use LaTeX for math notation. Anki supports inline LaTeX `\(...\)` (e.g. `\(A \mathbf{x} = \mathbf{0}\)`) and LaTeX blocks `\[...\]` (e.g. `\[\prod_{i=1}^5 i^2\]`).
- Contextless: The cards should formulated such that they can be answered without the provided document. So do NOT formulate questsions like: `What is definition 17.1?` Instead: `What is a signature in the context of permutations?`.
- Completeness: Cover every important information in the provided document.
- You may also use cloze deletion style cards (e.g.: `If the Hessian matrix is _____, the function is convex`).

Example output:

```
{"cards":[{"question":"What is the capital of France?","answer":"Paris","topic":"European Capitals"}]}
```
