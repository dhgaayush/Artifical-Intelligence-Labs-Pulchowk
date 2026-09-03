% Australia Map Colouring Problem (Constraint Satisfaction)
% Regions: WA, NT, Q, NSW, V, SA, T
% Domain : {red, green, blue}  (encoded as 1, 2, 3)
% Constraint: adjacent regions must have different colours.

:- use_module(library(clpfd)).

% solve(-Colouring)
% Colouring is a list Region-Colour where Colour is in 1..3.
solution(Colouring) :-
    Colouring = [
        wa-WA, nt-NT, q-Q, nsw-NSW, v-V, sa-SA, t-T
    ],
    Colours = [WA, NT, Q, NSW, V, SA, T],
    Colours ins 1..3,

    % Adjacency constraints: neighbouring regions must differ.
    WA #\= NT, WA #\= SA,
    NT #\= Q,  NT #\= SA,
    Q  #\= NSW, Q  #\= SA,
    NSW #\= V, NSW #\= SA,
    V #\= SA,

    label(Colours).

% colour_name(+Code, -Name)
colour_name(1, red).
colour_name(2, green).
colour_name(3, blue).

% print_solution(+Colouring)
print_solution(Colouring) :-
    write('Australia Map Colouring Solution:'), nl,
    forall(
        member(Region-Code, Colouring),
        ( colour_name(Code, Name),
          format('  ~w = ~w~n', [Region, Name]) )
    ).

% all_solutions(-Solutions)
all_solutions(Solutions) :-
    findall(Colouring, solution(Colouring), Solutions).
