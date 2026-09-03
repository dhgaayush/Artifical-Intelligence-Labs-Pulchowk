% Assignment 4: Length of a list
% Usage: list_length([a, b, c, d], L). → L = 4

list_length([], 0).
list_length([_ | T], Len) :-
    list_length(T, TailLen),
    Len is TailLen + 1.
