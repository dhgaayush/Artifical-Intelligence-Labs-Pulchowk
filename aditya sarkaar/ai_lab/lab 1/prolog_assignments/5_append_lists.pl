% Assignment 5: Append two lists
% Usage: append_lists([1, 2], [3, 4], R). → R = [1, 2, 3, 4]

append_lists([], L, L).
append_lists([H | T], L2, [H | Result]) :-
    append_lists(T, L2, Result).
