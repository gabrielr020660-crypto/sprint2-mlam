# -*- coding: utf-8 -*-
# Challenge Sprint 2 - FIAP / MLAM (Modelagem Linear para Aprendizado de Maquina)
# Base: Brazilian E-Commerce Public Dataset by Olist (Kaggle)
#
# Integrantes:
#   - Gustavo Guedes Pereira - 569779
#   - Lucas Angelo Colesanti - 569330
#   - Gustavo de Souza Correa - 570746
#   - Arthur Tae Gun Yong - 570647
#   - Murillo Boyadjian Guimaraes - 570774
#   - Gabriel Rodrigues - 569322
#
# O script monta a base, gera os 4 graficos (Item 01) e as 2 analises
# univariadas (Item 02). Usa apenas pandas, numpy e matplotlib.

import sys
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # salva os graficos em arquivo, sem abrir janela
import matplotlib.pyplot as plt

# faz o "R$" aparecer como texto normal (nao como formula matematica)
plt.rcParams["text.parse_math"] = False

# permite acentos nos prints do console do Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# pasta deste script, usada para ler e salvar os arquivos
PASTA = os.path.dirname(os.path.abspath(__file__))
PASTA_GRAFICOS = os.path.join(PASTA, "graficos")   # imagens dos graficos
PASTA_DATASET = os.path.join(PASTA, "dataset")      # CSVs (originais + base tratada)
os.makedirs(PASTA_GRAFICOS, exist_ok=True)
os.makedirs(PASTA_DATASET, exist_ok=True)


def caminho(*partes):
    return os.path.join(PASTA, *partes)


def dados(nome):
    # caminho de um arquivo dentro da pasta dataset/
    return os.path.join(PASTA_DATASET, nome)


# 1. Montagem da base
def montar_base():
    print("1. Montando a base")

    # le cada arquivo pelo nome correto (correcao do bug da Sprint 1)
    orders = pd.read_csv(dados("olist_orders_dataset.csv"))
    items = pd.read_csv(dados("olist_order_items_dataset.csv"))
    reviews = pd.read_csv(dados("olist_order_reviews_dataset.csv"))

    # confere se cada arquivo tem a coluna do seu conteudo
    assert "price" in items.columns, "items deve conter 'price'"
    assert "review_score" in reviews.columns, "reviews deve conter 'review_score'"
    assert "order_status" in orders.columns, "orders deve conter 'order_status'"

    # junta items + reviews (inner) e depois + orders (left), tudo por order_id
    base = items.merge(reviews, on="order_id", how="inner")
    base = base.merge(orders, on="order_id", how="left")

    # mantem so as colunas usadas, limpa e cria a faixa de preco em 3 grupos
    base = base[["order_status", "review_score", "order_item_id",
                 "price", "freight_value"]].copy()
    base = base.dropna(subset=["price", "review_score"])
    base["review_score"] = base["review_score"].astype(int)
    base["faixa_preco"] = pd.qcut(base["price"], q=3,
                                  labels=["Baixo", "Medio", "Alto"])

    base.to_csv(dados("base_olist_tratada.csv"), index=False, encoding="utf-8")
    print("\tBase final:", base.shape, "salva em dataset/base_olist_tratada.csv")
    return base


