in_room(bananas).
in_room(chair).
in_room(monkey).

dexterous(monkey).
tall(chair).

can_move(monkey, chair, bananas).
can_climb(monkey, chair).

can_reach(X,Y) :-
    dexterous(X),
    near(X,Y).

near(X,Z) :-
    get_on(X,Y),
    under(Y,Z),
    tall(Y).

get_on(X,Y) :-
    can_climb(X,Y).

under(Y,Z) :-
    in_room(X),
    in_room(Y),
    in_room(Z),
    can_move(X,Y,Z).