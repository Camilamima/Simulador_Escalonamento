def ordenar(prontas):
    prontas.sort(
        key=lambda t: (
            t.status == 'suspensa_mutex',  # 0 = ok, 1 = vai pro fim
            t.status == 'suspensa',        # se existir outro tipo
            -t.prioridade_v,      # 1º critério
            -t.prioridade,        # 2º critério
            not t.status == 'rodando',  # 3º
            t.ingresso,           # 4º
            t.duracao             # 5º
        )
    )

def compara(x,y):
    if x.tarefa_rodando.prioridade_v<y.tarefa_rodando.prioridade_v:
        return x
    else:
        return y
    
def compara_tarefa(x,y):
    if x.prioridade_v<y.prioridade_v:
        return x
    else:
        return y