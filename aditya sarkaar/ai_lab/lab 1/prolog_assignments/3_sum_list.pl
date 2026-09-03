% Assignment 3: Sum of an integer list
% Usage: sum_list([1, 2, 3, 4], S). → S = 10

sum_list([], 0).
sum_list([H | T], Sum) :-
    sum_list(T, TailSum),
    Sum is H + TailSum.
