import random

def atualizar_logica_ia(jogo):
    """ Gerencia as ações dos robôs baseando-se no estado atual da partida """
    if jogo.fase_distribuicao_inicial or jogo.turno_atual == 0 or len(jogo.animacoes_ativas) > 0 or not jogo.baralho_reservado:
        return

    jogo.tempo_acao_ia += 1
    
    if jogo.tempo_acao_ia == 45:
        carta_comprada = jogo.baralho_reservado.pop()
        if jogo.turno_atual == 1:
            jogo.disparar_animacao(carta_comprada, jogo.pos_monte[0], jogo.pos_monte[1], jogo.pos_adv1[0], jogo.pos_adv1[1] + 50, rotacionar=True)
        elif jogo.turno_atual == 2:
            jogo.disparar_animacao(carta_comprada, jogo.pos_monte[0], jogo.pos_monte[1], jogo.pos_parceiro[0] + 50, jogo.pos_parceiro[1])
        elif jogo.turno_atual == 3:
            jogo.disparar_animacao(carta_comprada, jogo.pos_monte[0], jogo.pos_monte[1], jogo.pos_adv2[0], jogo.pos_adv2[1] + 50, rotacionar=True)
        jogo.maos_ia[jogo.turno_atual].append(carta_comprada)

    elif jogo.tempo_acao_ia == 90:
        if jogo.maos_ia[jogo.turno_atual]:
            carta_descartada = jogo.maos_ia[jogo.turno_atual].pop(random.randrange(len(jogo.maos_ia[jogo.turno_atual])))
            
            if jogo.turno_atual == 1:
                jogo.disparar_animacao(carta_descartada, jogo.pos_adv1[0], jogo.pos_adv1[1] + 50, jogo.pos_lixo[0], jogo.pos_lixo[1], mostrar_frente=True)
            elif jogo.turno_atual == 2:
                jogo.disparar_animacao(carta_descartada, jogo.pos_parceiro[0] + 50, jogo.pos_parceiro[1], jogo.pos_lixo[0], jogo.pos_lixo[1], mostrar_frente=True)
            elif jogo.turno_atual == 3:
                jogo.disparar_animacao(carta_descartada, jogo.pos_adv2[0], jogo.pos_adv2[1] + 50, jogo.pos_lixo[0], jogo.pos_lixo[1], mostrar_frente=True)
            
            jogo.lixo.append(carta_descartada)
            jogo.alerta = f"O robô descartou um {carta_descartada.valor} de {carta_descartada.naipe}."
        
        proximos = {1: 2, 2: 3, 3: 0}
        jogo.turno_atual = proximos[jogo.turno_atual]
        jogo.tempo_acao_ia = 0
        if jogo.turno_atual == 0: 
            jogo.fase_turno = "COMPRAR"