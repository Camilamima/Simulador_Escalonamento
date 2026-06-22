def ordenar(prontas):
    prontas.sort(
        key=lambda t: (
            -t.prioridade,
            not t.status == 'rodando',
            t.ingresso,
            t.duracao
        )
    )