% ============================================================
% Assignment 2: Horses and Mammals
% ============================================================
% FOPL Representation:
%   1. Horses are mammals:
%      ∀X (horse(X) → mammal(X))
%      Prolog: mammal(X) :- horse(X).
%
%   2. An offspring of a horse is a horse:
%      ∀X,Y (offspring(X,Y) ∧ horse(Y) → horse(X))
%      Prolog: horse(X) :- offspring(X,Y), horse(Y).
%
%   3. Bluebeard is Charlie's parent:
%      parent(bluebeard, charlie).
%
%   4. Offspring and parents are inverse relations:
%      ∀X,Y (offspring(X,Y) ↔ parent(Y,X))
%      Prolog: offspring(X,Y) :- parent(Y,X).
%
%   5. Every mammal has a parent:
%      ∀X (mammal(X) → ∃Y parent(Y,X))
%      Prolog: parent(Y,X) :- mammal(X). (simplified)
%
% Goal: Is Charlie a horse?  ?- horse(charlie).
% ============================================================

% --- Facts ---
parent(bluebeard, charlie).

% We also need: Bluebeard is a horse (to test inference)
horse(bluebeard).

% --- Rules ---
% 1. Horses are mammals
mammal(X) :- horse(X).

% 2. An offspring of a horse is a horse
horse(X) :-
    offspring(X, Y),
    horse(Y).

% 4. Offspring and parents are inverse relations
offspring(X, Y) :- parent(Y, X).

% 5. Every mammal has a parent (represented as a constraint, not used for inference)
% has_parent(X) :- mammal(X).

% --- Queries ---
% ?- horse(charlie).
% Expected: true
%
% ?- mammal(charlie).
% Expected: true
