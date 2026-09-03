% ============================================================
% Assignment 1: Steve's Course Preference
% ============================================================
% FOPL Representation:
%   1. Steve only likes easy courses:
%      ∀X (likes(steve, X) → easy(X))
%      Prolog: likes(steve, X) :- course(X), easy(X).
%
%   2. Science courses are hard:
%      ∀X (science_course(X) → hard(X))
%      Prolog: hard(X) :- science_course(X).
%
%   3. All basket weaving courses are easy:
%      ∀X (basket_weaving_course(X) → easy(X))
%      Prolog: easy(X) :- basket_weaving_course(X).
%
%   4. BK301 is a basket weaving course:
%      basket_weaving_course(bk301).
%
% Goal: What course would Steve like?
%       ?- likes(steve, X).
% ============================================================

% --- Facts ---
course(bk301).
basket_weaving_course(bk301).

% --- Rules ---
% Steve only likes easy courses
likes(steve, X) :-
    course(X),
    easy(X).

% Science courses are hard
hard(X) :-
    science_course(X).

% All basket weaving courses are easy
easy(X) :-
    basket_weaving_course(X).

% --- Queries ---
% ?- likes(steve, X).
% Expected: X = bk301
