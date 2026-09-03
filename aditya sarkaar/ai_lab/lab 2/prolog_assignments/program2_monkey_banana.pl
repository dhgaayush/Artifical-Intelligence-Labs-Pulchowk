% ============================================================
% Program 2: Monkey-Banana Problem
% First Order Predicate Logic (FOPL) to Prolog
% ============================================================
% FOPL Representation:
%
% Objects: monkey, chair, bananas
%
% Facts:
%   in_room(monkey).   in_room(chair).   in_room(bananas).
%   dexterous(monkey).  tall(chair).
%   can_move(monkey, chair, bananas).
%   can_climb(monkey, chair).
%
% Rules:
%   can_reach(X,Y) ← dexterous(X) ∧ close(X,Y)
%   close(X,Z)     ← get_on(X,Y) ∧ under(Y,Z) ∧ tall(Y)
%   get_on(X,Y)    ← can_climb(X,Y)
%   under(Y,Z)     ← in_room(X) ∧ in_room(Y) ∧ in_room(Z)
%                     ∧ can_move(X,Y,Z)
%
% Goal: ?- can_reach(monkey, bananas). → true
% ============================================================

% --- Facts ---
in_room(bananas).
in_room(chair).
in_room(monkey).

dexterous(monkey).
tall(chair).

can_move(monkey, chair, bananas).
can_climb(monkey, chair).

% --- Rules ---

% Rule: The monkey can reach Y if it is dexterous and close to Y
can_reach(X, Y) :-
    dexterous(X),
    near(X, Y).

% Rule: X is near Z if X gets on Y, Y is under Z, and Y is tall
near(X, Z) :-
    get_on(X, Y),
    under(Y, Z),
    tall(Y).

% Rule: X gets on Y if X can climb Y
get_on(X, Y) :-
    can_climb(X, Y).

% Rule: Y is under Z if all three objects are in the room and
%        X can move Y to Z
under(Y, Z) :-
    in_room(X),
    in_room(Y),
    in_room(Z),
    can_move(X, Y, Z).

% --- Query ---
% ?- can_reach(monkey, bananas).
% Expected: true
%
% Inference chain (backward):
%   can_reach(monkey, bananas)
%     <- dexterous(monkey)           [FACT]
%     AND close(monkey, bananas)
%        <- get_on(monkey, chair)
%           <- can_climb(monkey, chair) [FACT]
%           => TRUE
%        AND under(chair, bananas)
%           <- in_room(monkey)       [FACT]
%           AND in_room(chair)       [FACT]
%           AND in_room(bananas)     [FACT]
%           AND can_move(monkey, chair, bananas) [FACT]
%           => TRUE
%        AND tall(chair)             [FACT]
%        => TRUE
%     => TRUE
