"""Fila Kovi - controle da fila de atendimento de uma locadora de veículos.

Programa de terminal. Os atendimentos ficam no arquivo atendimentos.csv.
Rodar com:  python sistema.py
"""

import csv
from datetime import datetime

from busca_ordenacao import (busca_sequencial, busca_binaria,
                             ordenar_bolha, ordenar_selecao, ordenar_insercao)
from estruturas import Fila

ARQUIVO = "atendimentos.csv"
CAMPOS = ["codigo", "data", "chegada", "cliente", "servico",
          "consultor", "duracao_min", "status"]
SERVICOS = ["locação", "devolução", "troca de carro", "financeiro", "sinistro"]
CONSULTORES = ["Ana", "Bruno", "Carla", "Diego", "Elisa"]
LIMITE_ALERTA = 90  # minutos: acima disso o atendimento entra em alerta

atendimentos = []   # todos os registros (memória)
fila = Fila()       # clientes aguardando, na ordem de chegada


# --------------------------------------------------------------- arquivo

def carregar():
    try:
        with open(ARQUIVO, newline="", encoding="utf-8") as arq:
            for linha in csv.DictReader(arq):
                linha["codigo"] = int(linha["codigo"])
                linha["duracao_min"] = int(linha["duracao_min"])
                atendimentos.append(linha)
    except FileNotFoundError:
        pass  # primeira execução: o arquivo ainda não existe
    # quem estava aguardando volta para a fila, na ordem de chegada (código)
    aguardando, _ = ordenar_insercao(
        [a for a in atendimentos if a["status"] == "aguardando"], "codigo")
    for a in aguardando:
        fila.entrar(a)


