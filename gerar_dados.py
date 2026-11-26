"""Gera atendimentos fictícios para testar o Fila Kovi.

Uso:
    python gerar_dados.py          -> cria atendimentos.csv com 40 registros
    python gerar_dados.py 500      -> cria com 500 registros

Nenhum dado é real: nomes e horários são sorteados.
"""

import csv
import random
import sys
from datetime import date, timedelta

from sistema import ARQUIVO, CAMPOS, SERVICOS, CONSULTORES

NOMES = ["Alice", "Bernardo", "Cecília", "Davi", "Elaine", "Fábio", "Gabriela",
         "Heitor", "Isadora", "João", "Kátia", "Lucas", "Marina", "Nicolas",
         "Olívia", "Paulo", "Rafaela", "Samuel", "Tatiana", "Vítor"]
SOBRENOMES = ["Alves", "Barros", "Costa", "Dias", "Farias", "Gomes", "Lima",
              "Melo", "Nunes", "Rocha", "Souza", "Teixeira"]
INICIO = date(2026, 10, 17)
FIM = date(2026, 11, 25)


def gerar(qtd, semente=42, aguardando=3):
    rnd = random.Random(semente)
    dias = (FIM - INICIO).days
    registros = []
    for i in range(qtd):
        dia = INICIO + timedelta(days=rnd.randint(0, dias))
        hora = rnd.randint(8, 17)
        minuto = rnd.randint(0, 59)
        registros.append({
            "data": dia.strftime("%d/%m/%Y"),
            "chegada": f"{hora:02d}:{minuto:02d}",
            "cliente": f"{rnd.choice(NOMES)} {rnd.choice(SOBRENOMES)[0]}.",
            "servico": rnd.choice(SERVICOS),
        })
    # código segue a ordem de chegada
    registros.sort(key=lambda r: (r["data"][6:], r["data"][3:5], r["data"][:2], r["chegada"]))
    for i, r in enumerate(registros):
        r["codigo"] = 1001 + i
        if i >= qtd - aguardando:
            r.update(consultor="", duracao_min=0, status="aguardando")
        else:
            r.update(consultor=rnd.choice(CONSULTORES),
                     duracao_min=max(5, int(rnd.gauss(35, 25))),
                     status="concluído")
    return registros


if __name__ == "__main__":
    qtd = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as arq:
        escritor = csv.DictWriter(arq, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(gerar(qtd))
    print(f"{qtd} atendimentos fictícios gravados em {ARQUIVO}.")
