%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Dictionary
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


:- [skladnicaTagsBases].
:- [walenty_subst].

hasTag(Word, Tag) :- tagAndBase(Word,_Base,Tag).
hasTag(w, prep:loc).
hasTag(ze, prep:loc).
hasTag(z, prep:loc).
hasTag(z, prep:gen).
hasTag(ze, prep:gen).
hasTag(dla, prep:gen).
hasBase(Word, Base) :- tagAndBase(Word,Base,_Tag).
 
:- op(1050, xfx, ==>).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% GRAMMAR
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


likeAdj(adj:L:P:R:_, L, P, R).
likeAdj(ppas:L:P:R:_, L, P, R).
%likeAdj(num:L:P:R:_, L, P, R).
likeAdj(pact:L:P:R:_:_, L, P, R).
likeAdj(ppron3:pl:gen:f:_:_:npraep, pl, gen, f).

whatever([A]) ==> [A], {not(hasTag(A, interp))}.
whatever([A|As]) ==> [A], whatever(As), {not(hasTag(A, interp))}.

np(L,P,R,As) ==> adj(L,P,R,As1), np(L,P,R,As2), append(As1, As2, As).

npFirst(L,P,R,[A|As]) ==> [X], npFirst(L,P,R,As), {hasBase(X,B), tagAndBase(A,B,adj:sg:nom:R:_)}.

np(L,P,R,As) ==> np(L,P,R,As1), adj(L,P,R,As2), append(As1,As2,As).

npFirst(L,P,R,As) ==> npFirst(L,P,R,As1), [X], append(As1, [A], As), {hasBase(X,B), tagAndBase(A,B,adj:sg:nom:R:_)}.


np(L,P,R,As) ==> np(L,P,R,As1), preph(As2), append(As1,As2,As).

npFirst(L,P,R,As) ==> npFirst(L,P,R,As1), preph(As2), append(As1,As2,As).

np(L,P,R,As) ==> np(L,P,R,As1), np(_,gen,_,As2), append(As1,As2,As).

npFirst(L,P,R,As) ==> npFirst(L,P,R,As1), np(_,gen,_,As2), append(As1,As2,As).

np(pl,P,R1,As) ==> np(_,P,R1,As1), [i], np(_,P,_R2,As2), append(As1,['i'|As2],As).

npFirst(pl,P,R1,As) ==>  np(_,P,R1,As1), [i], np(_,P,_R2,As2), append(As1,['i'|As2],As).

np(L,P,R,[X]) ==> [X], {hasTag(X,subst:L:P:R)}.

npFirst(L,P,R,[B]) ==> [X], {hasTag(X,subst:L:P:R), hasBase(X,B)}.

np(L,P,R,[X]) ==> [X], {hasTag(X,ger:L:P:R:_:_)}.

npFirst(L,P,R,[B]) ==> [X], {hasTag(X,ger:L:P:R:_:_), hasBase(X,B)}.

np(L,P,R,[X|[PRZY|As]]) ==> [X], [PRZY], np(_,P1,_,As), {hasTag(X,subst:L:P:R), hasBase(X,B), 
walenty(B,PRZY,P1)}.

npFirst(L,P,R,[B|[PRZY|As]]) ==> [X], [PRZY], np(_,P1,_,As), {hasBase(X,B), hasTag(X,subst:L:P:R), 
walenty(B,PRZY,P1)}.

%np(L,P,R,[A1|[A2|[PRZY|As]]]) ==> adj(L,P,R), [X], [PRZY], np(_,P1,_), {hasTag(X,subst:P:L:R), 
%hasBase(X,B), walenty(B,PRZY,P1)}.
%np(L,P,R) ==> [X], adj(L,P,R), [PRZY], np(_,P1,_), {hasTag(X,subst:P:L:R), 
%hasBase(X,B), walenty(B,PRZY,P1)}.

np(L,P,R,As) ==> np(L,P,R,As1), [','], [X], whatever(As2), [Z], append(As1, [','|[X|As2]], As3), append(As3, [Z],As),  {hasBase(X,'który'), 
hasTag(Z,interp)}.

npFirst(L,P,R,As) ==> npFirst(L,P,R,As1), [','], [X], whatever(As2), [Z], append(As1, [','|[X|As2]], As3), append(As3, [Z],As),  {hasBase(X,'który'),
hasTag(Z,interp)}.

%np(L,P,R) ==> np(L,P,R), [','], [PRZY], [X], whatever, [Z], 
%{hasTag(PRZY, prep:_:_), hasBase(X,'który'), hasTag(Z,interp)}.
%np(L,P,R) ==> np(L,P,R), [','], [PRZY], [X], whatever, [Z], 
%{hasTag(PRZY, prep:_), hasBase(X,'który'), hasTag(Z,interp)}.

adj(L,P,R,[X]) ==> [X], {hasTag(X, Tag), likeAdj(Tag,L,P,R)}.
adj(L,P,R,[X,Y]) ==> [X], [Y], {hasTag(X, TagX), likeAdj(TagX,L,P,R), hasTag(Y,TagY), 
likeAdj(TagY,L,P,R)}.
adj(L,P,R,[X,'-',Y]) ==> [X], [-], [Y], {hasTag(Y, TagY), likeAdj(TagY,L,P,R), 
hasTag(X, adja)}.
adj(L,P,R,['aż',X]) ==> [aż], [X], {hasTag(X, Tag), likeAdj(Tag,L,P,R)}.
adj(L,P,R,[X,Y]) ==> [X], [Y], {hasTag(X,adv:pos), hasTag(Y,ppas:L:P:R:_)}.
preph([X|As]) ==> [X], np(_,loc,_,As), {hasTag(X,prep:loc)}. 
preph([X|As]) ==> [X], np(_,gen,_,As), {hasTag(X,prep:gen)}. 


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
   analyze(L,Res),
   writeUnique(L,Res),
   L == end_of_file, !.

writeUnique([X|Y], []) :- write('[!]'), writeList([X|Y]),nl,!.
writeUnique(L,Res) :- makeUnique(L,Res,[],Res2), writeAll(L,Res2), !.

makeUnique(L,[X|Res],Z,Res2) :- member(X, Res), makeUnique(L,Res,Z,Res2), !.
makeUnique(L,[X|Res],Z,Res2) :- Z1 = [X|Z], makeUnique(L, Res, Z1, Res2), !.
makeUnique(_,[],Z,Res2) :- Res2 = Z, !.

writeAll(L, [X]) :- write('[]'), writeList(L), nl, writeList(X),nl,!.
writeAll(L, [X|Xs]) :- write('[*]'), writeList(L), nl, writeTable([X|Xs]).

writeTable([X|Res]) :- writeList(X),nl, writeTable(Res).

analyze(L,Res) :-   
   length(L,N),
   N < 7,
   findall(X, parse(npFirst(_,_,_,X), L), Res),
   !.
   %write('GOOD:'),
   %writeList(L), nl,writeList(X),nl.
   %analyze(L,_) :-
   %write('[!]'), writeList(L),nl,!.


:- parse0.
