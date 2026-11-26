"""Experimento: qual busca é mais rápida? E qual ordenação compara menos?

Para 100, 1.000 e 10.000 atendimentos fictícios:
- busca sequencial (lista sem ordem), busca binária (lista ordenada)
  e árvore binária de busca;
- 200 buscas em cada caso: metade de códigos que existem e metade que não.
Mede a média de comparações e o tempo médio de cada busca.

Depois conta as comparações dos três métodos de ordenação.
Resultados vão para resultados_busca.csv, resultados_ordenacao.csv
e o gráfico grafico_buscas.png.

Rodar com:  python experimento.py
"""

import csv
import math
import random
import time

from busca_ordenacao import (busca_sequencial, busca_binaria,
                             ordenar_bolha, ordenar_selecao, ordenar_insercao)
from estruturas import ArvoreBusca

VOLUMES = [100, 1000, 10000]
BUSCAS = 200
SEMENTE = 2026


def criar_registros(qtd, rnd):
    codigos = list(range(1001, 1001 + qtd))
    rnd.shuffle(codigos)  # chegam fora de ordem
    return [{"codigo": c, "duracao_min": rnd.randint(5, 120)} for c in codigos]


def medir(funcao, alvos):
    total_comp = 0
    inicio = time.perf_counter()
    for alvo in alvos:
        _, comp = funcao(alvo)
        total_comp += comp
    gasto = time.perf_counter() - inicio
    return total_comp / len(alvos), gasto / len(alvos) * 1_000_000  # microssegundos


def experimento_busca(rnd):
    linhas = []
    for qtd in VOLUMES:
        registros = criar_registros(qtd, rnd)
        ordenados, _ = ordenar_insercao(registros, "codigo")
        arvore = ArvoreBusca()
        for r in registros:  # ordem embaralhada deixa a árvore equilibrada
            arvore.inserir(r)
        existentes = [rnd.randint(1001, 1000 + qtd) for _ in range(BUSCAS // 2)]
        inexistentes = [rnd.randint(1001 + qtd, 2000 + 2 * qtd) for _ in range(BUSCAS // 2)]
        alvos = existentes + inexistentes

        testes = {
            "sequencial": lambda c: busca_sequencial(registros, c),
            "binária": lambda c: busca_binaria(ordenados, c),
            "árvore": lambda c: arvore.buscar(c),
        }
        for nome, funcao in testes.items():
            comp, micro = medir(funcao, alvos)
            linhas.append({"volume": qtd, "metodo": nome,
                           "comparacoes_media": round(comp, 1),
                           "tempo_medio_us": round(micro, 2)})
            print(f"{qtd:>6} | {nome:<10} | {comp:>8.1f} comparações | {micro:>9.2f} µs")
    return linhas


def experimento_ordenacao(rnd):
    linhas = []
    metodos = {"bolha": ordenar_bolha, "seleção": ordenar_selecao,
               "inserção": ordenar_insercao}
    for qtd in VOLUMES:
        registros = criar_registros(qtd, rnd)
        for nome, funcao in metodos.items():
            inicio = time.perf_counter()
            _, comp = funcao(registros, "duracao_min")
            gasto = time.perf_counter() - inicio
            linhas.append({"volume": qtd, "metodo": nome, "comparacoes": comp,
                           "tempo_s": round(gasto, 3)})
            print(f"{qtd:>6} | {nome:<9} | {comp:>12,} comparações | {gasto:>7.3f} s")
    return linhas


def gravar(nome, linhas):
    with open(nome, "w", newline="", encoding="utf-8") as arq:
        escritor = csv.DictWriter(arq, fieldnames=list(linhas[0].keys()))
        escritor.writeheader()
        escritor.writerows(linhas)


def grafico(linhas, arquivo="grafico_buscas.png"):
    """Gráfico de barras (escala logarítmica) feito com a biblioteca Pillow."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow não instalada: gráfico não gerado (pip install pillow).")
        return
    largura, altura = 1400, 800
    img = Image.new("RGB", (largura, altura), "white")
    d = ImageDraw.Draw(img)
    try:
        fonte = ImageFont.truetype("arial.ttf", 22)
        pequena = ImageFont.truetype("arial.ttf", 18)
    except OSError:
        fonte = pequena = ImageFont.load_default()
    cores = {"sequencial": (200, 90, 40), "binária": (40, 80, 160), "árvore": (60, 150, 90)}
    esq, topo, base = 120, 80, altura - 120
    maximo = math.log10(max(l["comparacoes_media"] for l in linhas)) + 0.3
    d.text((esq, 20), "Média de comparações por busca (escala logarítmica)", fill="black", font=fonte)
    for exp in range(0, int(maximo) + 1):  # linhas de grade 1, 10, 100...
        y = base - (exp / maximo) * (base - topo)
        d.line([(esq, y), (largura - 40, y)], fill=(225, 225, 225))
        d.text((esq - 80, y - 12), f"{10 ** exp:>6}", fill="black", font=pequena)
    grupo = (largura - esq - 80) / len(VOLUMES)
    barra = grupo / 4
    for g, qtd in enumerate(VOLUMES):
        x0 = esq + 20 + g * grupo
        for b, nome in enumerate(cores):
            valor = next(l["comparacoes_media"] for l in linhas
                         if l["volume"] == qtd and l["metodo"] == nome)
            h = (math.log10(max(valor, 1)) / maximo) * (base - topo)
            x = x0 + b * barra
            d.rectangle([x, base - h, x + barra - 10, base], fill=cores[nome])
            d.text((x, base - h - 26), f"{valor:g}", fill="black", font=pequena)
        d.text((x0 + barra, base + 15), f"{qtd:,} registros".replace(",", "."), fill="black", font=fonte)
    for b, (nome, cor) in enumerate(cores.items()):
        x = esq + b * 260
        d.rectangle([x, altura - 55, x + 25, altura - 30], fill=cor)
        d.text((x + 35, altura - 57), nome, fill="black", font=fonte)
    img.save(arquivo)
    print(f"Gráfico salvo em {arquivo}.")


if __name__ == "__main__":
    rnd = random.Random(SEMENTE)
    print("=== BUSCAS ===")
    buscas = experimento_busca(rnd)
    gravar("resultados_busca.csv", buscas)
    grafico(buscas)
    print("\n=== ORDENAÇÃO ===")
    gravar("resultados_ordenacao.csv", experimento_ordenacao(rnd))