def salvar():
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as arq:
        escritor = csv.DictWriter(arq, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(atendimentos)


# ------------------------------------------------------ leitura e validação

def ler_inteiro(mensagem, minimo=None):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo is not None and valor < minimo:
                print(f"O valor precisa ser pelo menos {minimo}.")
                continue
            return valor
        except ValueError:
            print("Digite um número inteiro.")


def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("Esse campo não pode ficar vazio.")


def ler_opcao(mensagem, opcoes):
    print(mensagem)
    for i, item in enumerate(opcoes, start=1):
        print(f"  {i}-{item}")
    while True:
        numero = ler_inteiro("Escolha: ")
        if 1 <= numero <= len(opcoes):
            return opcoes[numero - 1]
        print("Opção inválida.")


def proximo_codigo():
    maior = 1000
    for a in atendimentos:
        if a["codigo"] > maior:
            maior = a["codigo"]
    return maior + 1


def mostrar(a):
    duracao = f"{a['duracao_min']} min" if a["status"] == "concluído" else "-"
    print(f"{a['codigo']} | {a['data']} {a['chegada']} | {a['cliente']:<12} | "
          f"{a['servico']:<14} | {a['consultor'] or '-':<6} | {duracao:>7} | {a['status']}")


# --------------------------------------------------------------- funções

def registrar_chegada():
    agora = datetime.now()
    cliente = ler_texto("Nome do cliente: ")
    servico = ler_opcao("Serviço:", SERVICOS)
    novo = {"codigo": proximo_codigo(), "data": agora.strftime("%d/%m/%Y"),
            "chegada": agora.strftime("%H:%M"), "cliente": cliente,
            "servico": servico, "consultor": "", "duracao_min": 0,
            "status": "aguardando"}
    atendimentos.append(novo)
    fila.entrar(novo)
    salvar()
    print(f"Cliente na fila com o código {novo['codigo']}. "
          f"Posição: {fila.tamanho}.")


def ver_fila():
    if fila.vazia():
        print("Ninguém aguardando.")
        return
    for posicao, a in enumerate(fila.itens(), start=1):
        print(f"{posicao}º ", end="")
        mostrar(a)


def consultor_livre():
    """Escolhe o consultor sem atendimento em andamento e com menos
    atendimentos no total. Assim o volume fica equilibrado."""
    ocupados = [a["consultor"] for a in atendimentos if a["status"] == "em atendimento"]
    escolhido = None
    menor = None
    for c in CONSULTORES:
        if c in ocupados:
            continue
        total = 0
        for a in atendimentos:
            if a["consultor"] == c:
                total += 1
        if menor is None or total < menor:
            escolhido = c
            menor = total
    return escolhido


def chamar_proximo():
    if fila.vazia():
        print("Ninguém aguardando.")
        return
    consultor = consultor_livre()
    if consultor is None:
        print("Todos os consultores estão em atendimento.")
        return
    a = fila.sair()  # sempre o primeiro que chegou (FIFO)
    a["consultor"] = consultor
    a["status"] = "em atendimento"
    salvar()
    print(f"{a['cliente']} (código {a['codigo']}) vai com {consultor}.")


def finalizar():
    em_andamento = [a for a in atendimentos if a["status"] == "em atendimento"]
    if len(em_andamento) == 0:
        print("Nenhum atendimento em andamento.")
        return
    for a in em_andamento:
        mostrar(a)
    codigo = ler_inteiro("Código do atendimento a finalizar: ")
    posicao, _ = busca_sequencial(em_andamento, codigo)
    if posicao == -1:
        print("Esse código não está em atendimento.")
        return
    a = em_andamento[posicao]
    a["duracao_min"] = ler_inteiro("Duração (minutos): ", minimo=1)
    a["status"] = "concluído"
    salvar()
    print("Atendimento concluído.")
    if a["duracao_min"] > LIMITE_ALERTA:
        print(f"Alerta: passou de {LIMITE_ALERTA} minutos.")


def listar(lista):
    if len(lista) == 0:
        print("Nenhum atendimento registrado.")
        return
    for a in lista:
        mostrar(a)


def buscar():
    if len(atendimentos) == 0:
        print("Nenhum atendimento registrado.")
        return
    codigo = ler_inteiro("Código procurado: ")
    _, comp_seq = busca_sequencial(atendimentos, codigo)
    ordenados, _ = ordenar_insercao(atendimentos, "codigo")
    posicao, comp_bin = busca_binaria(ordenados, codigo)
    if posicao == -1:
        print("Atendimento não encontrado.")
    else:
        mostrar(ordenados[posicao])
    print(f"Comparações: sequencial {comp_seq} | binária {comp_bin}")


def ranking():
    concluidos = [a for a in atendimentos if a["status"] == "concluído"]
    if len(concluidos) == 0:
        print("Nenhum atendimento concluído.")
        return
    metodo = ler_opcao("Método de ordenação:", ["bolha", "seleção", "inserção"])
    funcoes = {"bolha": ordenar_bolha, "seleção": ordenar_selecao,
               "inserção": ordenar_insercao}
    lista, comparacoes = funcoes[metodo](concluidos, "duracao_min", decrescente=True)
    print("Atendimentos do mais longo para o mais curto:")
    listar(lista)
    print(f"({metodo}: {comparacoes} comparações)")


def relatorio():
    concluidos = [a for a in atendimentos if a["status"] == "concluído"]
    if len(concluidos) == 0:
        print("Nenhum atendimento concluído.")
        return
    total = 0
    maior = concluidos[0]
    menor = concluidos[0]
    for a in concluidos:
        total += a["duracao_min"]
        if a["duracao_min"] > maior["duracao_min"]:
            maior = a
        if a["duracao_min"] < menor["duracao_min"]:
            menor = a
    print(f"Atendimentos concluídos: {len(concluidos)}")
    print(f"Tempo médio de atendimento: {total / len(concluidos):.1f} min")
    print(f"Mais longo: {maior['codigo']} ({maior['duracao_min']} min)")
    print(f"Mais curto: {menor['codigo']} ({menor['duracao_min']} min)")
    print(f"Aguardando na fila: {fila.tamanho}")

    # matriz consultor x serviço (quantos atendimentos cada um fez de cada tipo)
    matriz = [[0] * len(SERVICOS) for _ in CONSULTORES]
    minutos = [0] * len(CONSULTORES)
    for a in concluidos:
        if a["consultor"] in CONSULTORES:
            i = CONSULTORES.index(a["consultor"])
            j = SERVICOS.index(a["servico"])
            matriz[i][j] += 1
            minutos[i] += a["duracao_min"]
    print("\nAtendimentos por consultor e serviço:")
    cabecalho = "".join(f"{s[:10]:>11}" for s in SERVICOS)
    print(f"{'consultor':<10}{cabecalho}{'total':>7}{'média':>8}")
    for i, c in enumerate(CONSULTORES):
        qtd = sum(matriz[i])
        media = minutos[i] / qtd if qtd else 0
        linha = "".join(f"{n:>11}" for n in matriz[i])
        print(f"{c:<10}{linha}{qtd:>7}{media:>8.1f}")

    alertas = [a for a in concluidos if a["duracao_min"] > LIMITE_ALERTA]
    print(f"\nAtendimentos acima de {LIMITE_ALERTA} min: {len(alertas)}")
    for a in alertas:
        mostrar(a)


def menu():
    carregar()
    while True:
        print(f"\n=== FILA KOVI === aguardando: {fila.tamanho}")
        print("1-Chegada de cliente  2-Ver fila  3-Chamar próximo  4-Finalizar atendimento")
        print("5-Listar  6-Buscar por código  7-Ranking por duração  8-Relatório  0-Sair")
        opcao = input("Opção: ").strip()
        if opcao == "1":
            registrar_chegada()
        elif opcao == "2":
            ver_fila()
        elif opcao == "3":
            chamar_proximo()
        elif opcao == "4":
            finalizar()
        elif opcao == "5":
            listar(atendimentos)
        elif opcao == "6":
            buscar()
        elif opcao == "7":
            ranking()
        elif opcao == "8":
            relatorio()
        elif opcao == "0":
            salvar()
            print("Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
