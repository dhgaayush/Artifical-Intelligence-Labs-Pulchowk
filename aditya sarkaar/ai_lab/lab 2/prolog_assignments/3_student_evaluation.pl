% ============================================================
% Assignment 3: Student Evaluation System
% Forward and Backward Chaining
% ============================================================
% FOPL Representation:
%
%   Rule I:  ∀X (good_position(X) ∧ no_higher_marks(X) → first_position(X))
%   Rule II: ∀X (attends_lectures(X) ∧ studies_books(X) → covers_course(X))
%   Rule III:∀X (covers_course(X) → good_position(X))
%
% Facts:
%   i.   attends_lectures(student).
%   ii.  studies_books(student).
%   iii. no_higher_marks(student).
%
% Goal: Show first_position(student) using forward & backward chaining.
% ============================================================

% =======================
% PART A: Backward Chaining (Prolog's default inference)
% =======================

% --- Facts ---
attends_lectures(student).
studies_books(student).
no_higher_marks(student).

% --- Rules ---
% Rule III: covers_course(X) if X covers course contents
covers_course(X) :-
    attends_lectures(X),
    studies_books(X).

% Rule II (reordered for logical flow): good_position if covers course
good_position(X) :-
    covers_course(X).

% Rule I: first_position if good position AND no one with higher marks
first_position(X) :-
    good_position(X),
    no_higher_marks(X).

% --- Backward Chaining Query ---
% ?- first_position(student).
% Trace (backward):
%   first_position(student)
%     <- good_position(student) AND no_higher_marks(student)
%        good_position(student)
%          <- covers_course(student)
%             covers_course(student)
%               <- attends_lectures(student) [FACT] AND studies_books(student) [FACT]
%               => TRUE
%          => TRUE
%        no_higher_marks(student) [FACT] => TRUE
%     => TRUE
% Result: true

% =======================
% PART B: Forward Chaining (explicit demonstration)
% =======================
% Forward chaining works from facts toward the goal.
% We use assert/1 to derive new facts iteratively.

% Initialize: clear derived facts
:- dynamic derived/1.

% Forward chaining engine
forward_chain :-
    % Step 1: From facts attends_lectures(student) and studies_books(student)
    %         apply Rule II to derive covers_course(student)
    (   attends_lectures(S),
        studies_books(S),
        \+ derived(covers_course(S))
    ->  assert(derived(covers_course(S))),
        format('Step 1 (Rule II): Derived covers_course(~w)~n', [S])
    ;   true),

    % Step 2: From covers_course(student) apply Rule III
    %         to derive good_position(student)
    (   derived(covers_course(S)),
        \+ derived(good_position(S))
    ->  assert(derived(good_position(S))),
        format('Step 2 (Rule III): Derived good_position(~w)~n', [S])
    ;   true),

    % Step 3: From good_position(student) AND no_higher_marks(student)
    %         apply Rule I to derive first_position(student)
    (   derived(good_position(S)),
        no_higher_marks(S),
        \+ derived(first_position(S))
    ->  assert(derived(first_position(S))),
        format('Step 3 (Rule I): Derived first_position(~w)~n', [S])
    ;   true).

% Query to run forward chaining:
% ?- forward_chain.
% Expected output:
%   Step 1 (Rule II): Derived covers_course(student)
%   Step 2 (Rule III): Derived good_position(student)
%   Step 3 (Rule I): Derived first_position(student)

% Query to verify derived result:
% ?- derived(first_position(student)).
% Expected: true
