# Knowledge Engine - Análise de Filmes com Prolog

## Descrição do Projeto

Este projeto implementa um **mecanismo de busca usando Lógica de Primeira Ordem** com Prolog, baseado em um dataset de filmes de cinema. O sistema permite realizar consultas sofisticadas sobre filmes, como rankings por avaliação, análise de lucratividade e retorno sobre investimento.

## Dataset

**Fonte:** TMDB 5000 Movies (Kaggle)  
**Tema:** Filmes de cinema com informações financeiras e de avaliação  
**Filtro:** Filmes com orçamento e bilheteria informados

## Estrutura do Banco de Conhecimento

Predicado principal: `filme(titulo, genero, ano, duracao_min, nota, bilheteria, orcamento, idioma)`

### Exemplos de Predicados

```prolog
filme(avatar, action, 2009, 162, 7.2, 2787965087, 237000000, ingles).
filme(titanic, drama, 1997, 194, 7.5, 1845034188, 200000000, ingles).
filme(the_avengers, science_fiction, 2012, 143, 7.4, 1519557910, 220000000, ingles).
```

**Campos:**
- **titulo**: Nome do filme (normalizado)
- **genero**: Primeiro gênero listado no dataset
- **ano**: Ano de lançamento
- **duracao_min**: Duração em minutos
- **nota**: Avaliação do público (0.0 a 10.0)
- **bilheteria**: Receita bruta em USD
- **orcamento**: Custo de produção em USD
- **idioma**: Idioma original (código ISO normalizado)

## Como Usar

### 1. Gerar a Base de Conhecimento

```bash
python projeto.py
```

**O que faz:**
- Lê o arquivo `tmdb_5000_movies.csv`
- Normaliza títulos, gêneros e idiomas para formato válido em Prolog
- Extrai 8 campos por filme
- Gera `filmes.pl` com todos os predicados

**Output esperado:**
```
4818 filmes carregados.
Base gerada: filmes.pl
4818 predicados escritos | 0 registros ignorados
```

### 2. Testar as Queries em Prolog

Acesse [SWISH - Online Prolog](https://swish.swi-prolog.org/):

1. Crie um novo notebook
2. Cole todo o conteúdo de `filmes.pl` na área **Program**
3. Cole todo o conteúdo de `queries.pl` na área **Program**
4. Use as queries abaixo na área **Query**

## Perguntas e Queries

### Pergunta 1: Qual gênero tem a maior média de avaliação?

**Tipo:** Sofisticada (agregação com findall + cálculo de média)

```prolog
?- ranking_generos(R).
```

**Resultado esperado:** Ranking dos gêneros pela nota média

```prolog
R = [8.3-science_fiction, 7.9-animation, 7.6-drama, 7.4-adventure, ...]
```

**Conceitos utilizados:**
- `findall/3` para coletar todas as notas de um gênero
- `sum_list/2` para somar notas
- `setof/3` para criar conjunto ordenado
- `reverse/2` para inverter ordem crescente → decrescente

---

### Pergunta 2: Quais filmes tiveram o maior lucro bruto?

**Tipo:** Sofisticada (cálculo aritmético + ranking)

```prolog
?- filmes_mais_lucrativos(R).
```

**Resultado esperado:** Top 10 filmes por lucro bruto (bilheteria - orçamento)

```prolog
R = [2550965087-avatar, 1645034188-titanic, 1285557910-the_avengers, ...]
```

**Conceitos utilizados:**
- Filtros com `>` (bilheteria e orçamento > 0)
- Aritmética com `is`
- `setof/3` para ordenação
- `reverse/2` para ranking decrescente

---

### Pergunta 3: Qual idioma concentra os filmes mais bem avaliados em média?

**Tipo:** Sofisticada (agregação com filtro de quantidade mínima)

```prolog
?- ranking_idiomas(R).
```

**Resultado esperado:** Ranking de idiomas por nota média (apenas idiomas com ≥5 filmes)

```prolog
R = [7.6-ingles, 7.2-frances, 7.0-espanhol, ...]
```

**Conceitos utilizados:**
- `findall/3` para coletar dados
- `length/2` para filtrar por quantidade mínima
- Cálculo de média
- `setof/3` com padrão complexo
- `reverse/2` para ordenação decrescente

---

### Pergunta 4: Quais filmes tiveram o maior retorno percentual sobre investimento (ROI)?

**Tipo:** Sofisticada (cálculo de percentual + ranking)

```prolog
?- ranking_roi(R).
```

**Resultado esperado:** Top filmes por ROI percentual

```prolog
R = [1076-avatar, 822-titanic, 584-the_avengers, ...]
```

**Conceitos utilizados:**
- Aritmética com operador `//` (divisão inteira)
- Operação percentual `* 100 // Orcamento`
- `setof/3` para ranking
- `reverse/2` para inversão de ordem

---

## Sentenças Auxiliares Definidas

```prolog
% Unários que verificam existência de cada entidade
titulo(T)  :- filme(T, _, _, _, _, _, _, _).
genero(G)  :- filme(_, G, _, _, _, _, _, _).
idioma(I)  :- filme(_, _, _, _, _, _, _, I).

% Predicados derivados para lucro e ROI
lucro(Titulo, Lucro) :- ...
roi(Titulo, ROI) :- ...
```

## Técnicas de Lógica Implementadas

| Técnica | Exemplo | Pergunta |
|---------|---------|----------|
| **Pattern Matching** | `filme(T, genero, _, _, _, _, _, _)` | Filtro básico |
| **Unificação com restrição** | `filme(_, G, _, _, N, _, _, _), N > 7` | Filtro com condição |
| **Agregação com findall** | `findall(N, ..., Lista)` | Pergunta 1, 3 |
| **Cálculo aritmético** | `Lucro is Bilheteria - Orcamento` | Pergunta 2, 4 |
| **Ordenação com setof** | `setof(Media-Genero, ..., Lista)` | Ranking |
| **Inversão com reverse** | `reverse(ListaOrd, Tabela)` | Ranking decrescente |
| **Composição de regras** | `media_nota_genero :- notas_do_genero, sum_list, ...` | Perguntas 1-3 |

## Estrutura de Arquivos

```
Projeto-Knowledge-Engine-Adrielle/
│
├── projeto.py              # ETL: CSV → Prolog
├── filmes.pl               # Base de conhecimento (4818 predicados)
├── queries.pl              # Sentenças e perguntas
├── tmdb_5000_movies.csv    # Dataset original
├── data.py                 # Exploração inicial (auxiliar)
├── README.md               # Este arquivo
├── enunciado.txt           # Descrição do projeto
└── exemplo.pl              # Exemplo do tutorial (referência)
```

## Requisitos do Projeto

 **Entrega Individual** - Dataset e implementação único  
 **Dataset Diferenciado** - Filmes (não o exemplo de futebol)  
 **ETL em Python** - Normalização e geração de base  
 **Base de Conhecimento** - 4818 predicados em Prolog  
 **Pelo menos 3 Perguntas** - 4 perguntas sofisticadas implementadas  
 **Queries em Prolog** - Sentenças com agregação e cálculo  
 **README** - Documentação completa do projeto  


## Referências

- [SWISH - Prolog Online](https://swish.swi-prolog.org/)
- [SWI-Prolog Documentation](https://www.swi-prolog.org/pldoc/doc_for?object=manual)
- [TMDB 5000 Movies - Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

---

**Autor:** Adrielle  
**Disciplina:** Lógica e Matemática Discreta  
**Professor:** Raul Ikeda
