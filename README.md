# Challenge Sprint 2 - Modelagem Linear para Aprendizado de Maquina (MLAM)

## Integrantes
- Gustavo Guedes Pereira - 569779
- Lucas Angelo Colesanti - 569330
- Gustavo de Souza Correa - 570746
- Arthur Tae Gun Yong - 570647
- Murillo Boyadjian Guimarães - 570774
- Gabriel Rodrigues - 569322

---

## 1. Introducao

Este repositorio entrega a Sprint 2 da disciplina de Modelagem Linear para
Aprendizado de Maquina, dando continuidade a Sprint 1. O objetivo e aplicar
analise grafica e estatistica descritiva sobre dados reais de e-commerce
brasileiro, transformando os numeros em insights que apoiem a tomada de decisao
da empresa.

O trabalho cobre tres itens:

- **Item 01:** quatro graficos em Python, cada um com uma variavel diferente.
- **Item 02:** duas analises univariadas completas (tendencia central, dispersao
  e separatrizes).
- **Item 03:** este relatorio tecnico, ligando os resultados a geracao de valor.

---

## 2. Base de dados

Utilizamos o **Brazilian E-Commerce Public Dataset by Olist** (Kaggle). A base
final foi montada a partir de tres arquivos originais, unidos pela chave
`order_id`:

- `olist_order_items_dataset.csv` (itens dos pedidos: preco e frete)
- `olist_order_reviews_dataset.csv` (notas de avaliacao)
- `olist_orders_dataset.csv` (status dos pedidos)

A juncao foi feita com `items + reviews` (inner) e depois `+ orders` (left),
todos por `order_id`. Em seguida foram removidas as linhas sem `price` ou sem
`review_score` e criada a variavel `faixa_preco` por tercis (`pd.qcut`, q=3).

> Correcao da Sprint 1: na leitura dos CSVs os arquivos haviam sido associados a
> conteudos trocados. Nesta versao cada arquivo e lido pelo nome correto e o
> codigo valida (via `assert`) que `price`, `review_score` e `order_status`
> estao em seus respectivos arquivos.

A base tratada (`dataset/base_olist_tratada.csv`) ficou com **112.372 linhas** e
6 colunas. Os CSVs (base tratada + os 3 originais) ficam na pasta `dataset/`.

### Variaveis da base tratada

| Variavel       | Tipo                              | Descricao                          |
|----------------|-----------------------------------|------------------------------------|
| order_status   | qualitativa nominal               | situacao do pedido                 |
| review_score   | ordinal / quantitativa discreta   | nota da avaliacao (1 a 5)          |
| faixa_preco    | ordinal (Baixo / Medio / Alto)    | tercil do preco do item            |
| order_item_id  | quantitativa discreta             | numero do item dentro do pedido    |
| price          | quantitativa continua             | preco do item (R$)                 |
| freight_value  | quantitativa continua             | valor do frete (R$)                |

---

## 3. Item 01 - Graficos

Os quatro graficos estao na pasta [`graficos/`](graficos/). Cada um usa uma
variavel diferente.

### a) Grafico de setores (pizza) - `order_status`
Arquivo: `graficos/g1_setores_status.png`

Mostra a distribuicao percentual dos pedidos por status. O resultado e
fortemente concentrado: **delivered (entregue) = 97,90%**. Os demais status sao
residuais: shipped 0,99%, canceled 0,47%, invoiced 0,32%, processing 0,31%,
unavailable 0,01% e approved 0,00%. Como as fatias pequenas ficariam ilegiveis,
seus percentuais foram detalhados na legenda.

### b) Grafico de barras - `review_score`
Arquivo: `graficos/g2_barras_review.png`

Mostra a quantidade de avaliacoes por nota (1 a 5). Predominam as notas altas:
nota 5 = 56,53% e nota 4 = 18,97% (juntas, mais de 75% das avaliacoes). Chama a
atencao a nota 1, com 12,67% - maior que as notas 2 e 3 somadas, indicando um
padrao de avaliacao polarizado (ou muito satisfeito, ou muito insatisfeito).

### c) Histograma - `price`
Arquivo: `graficos/g3_histograma_price.png`

Mostra a distribuicao do preco dos itens. A distribuicao e fortemente
assimetrica a direita: a grande maioria dos itens custa pouco e existe uma cauda
longa de produtos caros. Para a leitura ficar clara, o eixo X foi limitado a
R$500 (cobre ~97% dos itens); 2,8% dos itens custam acima desse valor e foram
sinalizados no grafico.

### d) Boxplot - `freight_value`
Arquivo: `graficos/g4_boxplot_frete.png`

Mostra a dispersao do valor do frete. A caixa (50% centrais) e estreita, mas ha
muitos pontos acima do limite superior, ou seja, varios fretes atipicamente
altos (outliers) puxados por entregas mais caras / distantes.

---

## 4. Item 02 - Analises univariadas

Calculadas no codigo e exibidas no console ao rodar `sprint2_mlam.py`.

### Univariada 1 - `price` (preco do item, R$) | N = 112.372

