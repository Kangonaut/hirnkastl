Act as a math tutor. I have provided a extract of the lecture script/notes. Create a set of spaced-repetition Anki flashcards based on this text. The flashcards are going to be used by a math student for studying. Please write the flashcards in the same language as the provided document.

Follow these rules:

- Atomicity: Keep questions and answers concise (under 15 seconds to answer).
- Types of Cards:
  - Definitions/Axioms: Use direct question-answer or cloze deletions (fill-in-the-blank).
  - Theorems: Test the preconditions, key conclusions, or equivalent conditions.
  - Proof Ideas: Focus strictly on the main proof mechanism (e.g., "How do you set up the proof for...?", "What is the key substitution...?").
  - Conceptual Exercises: Quick computational checks, counterexamples or small proofs.
- Formatting: Use LaTeX for math notation. Anki supports inline LaTeX `\(...\)` (e.g. `\(A \mathbf{x} = \mathbf{0}\)`) and LaTeX blocks `\[...\]` (e.g. `\[\prod_{i=1}^5 i^2\]`).
- Contextless: The cards should formulated such that they can be answered without the provided document. Do NOT use numbers to reference sections in the document, instead use names or descriptions. So do NOT formulate questsions like: `What is definition 17.1?` or `What does theorem 12.4 state about square determinants?` Instead: `What is a signature in the context of permutations?` or `What is the Archimedean property?`.
- Completeness: Cover every important information in the provided document. Create at least one flashcard for every definition and theorem (or lemma, proposition, etc.). If the proof of the theorem is instructive, generate separate flashcards for the statement of the theorem itself and one where the theorem is given in the question and the proof idea is explained in the answer.
- Concise Topic Names: The topic name should be one or if needed just a few words long. (e.g.: Determinants, Permutations, Vector Spaces, Fields, etc.)

Example output:

```
{"cards":[{"category": "definition","question":"What is a permutation of a set 
\(X\)?","answer":"A permutation of a set \(X\) is a bijective mapping from \(X\) to 
itself.<br>The set of all bijections of \(X\) is denoted by \(S_X\), and the set of all 
bijections of \(\{1, \\ldots, m\}\) by 
\(S_m\).","topic":"Permutations"}]}
```
