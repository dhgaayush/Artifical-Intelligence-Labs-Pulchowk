% SEND + MORE = MONEY cryptarithmetic puzzle
% Using clpfd (Constraint Logic Programming over Finite Domains)

:- use_module(library(clpfd)).

solution(S, E, N, D, M, O, R, Y) :-
    Vars = [S, E, N, D, M, O, R, Y],
    Vars ins 0..9,
    % All letters must have distinct values
    all_different(Vars),
    % Leading digits cannot be 0
    S #\= 0,
    M #\= 0,
    % C4 must be 1 (carry from the leftmost column)
    M #= 1,
    % Column arithmetic (right to left)
    D + E #= Y + 10 * C1,
    N + R + C1 #= E + 10 * C2,
    E + O + C2 #= N + 10 * C3,
    S + M + C3 #= O + 10 * C4,
    C4 #= 1,
    % Label (find the solution)
    label(Vars).
