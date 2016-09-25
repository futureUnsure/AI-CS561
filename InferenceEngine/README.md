Inference Engine : Logic Programming
====================================

Summary:
--------
- Simulates Logic Programming primitives on a Knowledge Base
- Computes if the given query can be inferred from the Knowledge Base or not
- Uses Backward Chaining algorithm with loop detection for inference

Introduction
------------
- With the rise of social media, we are sharing more and more information about us with the world
- Enterprise sees this as an opportunity, but what do we lose in return?
- How much control do we have on over our private information? Do we really share what we want to share?
- Using an inference engine, we can find out if a certain type of personal information can be extracted by that enterprise if it gains access to another set of information about the user.


Input Specifications:
---------------------
- Number of Queries
- Queries follow (For each of them, have to determine whether it can be inferred or not)
- Number of Clauses in the Knowledge Base
- Clauses follow
- Each clause is either an ```implication```, or a ```fact```
- Implication: ``` P1 ^ P2 ^ ... Pn => Q ```
- Fact:  '''P''' or '''~P'''(Atomic sentences)
- All ```P``` and ```Q``` are either a literal or a negative of a literal
- Number of stones in player 2's mancala
- Number of stones in player 1's mancala

Output:
-------
- For each of the Query in the Input, print ```TRUE``` if it could be inferred else print ```FALSE```
- Output file is ```output.txt```

Usage:
------
	python inference.py <path_to_input_file>

	 




