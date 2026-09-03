% =============================================================
% Program 1 (Worked Example): The Weapons / Criminal problem
% =============================================================
% Natural language statements -> FOPL -> Prolog
%
%  1. Every American who sells weapons to hostile nations is a criminal.
%        FOPL:  forall x ( American(x) /\ exists y ( Weapon(y) /\ Sells(x,y) /\
%                                   Hostile(y) ) -> Criminal(x) )
%  2. Every enemy of America is a hostile.
%        FOPL:  forall x ( EnemyOfAmerica(x) -> Hostile(x) )
%  3. Iraq has some missiles.
%        FOPL:  exists x ( Missile(x) /\ Owns(iraq, x) )
%        (modelled as the fact has_missile(iraq).)
%  4. All missiles of Iraq were sold by George.
%        FOPL:  forall x ( Missile(x) /\ Owns(iraq, x) -> Sells(george, x) )
%  5. George is an American.            american(george).
%  6. Iraq is a country.                country(iraq).
%  7. Iraq is the enemy of America.     enemy_of_america(iraq).
%  8. Missiles are weapons.
%        FOPL:  forall x ( Missile(x) -> Weapon(x) )
%
% GOAL:  ?- criminal(george).  ->  true
% =============================================================

% ---------- Facts ----------
american(george).
country(iraq).
enemy_of_america(iraq).
has_missile(iraq).
sells_missiles(george, iraq).     % George sold Iraq's missiles

% ---------- Rules ----------
% Rule 1: An American who sells weapons (missiles) to a hostile nation
%         is a criminal.
criminal(X) :-
    american(X),
    sells_missiles(X, Y),
    hostile(Y).

% Rule 2: Any country that is an enemy of America is hostile.
hostile(X) :-
    enemy_of_america(X).

% (In the lab sheet, "hostile(X) :- country(X)." also appears; this would
%  make *every* country hostile. We keep the more specific enemy rule so the
%  proof follows the intended chaining. Both give the same goal result here.)

% ---------- Example queries ----------
% ?- criminal(george).         -> true
% ?- hostile(iraq).            -> true
% ?- enemy_of_america(iraq).   -> true
