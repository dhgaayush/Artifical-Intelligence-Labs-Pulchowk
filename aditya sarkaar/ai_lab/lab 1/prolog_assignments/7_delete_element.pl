% Assignment 7: Delete a given element from a list (all occurrences)
% Usage: delete_element([1, 2, 3, 2, 4], 2, R). → R = [1, 3, 4]

delete_element(_, [], []).
delete_element(X, [X | T], R) :- delete_element(X, T, R), !.
delete_element(X, [H | T], [H | R]) :- delete_element(X, T, R).
