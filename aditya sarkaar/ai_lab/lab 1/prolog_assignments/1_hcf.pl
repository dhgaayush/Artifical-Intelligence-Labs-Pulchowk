% Assignment 1: HCF (GCD) of two numbers using Euclidean algorithm
% Usage: hcf(36, 24, R). → R = 12

hcf(X, 0, X) :- X > 0.
hcf(X, Y, R) :-
    Y > 0,
    Rem is X mod Y,
    hcf(Y, Rem, R).

% Alternative: if first number might be 0
hcf(0, Y, Y) :- Y > 0.
