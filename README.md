# Fila Kovi

Programa em Python, de terminal, para organizar a fila de atendimento de uma locadora de veículos.
Projeto Integrador: Laboratório de Programação (UNISA, 2026), por Erick Morais Vitoriano (RA 5589347).

## O que faz

- Coloca o cliente na fila por ordem de chegada (fila encadeada, FIFO)
- Chama o próximo e envia ao consultor livre com menos atendimentos
- Finaliza o atendimento com a duração e avisa quando passa de 90 minutos
- Busca por código (busca binária, mostrando as comparações)
- Ranking por duração com bolha, seleção ou inserção (sem `sorted()`)
- Relatório: tempo médio, maior e menor atendimento e matriz consultor × serviço
- Grava tudo em `atendimentos.csv`

## Como rodar

Precisa do Python 3.

```
python gerar_dados.py      # cria 40 atendimentos fictícios
python sistema.py          # abre o menu
python experimento.py      # compara as buscas com 100, 1.000 e 10.000 registros
```

O gráfico do experimento usa a biblioteca Pillow (`pip install pillow`). Sem ela, o experimento roda e só não desenha o gráfico.

## Arquivos

| Arquivo | Para quê |
|---|---|
| `sistema.py` | Menu e regras do atendimento |
| `estruturas.py` | Fila encadeada e árvore binária de busca |
| `busca_ordenacao.py` | Buscas e métodos de ordenação |
| `gerar_dados.py` | Dados fictícios para teste |
| `experimento.py` | Experimento das buscas e ordenações |

Todos os nomes nos dados são fictícios.
