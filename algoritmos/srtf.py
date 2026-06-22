def ordenar(prontas):
    prontas.sort(
        key=lambda t: (
            t.duracao,
            not t.status == 'rodando',
            t.ingresso
        )
    )