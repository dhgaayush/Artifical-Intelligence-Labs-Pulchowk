% Assignment 2: Family relationships - facts and rules for deductions
% Facts: parent(Parent, Child)

parent(john, mary).
parent(john, tom).
parent(mary, anna).
parent(mary, peter).
parent(tom, lisa).
parent(anna, david).

% Facts: male and female
male(john).
male(tom).
male(peter).
male(david).
female(mary).
female(anna).
female(lisa).

% Rules (deductions)
father(F, C) :- parent(F, C), male(F).
mother(M, C) :- parent(M, C), female(M).
child(C, P) :- parent(P, C).
grandparent(GP, GC) :- parent(GP, P), parent(P, GC).
grandfather(GF, GC) :- grandparent(GF, GC), male(GF).
grandmother(GM, GC) :- grandparent(GM, GC), female(GM).
sibling(A, B) :- parent(P, A), parent(P, B), A \= B.
brother(B, S) :- sibling(B, S), male(B).
sister(S, B) :- sibling(S, B), female(S).
ancestor(A, D) :- parent(A, D).
ancestor(A, D) :- parent(A, X), ancestor(X, D).

% Example queries:
% ?- father(john, mary).      → true
% ?- grandparent(john, anna).  → true
% ?- sibling(mary, tom).       → true
% ?- ancestor(john, david).    → true
