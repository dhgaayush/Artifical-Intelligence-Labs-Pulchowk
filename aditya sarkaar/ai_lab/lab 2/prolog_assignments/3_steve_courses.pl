% =============================================================
% Assignment 1: Steve's course preference (resolution question)
% =============================================================
% Facts given:
%   * Steve only likes easy courses.
%   * Science courses are hard.
%   * All courses in the basket-weaving department are easy.
%   * BK301 is a basket-weaving course.
%
% Question:  "What course would Steve like?"
%            -> Steve likes BK301 (and, in general, easy courses).
% =============================================================

% ---------- Facts ----------
course(bk301).                       % BK301 is a course
basket_weaving_course(bk301).        % BK301 belongs to basket-weaving dept.
science_course(cs101).               % (a science course, for contrast)

% ---------- Rules ----------
% Steve only likes easy courses.
steve_likes(C) :-
    easy(C).

% All courses in the basket-weaving department are easy.
easy(C) :-
    basket_weaving_course(C).

% Science courses are hard (so Steve, who likes only easy courses,
% does NOT like science courses).
hard(C) :-
    science_course(C).

% A course that Steve likes cannot be hard.
steve_dislikes(C) :-
    hard(C).

% ---------- Queries ----------
% ?- steve_likes(C).           -> C = bk301     (what Steve likes)
% ?- steve_likes(bk301).       -> true          (resolution: yes)
% ?- steve_likes(cs101).       -> false         (science = hard)
%
% Resolution derivation:
%   (a) likes(steve, X) :- easy(X).
%   (b) easy(X)        :- basket_weaving(X).
%   (c) basket_weaving(bk301).
%   From (a)+(b): likes(steve, X) :- basket_weaving(X).
%   Resolve with (c): likes(steve, bk301).     QED
% =============================================================
