% ── SENTENÇAS ─────────────────────────────────────────────────────────────────

% Auxiliares
titulo(T)  :- filme(T, _, _, _, _, _, _, _).
genero(G)  :- filme(_, G, _, _, _, _, _, _).
idioma(I)  :- filme(_, _, _, _, _, _, _, I).

% ── Pergunta 1: Ranking de gêneros por média de nota ─────────────────────────
% "Qual gênero tem a maior média de avaliação?"

notas_do_genero(Genero, Lista) :-
    genero(Genero),
    findall(N, filme(_, Genero, _, _, N, _, _, _), Lista).

media_nota_genero(Genero, Media) :-
    notas_do_genero(Genero, Lista),
    Lista \= [],
    length(Lista, Qtd),
    sum_list(Lista, Soma),
    Media is Soma / Qtd.

ranking_generos(Ranking) :-
    setof(Media-Genero, media_nota_genero(Genero, Media), Lista),
    reverse(Lista, Ranking).

% ── Pergunta 2: Filmes mais lucrativos ────────────────────────────────────────
% "Quais filmes tiveram o maior lucro bruto (bilheteria - orçamento)?"

lucro(Titulo, Lucro) :-
    filme(Titulo, _, _, _, _, Bilheteria, Orcamento, _),
    Bilheteria > 0,
    Orcamento  > 0,
    Lucro is Bilheteria - Orcamento.

filmes_mais_lucrativos(Ranking) :-
    setof(Lucro-Titulo, lucro(Titulo, Lucro), Lista),
    reverse(Lista, Ranking).

% ── Pergunta 3: Ranking de idiomas por média de nota ─────────────────────────
% "Qual idioma concentra os filmes mais bem avaliados em média?"

notas_do_idioma(Idioma, Lista) :-
    idioma(Idioma),
    findall(N, filme(_, _, _, _, N, _, _, Idioma), Lista),
    length(Lista, Qtd), Qtd >= 5.

media_nota_idioma(Idioma, Media) :-
    notas_do_idioma(Idioma, Lista),
    length(Lista, Qtd),
    sum_list(Lista, Soma),
    Media is Soma / Qtd.

ranking_idiomas(Ranking) :-
    setof(Media-Idioma, media_nota_idioma(Idioma, Media), Lista),
    reverse(Lista, Ranking).

% ── Pergunta 4: ROI — retorno sobre investimento ──────────────────────────────
% "Quais filmes tiveram o maior retorno percentual sobre o orçamento?"

roi(Titulo, ROI) :-
    filme(Titulo, _, _, _, _, Bilheteria, Orcamento, _),
    Orcamento  > 0,
    Bilheteria > 0,
    ROI is (Bilheteria - Orcamento) * 100 // Orcamento.

ranking_roi(Ranking) :-
    setof(ROI-Titulo, roi(Titulo, ROI), Lista),
    reverse(Lista, Ranking).


% ── QUERIES ───────────────────────────────────────────────────────────────────
%
% Pergunta 1 — Ranking de gêneros por média de nota:
%   ?- ranking_generos(R).
%
% Pergunta 2 — Filmes mais lucrativos:
%   ?- filmes_mais_lucrativos(R).
%
% Pergunta 3 — Ranking de idiomas por média de nota:
%   ?- ranking_idiomas(R).
%
% Pergunta 4 — Ranking por ROI (%):
%   ?- ranking_roi(R).
%
% Filtros básicos:
%   ?- filme(T, action, _, _, N, _, _, _), N > 8.0.
%   ?- filme(T, _, Ano, _, _, B, _, _), Ano > 2010, B > 1000000000.