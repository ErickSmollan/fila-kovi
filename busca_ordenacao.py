"""Funções de busca e ordenação do Fila Kovi.

Todas devolvem também o número de comparações feitas,
que é a medida usada no experimento (experimento.py).
"""


# ---------------------------------------------------------------- buscas

def busca_sequencial(registros, codigo):
    """Olha um registro por vez. Funciona com a lista em qualquer ordem."""
    comparacoes = 0
    for i in range(len(registros)):
        comparacoes += 1
        if registros[i]["codigo"] == codigo:
            return i, comparacoes
    return -1, comparacoes


def busca_binaria(registros, codigo):
    """Divide a lista ao meio a cada passo. Exige a lista ordenada pelo código."""
    inicio = 0
    fim = len(registros) - 1
    comparacoes = 0
    while inicio <= fim:
        meio = (inicio + fim) // 2
        comparacoes += 1
        if registros[meio]["codigo"] == codigo:
            return meio, comparacoes
        elif registros[meio]["codigo"] < codigo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1, comparacoes


# ------------------------------------------------------------ ordenação
# As três recebem a chave (campo) e se a ordem é decrescente.
# Trabalham numa cópia, para não bagunçar a lista original.

def _fora_de_ordem(a, b, decrescente):
    """True quando a deve vir depois de b."""
    if decrescente:
        return a < b
    return a > b


def ordenar_bolha(registros, chave, decrescente=False):
    lista = registros[:]
    comparacoes = 0
    n = len(lista)
    for i in range(n - 1):
        trocou = False
        for j in range(n - 1 - i):
            comparacoes += 1
            if _fora_de_ordem(lista[j][chave], lista[j + 1][chave], decrescente):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                trocou = True
        if not trocou:  # já está ordenada: para antes
            break
    return lista, comparacoes


def ordenar_selecao(registros, chave, decrescente=False):
    lista = registros[:]
    comparacoes = 0
    n = len(lista)
    for i in range(n - 1):
        escolhido = i
        for j in range(i + 1, n):
            comparacoes += 1
            if _fora_de_ordem(lista[escolhido][chave], lista[j][chave], decrescente):
                escolhido = j
        lista[i], lista[escolhido] = lista[escolhido], lista[i]
    return lista, comparacoes


def ordenar_insercao(registros, chave, decrescente=False):
    lista = registros[:]
    comparacoes = 0
    for i in range(1, len(lista)):
        atual = lista[i]
        j = i - 1
        while j >= 0:
            comparacoes += 1
            if _fora_de_ordem(lista[j][chave], atual[chave], decrescente):
                lista[j + 1] = lista[j]
                j -= 1
            else:
                break
        lista[j + 1] = atual
    return lista, comparacoes
