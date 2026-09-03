% Assignment 6: Filter a list of integers to keep only 1s and 2s
% Usage: filter_ones_twos([1,2,4,5,2,4,5,1,1], R). → R = [1, 2, 2, 1, 1]

filter_ones_twos([], []).
filter_ones_twos([H | T], [H | R]) :-
    (H = 1 ; H = 2),
    filter_ones_twos(T, R).
filter_ones_twos([H | T], R) :-
    H \= 1,
    H \= 2,
    filter_ones_twos(T, R).
