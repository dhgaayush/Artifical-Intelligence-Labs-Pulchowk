% ============================================================
% Program 1: Criminal / Weapons / Iraq Problem
% First Order Predicate Logic (FOPL) to Prolog
% ============================================================
% FOPL Representation:
%
%  1. Every American who sells weapons to hostile nations is a criminal:
%     ∀X (american(X) ∧ sells_weapons(X,Y) ∧ hostile(Y) → criminal(X))
%
%  2. Every enemy of America is a hostile nation:
%     ∀X (enemy_of_america(X) → hostile(X))
%
%  3. Iraq has some missiles:
%     ∃X (missile(X) ∧ owns(iraq, X))
%
%  4. All missiles of Iraq were sold by George:
%     ∀X (missile(X) ∧ owns(iraq,X) → sells(george, X, iraq))
%
%  5. George is an American:
%     american(george).
%
%  6. Iraq is a country:
%     country(iraq).
%
%  7. Iraq is the enemy of America:
%     enemy_of_america(iraq).
%
%  8. Missiles are weapons:
%     ∀X (missile(X) → weapon(X))
%
% Goal: ?- criminal(george).  → true
% ============================================================

% --- Predicates ---
% hostile/1, enemy_of_america/1, american/1, criminal/1
% sells_weapons/2, has_missile/1, country/1

% --- Facts ---
enemy_of_america(iraq).
has_missile(iraq).
sells_weapons(george, iraq).
american(george).
country(iraq).

% --- Rules ---
% Rule 1: An American who sells weapons to a hostile nation is a criminal
criminal(X) :-
    american(X),
    sells_weapons(X, Y),
    hostile(Y).

% Rule 2: Every enemy of America is a hostile nation
hostile(X) :-
    enemy_of_america(X).

% Rule 2 (alt): A country that is an enemy of America is also hostile
hostile(X) :-
    country(X),
    enemy_of_america(X).

% --- Query ---
% ?- criminal(george).
% Expected: true
%
% Inference chain:
%   criminal(george)
%     <- american(george)           [FACT]
%     AND sells_weapons(george, iraq) [FACT]
%     AND hostile(iraq)
%        <- enemy_of_america(iraq)  [FACT]
%     => true
