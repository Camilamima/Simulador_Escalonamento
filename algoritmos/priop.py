def ordenar(prontas):
    prontas.sort(
        key=lambda t: (
            t.status == 'suspensa_mutex',  # 0 = ok, 1 = vai pro fim
            t.status == 'suspensa',        # se existir outro tipo
            -t.prioridade,
            not t.status == 'rodando',
            t.ingresso,
            t.duracao
        )
    )