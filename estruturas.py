"""Estruturas de dados do Fila Kovi.

- Fila: guarda os clientes que chegaram e esperam atendimento.
  Quem chega primeiro é atendido primeiro (FIFO).
- ArvoreBusca: árvore binária de busca pelo código do atendimento.
  Usada no experimento para comparar com as outras buscas.
"""


class _No:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None


class Fila:
    """Fila encadeada: entra no fim, sai do começo."""

    def __init__(self):
        self.inicio = None
        self.fim = None
        self.tamanho = 0

    def vazia(self):
        return self.tamanho == 0

    def entrar(self, valor):
        novo = _No(valor)
        if self.vazia():
            self.inicio = novo
        else:
            self.fim.proximo = novo
        self.fim = novo
        self.tamanho += 1

    def sair(self):
        """Tira e devolve quem está na frente. Devolve None se estiver vazia."""
        if self.vazia():
            return None
        valor = self.inicio.valor
        self.inicio = self.inicio.proximo
        if self.inicio is None:
            self.fim = None
        self.tamanho -= 1
        return valor

    def itens(self):
        """Lista os itens do primeiro ao último, sem tirar ninguém da fila."""
        resultado = []
        atual = self.inicio
        while atual is not None:
            resultado.append(atual.valor)
            atual = atual.proximo
        return resultado


class _NoArvore:
    def __init__(self, registro):
        self.registro = registro
        self.esquerda = None
        self.direita = None


class ArvoreBusca:
    """Árvore binária de busca: menores à esquerda, maiores à direita."""

    def __init__(self):
        self.raiz = None

    def inserir(self, registro):
        novo = _NoArvore(registro)
        if self.raiz is None:
            self.raiz = novo
            return
        atual = self.raiz
        while True:
            if registro["codigo"] < atual.registro["codigo"]:
                if atual.esquerda is None:
                    atual.esquerda = novo
                    return
                atual = atual.esquerda
            else:
                if atual.direita is None:
                    atual.direita = novo
                    return
                atual = atual.direita

    def buscar(self, codigo):
        """Busca recursiva. Devolve (registro ou None, comparações)."""
        return self._buscar(self.raiz, codigo, 0)

    def _buscar(self, no, codigo, comparacoes):
        if no is None:
            return None, comparacoes
        comparacoes += 1
        if codigo == no.registro["codigo"]:
            return no.registro, comparacoes
        if codigo < no.registro["codigo"]:
            return self._buscar(no.esquerda, codigo, comparacoes)
        return self._buscar(no.direita, codigo, comparacoes)