| Grupo                | Medida              | Valor       |
|----------------------|---------------------|-------------|
| Tendencia central    | Media               | 120,38      |
|                      | Mediana             | 74,90       |
|                      | Moda                | 59,90       |
| Dispersao            | Amplitude           | 6.734,15    |
|                      | Variancia           | 33.179,49   |
|                      | Desvio padrao       | 182,15      |
|                      | Coef. de variacao   | 151,32%     |
| Separatrizes         | Q1 (25%)            | 39,90       |
|                      | Q2 (50%)            | 74,90       |
|                      | Q3 (75%)            | 134,90      |
|                      | D1 (10%)            | 23,89       |
|                      | D9 (90%)            | 229,04      |
|                      | P95                 | 349,90      |

**Leitura:** a media (120,38) e bem maior que a mediana (74,90), confirmando a
assimetria a direita vista no histograma - alguns itens muito caros elevam a
media. O coeficiente de variacao de 151,32% indica dispersao altissima: os
precos sao muito heterogeneos. Metade dos itens custa entre R$39,90 (Q1) e
R$134,90 (Q3).

### Univariada 2 - `freight_value` (valor do frete, R$) | N = 112.372

| Grupo                | Medida              | Valor       |
|----------------------|---------------------|-------------|
| Tendencia central    | Media               | 19,98       |
|                      | Mediana             | 16,25       |
|                      | Moda                | 15,10       |
| Dispersao            | Amplitude           | 409,68      |
|                      | Variancia           | 249,05      |
|                      | Desvio padrao       | 15,78       |
|                      | Coef. de variacao   | 78,99%      |
| Separatrizes         | Q1 (25%)            | 13,07       |
|                      | Q2 (50%)            | 16,25       |
|                      | Q3 (75%)            | 21,15       |
|                      | D1 (10%)            | 8,74        |
|                      | D9 (90%)            | 34,04       |
|                      | P95                 | 45,12       |

**Leitura:** o frete e bem mais comportado que o preco. A media (19,98) e
proxima da mediana (16,25) e o coeficiente de variacao (78,99%) e cerca de
metade do observado em `price`. Ainda assim ha cauda a direita: 10% dos fretes
passam de R$34,04 (D9) e 5% passam de R$45,12 (P95), coerente com os outliers do
boxplot.

---

## 5. Item 03 - Insights e geracao de valor

**1. Operacao logistica saudavel, mas com pontos a monitorar.**
Com 97,90% dos pedidos entregues, a operacao de entrega e eficiente. Os ~2% em
status como canceled, unavailable e processing sao pequenos em volume, mas valem
acompanhamento porque costumam concentrar reclamacoes e custo de reprocessamento.

**2. Satisfacao alta, porem polarizada.**
Mais de 75% das avaliacoes sao 4 ou 5, o que sustenta a reputacao da plataforma.
Mas os 12,67% de nota 1 sao um sinal de alerta: cruzar essas avaliacoes com
status do pedido e valor do frete ajuda a identificar se a insatisfacao vem de
atraso, cancelamento ou frete caro - e atacar a causa raiz.

**3. Catalogo de baixo ticket com cauda premium.**
A mediana de preco de R$74,90 mostra um catalogo predominantemente de baixo
ticket, mas a cauda longa (ate R$6.734) revela um nicho premium. A faixa_preco
em tercis permite politicas diferentes por segmento: promocao e volume nos itens
"Baixo" e foco em margem / atendimento diferenciado nos itens "Alto".

**4. Frete como alavanca competitiva.**
O frete tem dispersao relevante (CV 78,99%) e outliers acima de R$45. Como o
frete pesa mais sobre itens baratos (maioria do catalogo), renegociar tabelas de
transporte ou oferecer frete subsidiado nas faixas de menor preco pode aumentar
conversao sem corroer a margem dos itens premium.

**Resumo do valor gerado:** as analises permitem priorizar onde agir -
reduzir cancelamentos, atacar a causa das notas baixas, segmentar o catalogo por
faixa de preco e usar o frete como ferramenta de conversao. Tudo a partir de
medidas simples (media, mediana, dispersao e quartis) aplicadas a dados reais.

---

## 6. Conclusao

A Sprint 2 mostrou que estatistica descritiva basica, bem aplicada, ja entrega
direcionamento de negocio. As variaveis continuas (`price` e `freight_value`)
revelaram distribuicoes assimetricas com outliers, enquanto as qualitativas
(`order_status`, `review_score`) descreveram a saude operacional e a satisfacao
do cliente. O conjunto desses indicadores forma uma base solida para as proximas
etapas de modelagem.

---

## 7. Estrutura do repositorio

```
mlam_sprint2_fix/
├── sprint2_mlam.py            # codigo unico (base + graficos + estatistica)
├── README.md                  # este relatorio tecnico
├── dataset/
│   ├── base_olist_tratada.csv        # base oficial tratada
│   ├── olist_orders_dataset.csv      # CSVs originais da Olist
│   ├── olist_order_items_dataset.csv
│   └── olist_order_reviews_dataset.csv
└── graficos/
    ├── g1_setores_status.png
    ├── g2_barras_review.png
    ├── g3_histograma_price.png
    └── g4_boxplot_frete.png
```

## 8. Como executar

Requisitos: Python 3 com `pandas`, `numpy` e `matplotlib`.

```
pip install pandas numpy matplotlib
python sprint2_mlam.py
```

O script le os 3 CSVs originais da Olist (na pasta `dataset/`), gera a base
tratada em `dataset/` e os 4 graficos em `graficos/`, e imprime as estatisticas
do Item 02 no console.
