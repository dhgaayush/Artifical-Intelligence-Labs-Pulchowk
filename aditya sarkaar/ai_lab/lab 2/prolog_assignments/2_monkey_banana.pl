% =============================================================
% Program 2 (Worked Example): The Monkey - Banana Problem
% =============================================================
% A monkey, a chair and some bananas are in a room. The bananas are
% hung from the ceiling, out of the monkey's reach. The monkey is
% dexterous, can move the chair under the bananas and climb on it.
% Prove that the monkey can reach the bananas.
%
% The sheet's GOAL has a typo ("can_reach(monkey, appple)") - it must
% be bananas.
%
%  can_reach(monkey, bananas)  ->  true
% =============================================================

% ---------- Facts ----------
in_room(bananas).
in_room(chair).
in_room(monkey).

dexterous(monkey).
tall(chair).

can_move(monkey, chair, bananas).   % monkey can push chair under bananas
can_climb(monkey, chair).

% ---------- Rules ----------
% Rule 1: A dexterous being that is near something can reach it.
can_reach(X, Y) :-
    dexterous(X),
    close(X, Y).

% Rule 2: A being is close to Z if it gets on Y, Y is under Z, and Y is tall.
close(X, Z) :-
    get_on(X, Y),
    under(Y, Z),
    tall(Y).

% Rule 3: X gets on Y if X can climb Y.
get_on(X, Y) :-
    can_climb(X, Y).

% Rule 4: Object Y is under Z when both Y and Z (and the mover X) are
%         in the room and X can move Y to Z.
under(Y, Z) :-
    in_room(X),
    in_room(Y),
    in_room(Z),
    can_move(X, Y, Z).

% ---------- Example queries ----------
% ?- can_reach(monkey, bananas).   -> true
% ?- close(monkey, bananas).       -> true
% ?- under(chair, bananas).        -> true
