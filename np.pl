%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Dictionary
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


:- [skladnicaTagsBases].

hasTag(Word, Tag) :- tagAndBase(Word,_Base,Tag).
hasTag(w, prep:loc).
hasBase(Word, Base) :- tagAndBase(Word,Base,_Tag).
 
:- op(1050, xfx, ==>).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% GRAMMAR
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


likeAdj(adj:L:P:R:_, L, P, R).
likeAdj(ppas:L:P:R:_, L, P, R).
likeAdj(num:L:P:R:_, L, P, R).

whatever ==> [X], {not(hasTag(X, interp))}.
whatever ==> [X], whatever, {not(hasTag(X, interp))}.

np(L,P,R) ==> adj(L,P,R), np(L,P,R).
np(L,P,R) ==> np(L,P,R), adj(L,P,R).
np(L,P,R) ==> np(L,P,R), preph.
np(L,P,R) ==> np(L,P,R), np(_,gen,_).
np(pl,P,R1) ==> np(_,P,R1), [i], np(_,P,_R2).
np(pl,P,R1) ==> np(_,P,R1), [oraz], np(_,P,_R2).
np(L,P,R) ==> [X], {hasTag(X,subst:L:P:R)}.
np(L,P,R) ==> [X], [Y], {hasTag(X,subst:L:P:R), hasTag(Y,subst:L:P:R)}.
np(L,P,R) ==> [X], {hasTag(X,ppron12:L:P:R:_)}.
np(L,P,R) ==> [X], {hasTag(X,ppron3:L:P:R:_)}.
np(L,P,R) ==> np(L,P,R), [','], [X], whatever, [Z], {hasBase(X,'który'), hasTag(Z,interp)}.

adj(L,P,R) ==> [X], {hasTag(X, Tag), likeAdj(Tag,L,P,R)}.
adj(L,P,R) ==> [aż], [X], {hasTag(X, Tag), likeAdj(Tag,L,P,R)}.
preph ==> [X], np(_,_,_), {hasTag(X,prep:_:_)}. 



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Parse
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
commasToList((X,Y), [X|Rest]) :- 
   !, commasToList(Y,Rest).
commasToList(X,[X]).   


allign( [[W]| Rest], [W|T], Alligment) :-
   !,allign(Rest, T, Alligment). 
allign( [At|Rest], Ts, [ (At,Pref) | ARest]):-
   Pref = [_|_],
   append(Pref, RestT, Ts),
   allign(Rest, RestT, ARest).
allign( [{C}], [], []) :- C.
allign( [], [], []).


   
parse(A,TokensToParse) :-
   (A ==> Right),
   commasToList(Right, ListRight),
   allign(ListRight, TokensToParse, Alligment),
   parsePairs(Alligment).
   
parsePairs([]).
parsePairs([(A,L)| Rest]):-
   parse(A,L),
   parsePairs(Rest).

writeList([A]) :- write(A),!.
writeList([A|As]):- write(A), write(' '),writeList(As).
   
parse0 :-
   see('phrases.pl'),
   parsing,
   seen.

parsing :-
   repeat,
   read(L),
   analyze(L),
   L = end_of_file,!.

analyze(L) :-   
   length(L,N),
   N < 7,
   parse(np(_,_,_), L),
   write('GOOD:'),
   writeList(L),nl,!.
analyze(L) :-
   write('BAD:'), writeList(L),nl,!.


:- parse0.
