def validar_novo_jogo(cartas_selecionadas):
    """ Valida se um conjunto de cartas forma uma sequência válida do mesmo naipe """
    if len(cartas_selecionadas) < 3:
        return False, "Um jogo precisa de pelo menos 3 cartas!"

    # Separa curingas (2) e cartas normais
    normais = [c for c in cartas_selecionadas if c.valor != "2"]
    curingas = [c for c in cartas_selecionadas if c.valor == "2"]

    if not normais:
        return False, "Não é permitido um jogo feito apenas de curingas!"

    # 1. Validação de Naipe Único
    naipe_base = normais[0].naipe
    if any(c.naipe != naipe_base for c in normais):
        return False, "Inválido! Todas as cartas da sequência devem ser do mesmo naipe."

    # 2. Validação de Sequência Numérica
    pesos = sorted([c.peso_numerico for c in normais])
    
    if len(pesos) != len(set(pesos)):
        return False, "Inválido! Cartas repetidas idênticas na mesma sequência."

    # Calcula buracos na sequência
    buracos = 0
    for i in range(len(pesos) - 1):
        diff = pesos[i+1] - pesos[i] - 1
        if diff > 0:
            buracos += diff

    if buracos > len(curingas):
        return False, "Inválido! As cartas não formam uma sequência numérica contínua."

    return True, "Jogo válido!"

def validar_adicao_jogo(carta, jogo_existente):
    """ Valida se uma única carta pode entrar em um jogo que já está na mesa """
    normais_jogo = [c for c in jogo_existente if c.valor != "2"]
    
    if not normais_jogo:
        return True

    naipe_jogo = normais_jogo[0].naipe

    if carta.valor != "2" and carta.naipe != naipe_jogo:
        return False

    pesos_atuais = sorted([c.peso_numerico for c in jogo_existente])
    
    if carta.valor != "2":
        if carta.peso_numerico in pesos_atuais:
            return False
        if carta.peso_numerico == pesos_atuais[0] - 1 or carta.peso_numerico == pesos_atuais[-1] + 1:
            return True
        
        novos_pesos = sorted(pesos_atuais + [carta.peso_numerico])
        curingas_jogo = [c for c in jogo_existente if c.valor == "2"]
        buracos = sum((novos_pesos[i+1] - novos_pesos[i] - 1) for i in range(len(novos_pesos)-1))
        return buracos <= len(curingas_jogo)
    else:
        qtd_curingas = sum(1 for c in jogo_existente if c.valor == "2")
        return qtd_curingas < 2