# 2. Graficos - Item 01 (cada grafico usa uma variavel diferente)
def gerar_graficos(base):
    print("2. Gerando graficos (Item 01)")

    # a) Setores (pizza) - order_status
    status = base["order_status"].value_counts()
    perc = status / status.sum() * 100
    cores = plt.cm.Set3(np.linspace(0, 1, len(status)))

    # mostra o percentual so nas fatias grandes; as pequenas ficam na legenda
    def rotulo_pct(valor):
        return ("%1.1f%%" % valor) if valor >= 1.0 else ""

    legenda = ["{} - {:.2f}%".format(nome, p) for nome, p in perc.items()]
    plt.figure(figsize=(8, 6))
    plt.pie(status.values, autopct=rotulo_pct, startangle=90,
            colors=cores, pctdistance=0.75)
    plt.title("Distribuicao dos Pedidos por Status (order_status)")
    plt.legend(legenda, title="Status do pedido", loc="center left",
               bbox_to_anchor=(1.0, 0.5))
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig(os.path.join(PASTA_GRAFICOS, "g1_setores_status.png"),
                dpi=120, bbox_inches="tight")
    plt.close()
    print("\tg1_setores_status.png")

    # b) Barras - review_score
    notas = base["review_score"].value_counts().sort_index()
    plt.figure(figsize=(8, 6))
    plt.bar(notas.index.astype(str), notas.values, color="#4C72B0",
            label="Quantidade de avaliacoes")
    plt.title("Quantidade de Avaliacoes por Nota (review_score)")
    plt.xlabel("Nota da avaliacao (1 a 5)")
    plt.ylabel("Quantidade de pedidos")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(PASTA_GRAFICOS, "g2_barras_review.png"), dpi=120)
    plt.close()
    print("\tg2_barras_review.png")

    # c) Histograma - price (eixo limitado a R$500 por causa dos outliers)
    limite_x = 500
    acima = (base["price"] > limite_x).mean() * 100
    plt.figure(figsize=(8, 6))
    plt.hist(base["price"], bins=50, range=(0, limite_x),
             color="#55A868", edgecolor="black")
    plt.title("Distribuicao do Preco dos Itens (price)")
    plt.xlabel("Preco (R$) - eixo limitado a R$500 para leitura")
    plt.ylabel("Frequencia")
    plt.annotate("{:.1f}% dos itens custam acima de R$500".format(acima),
                 xy=(0.97, 0.85), xycoords="axes fraction", ha="right",
                 fontsize=9, color="gray")
    plt.tight_layout()
    plt.savefig(os.path.join(PASTA_GRAFICOS, "g3_histograma_price.png"), dpi=120)
    plt.close()
    print("\tg3_histograma_price.png")

    # d) Boxplot - freight_value
    plt.figure(figsize=(8, 6))
    caixa = plt.boxplot(base["freight_value"], patch_artist=True,
                        tick_labels=["freight_value"])
    caixa["boxes"][0].set_facecolor("#C44E52")
    plt.title("Boxplot do Valor do Frete (freight_value)")
    plt.xlabel("Variavel")
    plt.ylabel("Valor do frete (R$)")
    plt.tight_layout()
    plt.savefig(os.path.join(PASTA_GRAFICOS, "g4_boxplot_frete.png"), dpi=120)
    plt.close()
    print("\tg4_boxplot_frete.png")


# 3. Estatistica - Item 02 (analise univariada de uma variavel)
def analise_univariada(serie, nome):
    serie = serie.dropna()

    # a) tendencia central
    media = serie.mean()
    mediana = serie.median()
    moda = serie.mode()  # em variavel continua pode haver varios valores

    # b) dispersao
    amplitude = serie.max() - serie.min()
    variancia = serie.var()
    desvio = serie.std()
    coef_var = desvio / media * 100

    # c) separatrizes
    q1, q2, q3 = serie.quantile([0.25, 0.50, 0.75])
    d1, d9 = serie.quantile([0.10, 0.90])
    p95 = serie.quantile(0.95)

    # texto da moda (resume quando ha muitos valores empatados)
    if len(moda) <= 5:
        moda_txt = ", ".join("{:.2f}".format(v) for v in moda)
    else:
        moda_txt = "{} valores empatados; primeiros: {}".format(
            len(moda), ", ".join("{:.2f}".format(v) for v in moda[:5]))

    print("Analise univariada: " + nome)
    print("N (observacoes): {}".format(len(serie)))
    print("a) Tendencia central")
    print("\tMedia  : {:.2f}".format(media))
    print("\tMediana: {:.2f}".format(mediana))
    print("\tModa   : {}".format(moda_txt))
    print("b) Dispersao")
    print("\tAmplitude        : {:.2f}".format(amplitude))
    print("\tVariancia        : {:.2f}".format(variancia))
    print("\tDesvio padrao    : {:.2f}".format(desvio))
    print("\tCoef. de variacao: {:.2f}%".format(coef_var))
    print("c) Separatrizes")
    print("\tQ1 (25%): {:.2f}".format(q1))
    print("\tQ2 (50%): {:.2f}".format(q2))
    print("\tQ3 (75%): {:.2f}".format(q3))
    print("\tD1 (10%): {:.2f}".format(d1))
    print("\tD9 (90%): {:.2f}".format(d9))
    print("\tP95     : {:.2f}".format(p95))
    print("")


def gerar_estatistica(base):
    print("3. Estatistica descritiva (Item 02)")
    print("")
    analise_univariada(base["price"], "price (preco do item, R$)")
    analise_univariada(base["freight_value"], "freight_value (valor do frete, R$)")


def main():
    base = montar_base()
    gerar_graficos(base)
    gerar_estatistica(base)
    print("Concluido.")


if __name__ == "__main__":
    main()
