import pygame
import random
import sys
import math

# Inicialização do Pygame
pygame.init()

# Configurações de Resolução Base
LARGURA_BASE, ALTURA_BASE = 1250, 800
tela_janela = pygame.display.set_mode((LARGURA_BASE, ALTURA_BASE))
pygame.display.set_caption("Canastra 2.0 - Regras Oficiais e Trava de Layout")

tela_virtual = pygame.Surface((LARGURA_BASE, ALTURA_BASE))

# Cores
COR_FUNDO = (20, 90, 40)
COR_MENU_FUNDO = (15, 60, 30)
COR_CARTA = (255, 255, 255)
COR_VERSO_AZUL = (30, 70, 150)
COR_VERSO_VERMELHO = (180, 40, 40)
COR_VERSO_BORDA = (220, 220, 255)
COR_SELECIONADA = (255, 215, 0)
COR_BLOQUEIO = (220, 50, 50)
COR_TEXTO = (255, 255, 255)
COR_BOTAO = (40, 50, 130)
COR_BOTAO_HOVER = (60, 80, 200)
COR_BOTAO_ATIVO = (230, 180, 40)

# Fontes
fonte_p = pygame.font.SysFont("Arial", 12, bold=True)
fonte_m = pygame.font.SysFont("Arial", 16, bold=True)
fonte_g = pygame.font.SysFont("Arial", 24, bold=True)
fonte_titulo = pygame.font.SysFont("Arial", 48, bold=True)

# Dados do Baralho
NAIPES = ["Copas", "Espadas", "Ouros", "Paus"]
VALORES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
PONTOS_CARTAS = {v: 10 if v in ["8", "9", "10", "J", "Q", "K"] else (15 if v == "A" else (20 if v == "2" else 5)) for v in VALORES}

ORDEM_NUMERICA = {v: i+1 for i, v in enumerate(VALORES)}
ORDEM_NAIPES = {"Copas": 0, "Espadas": 1, "Ouros": 2, "Paus": 3}

class CartaVisual:
    def __init__(self, naipe, valor):
        self.naipe = naipe
        self.valor = valor
        self.valor_pontos = PONTOS_CARTAS[valor]
        self.peso_numerico = ORDEM_NUMERICA[valor]
        self.peso_naipe = ORDEM_NAIPES[naipe]
        self.largura = 60
        self.altura = 85
        self.rect = pygame.Rect(0, 0, self.largura, self.altura)
        self.selecionada = False
        self.offset_animacao = random.uniform(0, 10)

    def desenhar_frente(self, superficie, x, y, tempo=0):
        efeito_flutuar = math.sin(tempo * 3 + self.offset_animacao) * 3 if not self.selecionada else 0
        self.rect.x = x
        self.rect.y = (y - 20 if self.selecionada else y) + efeito_flutuar
        
        pygame.draw.rect(superficie, COR_CARTA, self.rect, border_radius=5)
        cor_borda = COR_SELECIONADA if self.selecionada else (COR_BLOQUEIO if self.valor == "2" else (0, 0, 0))
        pygame.draw.rect(superficie, cor_borda, self.rect, 2 if self.selecionada else 1, border_radius=5)
        
        cor_naipe = (200, 0, 0) if self.naipe in ["Copas", "Ouros"] else (0, 0, 0)
        simbolos = {"Copas": "♥", "Ouros": "♦", "Espadas": "♠", "Paus": "♣"}
        
        txt = fonte_m.render(f"{self.valor}{simbolos[self.naipe]}", True, cor_naipe)
        superficie.blit(txt, (self.rect.x + 5, self.rect.y + 5))

    def desenhar_verso(self, superficie, x, y, rotacionada=False, tempo=0, cor_fundo=COR_VERSO_AZUL):
        w = self.altura if rotacionada else self.largura
        h = self.largura if rotacionada else self.altura
        efeito_balanco = math.cos(tempo * 2 + x * 0.05) * 1.5 if tempo > 0 else 0
        y_final = y + efeito_balanco if not rotacionada else y
        x_final = x + efeito_balanco if rotacionada else x
        
        rect_verso = pygame.Rect(x_final, y_final, w, h)
        pygame.draw.rect(superficie, cor_fundo, rect_verso, border_radius=5)
        pygame.draw.rect(superficie, COR_VERSO_BORDA, rect_verso, 1, border_radius=5)
        
        cor_linhas = (200, 80, 80) if cor_fundo == COR_VERSO_VERMELHO else (50, 100, 200)
        if rotacionada:
            pygame.draw.line(superficie, cor_linhas, (x_final, y_final + h//2), (x_final + w, y_final + h//2), 2)
        else:
            pygame.draw.line(superficie, cor_linhas, (x_final + w//2, y_final), (x_final + w//2, y_final + h), 2)


class AnimacaoCarta:
    def __init__(self, carta, x_ini, y_ini, x_fim, y_fim, mostrar_frente=False, rotacionar=False, velocidade=0.08):
        self.carta = carta
        self.x_atual = x_ini
        self.y_atual = y_ini
        self.x_fim = x_fim
        self.y_fim = y_fim
        self.mostrar_frente = mostrar_frente
        self.rotacionar = rotacionar
        self.progresso = 0.0
        self.velocidade = velocidade
        self.concluida = False

    def atualizar(self):
        if self.progresso < 1.0:
            self.progresso += self.velocidade
            if self.progresso >= 1.0:
                self.progresso = 1.0
                self.concluida = True
            self.x_atual = self.x_atual + (self.x_fim - self.x_atual) * self.progresso
            self.y_atual = self.y_atual + (self.y_fim - self.y_atual) * self.progresso

    def desenhar(self, superficie, tempo):
        if self.mostrar_frente:
            self.carta.desenhar_frente(superficie, int(self.x_atual), int(self.y_atual), tempo)
        else:
            self.carta.desenhar_verso(superficie, int(self.x_atual), int(self.y_atual), rotacionada=self.rotacionar, tempo=0)


class JogoVisual:
    def __init__(self):
        self.estado_jogo = "MENU"
        self.meta_pontos = 3000
        self.tela_cheia = False
        
        self.turno_atual = 0 
        self.tempo_acao_ia = 0 
        
        self.modo_organizacao_atual = "naipe" 

        self.baralho_reservado = [] 
        self.mao_jogador = []
        self.maos_ia = {1: [], 2: [], 3: []}
        self.morto_1 = []
        self.morto_2 = []
        self.lixo = []
        
        self.fase_distribuicao_inicial = False
        self.cartas_para_distribuir = []
        self.cronometro_distribuicao = 0
        
        self.jogos_na_mesa = [] # Lista de listas de cartas descidas
        self.fase_turno = "COMPRAR"
        self.alerta = ""
        self.animacoes_ativas = []

        # Posições Estratégicas
        self.pos_monte = (530, 200)
        self.pos_lixo = (630, 200)
        self.pos_adv1 = (40, 220)
        self.pos_parceiro = (440, 70)
        self.pos_adv2 = (1140, 220)
        self.pos_morto_base = (1050, 70)

        self.rect_monte = pygame.Rect(self.pos_monte[0], self.pos_monte[1], 60, 85)
        self.rect_lixo = pygame.Rect(self.pos_lixo[0], self.pos_lixo[1], 60, 85)
        
        # Botões
        self.btn_descer_dinamico = pygame.Rect(525, 595, 200, 35)
        self.btn_org_numero = pygame.Rect(50, 600, 120, 28)
        self.btn_org_naipe = pygame.Rect(180, 600, 120, 28)
        
        self.btn_3000 = pygame.Rect(325, 380, 150, 50)
        self.btn_5000 = pygame.Rect(550, 380, 150, 50)
        self.btn_8000 = pygame.Rect(775, 380, 150, 50)
        self.btn_jogar = pygame.Rect(475, 520, 300, 60)

    def iniciar_partida(self):
        self.estado_jogo = "PARTIDA"
        self.turno_atual = 0
        self.fase_turno = "COMPRAR"
        self.jogos_na_mesa.clear()
        self.animacoes_ativas.clear()
        self.lixo.clear()
        self.mao_jogador.clear()
        self.maos_ia[1].clear()
        self.maos_ia[2].clear()
        self.maos_ia[3].clear()
        
        self.baralho_reservado = []
        for _ in range(2):
            for naipe in NAIPES:
                for valor in VALORES:
                    self.baralho_reservado.append(CartaVisual(naipe, valor))
                    
        random.shuffle(self.baralho_reservado)
        
        self.morto_1 = [self.baralho_reservado.pop() for _ in range(11)]
        self.morto_2 = [self.baralho_reservado.pop() for _ in range(11)]
        
        self.cartas_para_distribuir = []
        for _ in range(11):
            self.cartas_para_distribuir.append((0, self.baralho_reservado.pop()))
            self.cartas_para_distribuir.append((1, self.baralho_reservado.pop()))
            self.cartas_para_distribuir.append((2, self.baralho_reservado.pop()))
            self.cartas_para_distribuir.append((3, self.baralho_reservado.pop()))
            
        self.fase_distribuicao_inicial = True
        self.cronometro_distribuicao = 0
        self.alerta = "Distribuindo cartas... Formando sua mão inicial!"

    def aplicar_auto_organizacao(self):
        if self.modo_organizacao_atual == "numero":
            self.mao_jogador.sort(key=lambda c: (c.peso_numerico, c.peso_naipe))
        elif self.modo_organizacao_atual == "naipe":
            self.mao_jogador.sort(key=lambda c: (c.peso_naipe, c.peso_numerico))
        self.atualizar_posicoes_mao()

    def organizar_por_numero(self):
        self.modo_organizacao_atual = "numero"
        self.aplicar_auto_organizacao()
        self.alerta = "Mão organizada por sequência numérica!"

    def organizar_por_naipe(self):
        self.modo_organizacao_atual = "naipe"
        self.aplicar_auto_organizacao()
        self.alerta = "Mão organizada por Naipes!"

    def atualizar_posicoes_mao(self):
        if not self.mao_jogador: return
        
        qtd = len(self.mao_jogador)
        largura_disponivel = LARGURA_BASE - 120
        passo = 45 
        
        if ((qtd - 1) * passo + 60) > largura_disponivel:
            passo = (largura_disponivel - 60) / (qtd - 1)
            
        largura_total_real = ((qtd - 1) * passo) + 60
        x_inicial = (LARGURA_BASE - largura_total_real) // 2
        
        for i, carta in enumerate(self.mao_jogador):
            carta.rect.x = int(x_inicial + (i * passo))
            carta.rect.y = 670

    def obter_posicao_final_sua_mao(self):
        if not self.mao_jogador: return LARGURA_BASE // 2, 670
        return self.mao_jogador[-1].rect.x + 35, 670

    def alternar_tela_cheia(self):
        self.tela_cheia = not self.tela_cheia
        if self.tela_cheia: pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else: pygame.display.set_mode((LARGURA_BASE, ALTURA_BASE))

    def disparar_animacao(self, carta, x_ini, y_ini, x_fim, y_fim, mostrar_frente=False, rotacionar=False):
        anim = AnimacaoCarta(carta, x_ini, y_ini, x_fim, y_fim, mostrar_frente, rotacionar)
        self.animacoes_ativas.append(anim)

    # --- SISTEMA DE VALIDAÇÃO DE REGRAS REAIS ---
    def validar_novo_jogo(self, cartas_selecionadas):
        """ Valida se um conjunto de cartas forma uma sequência válida do mesmo naipe """
        if len(cartas_selecionadas) < 3:
            return False, "Um jogo precisa de pelo menos 3 cartas!"

        # Separa curingas (2) e cartas normais
        normais = [c for c in cartas_selecionadas if c.valor != "2"]
        curingas = [c for c in cartas_selecionadas if c.valor == "2"]

        if not normais:
            # Caso bizarro de tentar descer apenas curingas de 2
            return False, "Não é permitido um jogo feito apenas de curingas!"

        # 1. Validação de Naipe Único (Regra da Canastra)
        naipe_base = normais[0].naipe
        if any(c.naipe != naipe_base for c in normais):
            return False, "Inválido! Todas as cartas da sequência devem ser do mesmo naipe."

        # 2. Validação de Sequência Numérica
        pesos = sorted([c.peso_numerico for c in normais])
        
        # Verifica se existem duplicadas nas normais (ex: dois 5 de espadas sem ser curinga na sequência)
        if len(pesos) != len(set(pesos)):
            return False, "Inválido! Cartas repetidas idênticas na mesma sequência."

        # Calcula buracos na sequência para ver se os curingas cobrem
        buracos = 0
        for i in range(len(pesos) - 1):
            diff = pesos[i+1] - pesos[i] - 1
            if diff > 0:
                buracos += diff

        if buracos > len(curingas):
            return False, "Inválido! As cartas não formam uma sequência numérica contínua."

        return True, "Jogo válido!"

    def validar_adicao_jogo(self, carta, jogo_existente):
        """ Valida se uma única carta pode entrar em um jogo que já está na mesa """
        # Filtra as cartas normais do jogo para identificar o naipe correto
        normais_jogo = [c for c in jogo_existente if c.valor != "2"]
        
        if not normais_jogo:
            return True # Se só tiver curingas por algum motivo limpa a trava

        naipe_jogo = normais_jogo[0].naipe

        # Se a carta não for curinga, ela PRECISA ser do mesmo naipe
        if carta.valor != "2" and carta.naipe != naipe_jogo:
            return False

        # Se for curinga, ela assume o naipe do jogo temporariamente, permitindo a inserção
        pesos_atuais = sorted([c.peso_numerico for c in jogo_existente])
        
        if carta.valor != "2":
            # Verifica se já existe esse número no jogo
            if carta.peso_numerico in pesos_atuais:
                return False
            # Verifica se ela encaixa nas extremidades ou preenche buracos
            if carta.peso_numerico == pesos_atuais[0] - 1 or carta.peso_numerico == pesos_atuais[-1] + 1:
                return True
            
            # Testa inserção direta ordenando tudo
            novos_pesos = sorted(pesos_atuais + [carta.peso_numerico])
            curingas_jogo = [c for c in jogo_existente if c.valor == "2"]
            buracos = sum((novos_pesos[i+1] - novos_pesos[i] - 1) for i in range(len(novos_pesos)-1))
            return buracos <= len(curingas_jogo)

        else:
            # É curinga de 2, sempre pode entrar se o jogo ainda tiver espaço para curingas (limite de 1 por jogo)
            qtd_curingas = sum(1 for c in jogo_existente if c.valor == "2")
            return qtd_curingas < 2

    def atualizar_logica_ia(self):
        if self.fase_distribuicao_inicial or self.turno_atual == 0 or len(self.animacoes_ativas) > 0 or not self.baralho_reservado:
            return

        self.tempo_acao_ia += 1
        
        if self.tempo_acao_ia == 45:
            carta_comprada = self.baralho_reservado.pop()
            if self.turno_atual == 1:
                self.disparar_animacao(carta_comprada, self.pos_monte[0], self.pos_monte[1], self.pos_adv1[0], self.pos_adv1[1] + 50, rotacionar=True)
            elif self.turno_atual == 2:
                self.disparar_animacao(carta_comprada, self.pos_monte[0], self.pos_monte[1], self.pos_parceiro[0] + 50, self.pos_parceiro[1])
            elif self.turno_atual == 3:
                self.disparar_animacao(carta_comprada, self.pos_monte[0], self.pos_monte[1], self.pos_adv2[0], self.pos_adv2[1] + 50, rotacionar=True)
            self.maos_ia[self.turno_atual].append(carta_comprada)

        elif self.tempo_acao_ia == 90:
            if self.maos_ia[self.turno_atual]:
                carta_descartada = self.maos_ia[self.turno_atual].pop(random.randrange(len(self.maos_ia[self.turno_atual])))
                
                if self.turno_atual == 1:
                    self.disparar_animacao(carta_descartada, self.pos_adv1[0], self.pos_adv1[1] + 50, self.pos_lixo[0], self.pos_lixo[1], mostrar_frente=True)
                elif self.turno_atual == 2:
                    self.disparar_animacao(carta_descartada, self.pos_parceiro[0] + 50, self.pos_parceiro[1], self.pos_lixo[0], self.pos_lixo[1], mostrar_frente=True)
                elif self.turno_atual == 3:
                    self.disparar_animacao(carta_descartada, self.pos_adv2[0], self.pos_adv2[1] + 50, self.pos_lixo[0], self.pos_lixo[1], mostrar_frente=True)
                
                self.lixo.append(carta_descartada)
                self.alerta = f"O robô descartou um {carta_descartada.valor} de {carta_descartada.naipe}."
            
            proximos = {1: 2, 2: 3, 3: 0}
            self.turno_atual = proximos[self.turno_atual]
            self.tempo_acao_ia = 0
            if self.turno_atual == 0: self.fase_turno = "COMPRAR"

    def rodar(self):
        relogio = pygame.time.Clock()
        
        while True:
            relogio.tick(60)
            tempo = pygame.time.get_ticks() / 1000.0
            
            largura_atual, altura_atual = pygame.display.get_surface().get_size()
            pos_mouse_real = pygame.mouse.get_pos()
            pos_mouse = (
                int(pos_mouse_real[0] * (LARGURA_BASE / largura_atual)),
                int(pos_mouse_real[1] * (ALTURA_BASE / altura_atual))
            )
            
            if self.estado_jogo == "PARTIDA":
                if self.fase_distribuicao_inicial:
                    self.cronometro_distribuicao += 1
                    if self.cronometro_distribuicao >= 6:
                        self.cronometro_distومتica = 0
                        if self.cartas_para_distribuir:
                            alvo, carta = self.cartas_para_distribuir.pop(0)
                            if alvo == 0:
                                self.disparar_animacao(carta, self.pos_monte[0], self.pos_monte[1], *self.obter_posicao_final_sua_mao(), mostrar_frente=True)
                                self.mao_jogador.append(carta)
                                self.aplicar_auto_organizacao()
                            elif alvo == 1:
                                self.disparar_animacao(carta, self.pos_monte[0], self.pos_monte[1], self.pos_adv1[0], self.pos_adv1[1] + 50, rotacionar=True)
                                self.maos_ia[1].append(carta)
                            elif alvo == 2:
                                self.disparar_animacao(carta, self.pos_monte[0], self.pos_monte[1], self.pos_parceiro[0] + 50, self.pos_parceiro[1])
                                self.maos_ia[2].append(carta)
                            elif alvo == 3:
                                self.disparar_animacao(carta, self.pos_monte[0], self.pos_monte[1], self.pos_adv2[0], self.pos_adv2[1] + 50, rotacionar=True)
                                self.maos_ia[3].append(carta)
                        else:
                            self.fase_distribuicao_inicial = False
                            self.lixo.append(self.baralho_reservado.pop())
                            self.alerta = "Sua vez! Compre do Monte ou do Lixo."
                
                self.atualizar_logica_ia()
                for anim in self.animacoes_ativas[:]:
                    anim.atualizar()
                    if anim.concluida: self.animacoes_ativas.remove(anim)

            # --- RENDERIZAÇÃO ---
            if self.estado_jogo == "MENU":
                tela_virtual.fill(COR_MENU_FUNDO)
                txt_tit = fonte_titulo.render("CANASTRA 2.0", True, (255, 230, 100))
                tela_virtual.blit(txt_tit, (LARGURA_BASE // 2 - txt_tit.get_width() // 2, 130))
                
                for btn, valor in [(self.btn_3000, 3000), (self.btn_5000, 5000), (self.btn_8000, 8000)]:
                    cor = COR_BOTAO_ATIVO if self.meta_pontos == valor else (COR_BOTAO_HOVER if btn.collidepoint(pos_mouse) else COR_BOTAO)
                    pygame.draw.rect(tela_virtual, cor, btn, border_radius=8)
                    txt = fonte_g.render(str(valor), True, (0,0,0) if self.meta_pontos == valor else COR_TEXTO)
                    tela_virtual.blit(txt, (btn.x + (btn.w//2 - txt.get_width()//2), btn.y + 12))

                pygame.draw.rect(tela_virtual, (100, 220, 100) if self.btn_jogar.collidepoint(pos_mouse) else (60, 180, 60), self.btn_jogar, border_radius=10)
                txt_j = fonte_g.render("INICIAR JOGO", True, (0, 40, 0))
                tela_virtual.blit(txt_j, (self.btn_jogar.x + (self.btn_jogar.w//2 - txt_j.get_width()//2), self.btn_jogar.y + 15))

            elif self.estado_jogo == "PARTIDA":
                tela_virtual.fill(COR_FUNDO)
                
                nomes_turnos = {0: "Sua Vez!", 1: "Vez do Adv 1", 2: "Vez do Parceiro", 3: "Vez do Adv 2"}
                tela_virtual.blit(fonte_g.render("CANASTRA 2.0 - MESA", True, COR_TEXTO), (20, 20))
                tela_virtual.blit(fonte_m.render(f"Turno: {nomes_turnos[self.turno_atual]}", True, (255, 255, 100)), (20, 60))
                
                pygame.draw.rect(tela_virtual, (10, 50, 25), (250, 20, 750, 35), border_radius=5)
                tela_virtual.blit(fonte_m.render(self.alerta, True, (255, 230, 150)), (265, 28))

                for i in range(len(self.maos_ia[2])): CartaVisual("Copas", "A").desenhar_verso(tela_virtual, self.pos_parceiro[0] + (i * 20), self.pos_parceiro[1], tempo=tempo)
                for i in range(len(self.maos_ia[1])): CartaVisual("Copas", "A").desenhar_verso(tela_virtual, self.pos_adv1[0], self.pos_adv1[1] + (i * 15), rotacionada=True, tempo=tempo)
                for i in range(len(self.maos_ia[3])): CartaVisual("Copas", "A").desenhar_verso(tela_virtual, self.pos_adv2[0], self.pos_adv2[1] + (i * 15), rotacionada=True, tempo=tempo)

                # Desenho do Morto Cruzado
                mx, my = self.pos_morto_base
                pygame.draw.rect(tela_virtual, (15, 70, 30), (mx - 25, my - 15, 145, 145), border_radius=8)
                if self.morto_1: 
                    CartaVisual("Copas", "A").desenhar_verso(tela_virtual, mx - 12, my + 12, rotacionada=True, cor_fundo=COR_VERSO_VERMELHO)
                if self.morto_2: 
                    CartaVisual("Copas", "A").desenhar_verso(tela_virtual, mx, my, rotacionada=False, cor_fundo=COR_VERSO_VERMELHO)

                if self.baralho_reservado:
                    pygame.draw.rect(tela_virtual, COR_VERSO_AZUL, self.rect_monte, border_radius=5)
                    pygame.draw.rect(tela_virtual, COR_VERSO_BORDA, self.rect_monte, 2, border_radius=5)
                    tela_virtual.blit(fonte_p.render(f"MONTE ({len(self.baralho_reservado)})", True, COR_TEXTO), (525, 290))

                selecionadas = [c for c in self.mao_jogador if c.selecionada]
                
                if self.lixo:
                    self.lixo[-1].desenhar_frente(tela_virtual, self.pos_lixo[0], self.pos_lixo[1], tempo=tempo)
                    self.rect_lixo = self.lixo[-1].rect
                    tela_virtual.blit(fonte_p.render(f"LIXO ({len(self.lixo)})", True, COR_TEXTO), (640, 180))

                # --- TRAVA DE SEGURANÇA CONTRA INVASÃO DA MÃO ---
                # A altura máxima da área de jogos agora é restrita rigidamente a 220px (termina em Y=560)
                pygame.draw.rect(tela_virtual, (15, 65, 30), (220, 340, 800, 220), border_radius=8)
                tela_virtual.blit(fonte_p.render("JOGOS NA MESA (Clique em 1 carta da mão e depois no jogo para somar)", True, (200, 255, 200)), (230, 345))
                
                # CORREÇÃO DE EMBALAGEM LATERAL: As cartas agora crescem para a direita (horizontal), nunca invadindo a mão!
                for i_jogo, jogo_lista in enumerate(self.jogos_na_mesa):
                    x_jogo_base = 240 + (i_jogo * 140)
                    for i_carta, card_mesa in enumerate(jogo_lista):
                        x_c = x_jogo_base + (i_carta * 16) # Empilhamento lateral sutil (estilo cascata horizontal)
                        y_c = 375 + (i_carta * 4)          # Queda vertical mínima para manter o efeito tridimensional
                        card_mesa.rect.x = x_c
                        card_mesa.rect.y = y_c
                        card_mesa.desenhar_frente(tela_virtual, x_c, y_c, tempo=0)

                # Botões de Organização
                cor_num = COR_BOTAO_ATIVO if self.modo_organizacao_atual == "numero" else ((50, 130, 200) if self.btn_org_numero.collidepoint(pos_mouse) else (40, 90, 150))
                pygame.draw.rect(tela_virtual, cor_num, self.btn_org_numero, border_radius=4)
                txt_num = fonte_p.render("Org. Número", True, (0,0,0) if self.modo_organizacao_atual == "numero" else COR_TEXTO)
                tela_virtual.blit(txt_num, (self.btn_org_numero.x + (self.btn_org_numero.w//2 - txt_num.get_width()//2), self.btn_org_numero.y + 6))

                cor_np = COR_BOTAO_ATIVO if self.modo_organizacao_atual == "naipe" else ((50, 130, 200) if self.btn_org_naipe.collidepoint(pos_mouse) else (40, 90, 150))
                pygame.draw.rect(tela_virtual, cor_np, self.btn_org_naipe, border_radius=4)
                txt_np = fonte_p.render("Org. Naipe", True, (0,0,0) if self.modo_organizacao_atual == "naipe" else COR_TEXTO)
                tela_virtual.blit(txt_np, (self.btn_org_naipe.x + (self.btn_org_naipe.w//2 - txt_np.get_width()//2), self.btn_org_naipe.y + 6))

                # Área Livre da Mão Protegida
                tela_virtual.blit(fonte_g.render(f"Sua Mão ({len(self.mao_jogador)} cartas)", True, COR_TEXTO), (250, 635))
                for carta in self.mao_jogador: 
                    carta.desenhar_frente(tela_virtual, carta.rect.x, 670, tempo=tempo)

                if self.turno_atual == 0 and self.fase_turno == "MESA_DESCARTE" and len(selecionadas) >= 3:
                    cor_b = COR_BOTAO_HOVER if self.btn_descer_dinamico.collidepoint(pos_mouse) else COR_BOTAO_ATIVO
                    pygame.draw.rect(tela_virtual, cor_b, self.btn_descer_dinamico, border_radius=6)
                    txt_b = fonte_m.render("Baixar Novo Jogo", True, (0,0,0))
                    tela_virtual.blit(txt_b, (self.btn_descer_dinamico.x + (self.btn_descer_dinamico.w//2 - txt_b.get_width()//2), self.btn_descer_dinamico.y + 8))

                for anim in self.animacoes_ativas: anim.desenhar(tela_virtual, tempo)

            tela_atual = pygame.display.get_surface()
            tela_atual.blit(pygame.transform.smoothscale(tela_virtual, (largura_atual, altura_atual)), (0, 0))

            # --- EVENTOS ---
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_F11:
                    self.alternar_tela_cheia()
                    
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if self.animacoes_ativas or self.fase_distribuicao_inicial: continue
                        
                    if self.estado_jogo == "MENU":
                        if self.btn_3000.collidepoint(pos_mouse): self.meta_pontos = 3000
                        elif self.btn_5000.collidepoint(pos_mouse): self.meta_pontos = 5000
                        elif self.btn_8000.collidepoint(pos_mouse): self.meta_pontos = 8000
                        elif self.btn_jogar.collidepoint(pos_mouse): self.iniciar_partida()
                            
                    elif self.estado_jogo == "PARTIDA":
                        if self.btn_org_numero.collidepoint(pos_mouse):
                            self.organizar_por_numero()
                            continue
                        elif self.btn_org_naipe.collidepoint(pos_mouse):
                            self.organizar_por_naipe()
                            continue

                        if self.turno_atual == 0:
                            selecionadas = [c for c in self.mao_jogador if c.selecionada]
                            
                            clicou_carta = False
                            for carta in reversed(self.mao_jogador):
                                if carta.rect.collidepoint(pos_mouse):
                                    carta.selecionada = not carta.selecionada
                                    clicou_carta = True
                                    break
                            if clicou_carta: continue
                            
                            if self.fase_turno == "MESA_DESCARTE" and len(selecionadas) == 1:
                                clicou_jogo_mesa = False
                                for jogo_lista in self.jogos_na_mesa:
                                    for card_mesa in jogo_lista:
                                        if card_mesa.rect.collidepoint(pos_mouse):
                                            carta_mao = selecionadas[0]
                                            
                                            # Executa a Validação de Regra Real antes de aceitar juntar carta ao jogo
                                            if self.validar_adicao_jogo(carta_mao, jogo_lista):
                                                carta_mao.selecionada = False
                                                jogo_lista.append(carta_mao)
                                                # Reordena o jogo na mesa pela sequência para manter bonito
                                                jogo_lista.sort(key=lambda c: c.peso_numerico if c.valor != "2" else 2)
                                                self.mao_jogador.remove(carta_mao)
                                                self.alerta = f"Somou {carta_mao.valor} de {carta_mao.naipe} com sucesso!"
                                                
                                                if len(self.mao_jogador) == 0:
                                                    if self.morto_1:
                                                        self.mao_jogador = self.morto_1[:]
                                                        self.morto_1.clear()
                                                        self.aplicar_auto_organizacao()
                                                    elif self.morto_2:
                                                        self.mao_jogador = self.morto_2[:]
                                                        self.morto_2.clear()
                                                        self.aplicar_auto_organizacao()
                                                
                                                self.atualizar_posicoes_mao()
                                                clicou_jogo_mesa = True
                                                break
                                            else:
                                                self.alerta = "Movimento Inválido! Essa carta não pertence a este jogo/naipe."
                                                clicou_jogo_mesa = True
                                                break
                                    if clicou_jogo_mesa: break
                                if clicou_jogo_mesa: continue

                            if self.fase_turno == "COMPRAR":
                                if self.rect_monte.collidepoint(pos_mouse) and self.baralho_reservado:
                                    nova = self.baralho_reservado.pop()
                                    self.disparar_animacao(nova, self.pos_monte[0], self.pos_monte[1], *self.obter_posicao_final_sua_mao(), mostrar_frente=True)
                                    self.mao_jogador.append(nova)
                                    self.aplicar_auto_organizacao()
                                    self.fase_turno = "MESA_DESCARTE"
                                    self.alerta = "Comprou do monte!"
                                
                                elif self.rect_lixo.collidepoint(pos_mouse):
                                    if self.lixo:
                                        for c in self.mao_jogador: c.selecionada = False
                                        self.alerta = f"Pegou o lixo com {len(self.lixo)} cartas!"
                                        for card_lixo in self.lixo:
                                            self.mao_jogador.append(card_lixo)
                                        self.lixo.clear()
                                        self.aplicar_auto_organizacao()
                                        self.fase_turno = "MESA_DESCARTE"

                            elif self.fase_turno == "MESA_DESCARTE":
                                if self.rect_lixo.collidepoint(pos_mouse) and len(selecionadas) == 1:
                                    card = selecionadas[0]
                                    card.selecionada = False
                                    self.disparar_animacao(card, card.rect.x, card.rect.y, self.pos_lixo[0], self.pos_lixo[1], mostrar_frente=True)
                                    self.mao_jogador.remove(card)
                                    self.lixo.append(card)
                                    self.atualizar_posicoes_mao()
                                    self.turno_atual = 1
                                    self.tempo_acao_ia = 0
                                
                                elif len(selecionadas) >= 3 and self.btn_descer_dinamico.collidepoint(pos_mouse):
                                    # Executa Validação Completa de Sequência e Naipe Único
                                    valido, msg = self.validar_novo_jogo(selecionadas)
                                    if valido:
                                        novo_jogo = []
                                        for c in selecionadas:
                                            c.selecionada = False
                                            novo_jogo.append(c)
                                            self.mao_jogador.remove(c)
                                            
                                        novo_jogo.sort(key=lambda c: c.peso_numerico)
                                        self.jogos_na_mesa.append(novo_jogo)
                                        self.alerta = "Novo jogo descido respeitando o mesmo naipe!"
                                        
                                        if len(self.mao_jogador) == 0:
                                            if self.morto_1:
                                                self.mao_jogador = self.morto_1[:]
                                                self.morto_1.clear()
                                                self.aplicar_auto_organizacao()
                                            elif self.morto_2:
                                                self.mao_jogador = self.morto_2[:]
                                                self.morto_2.clear()
                                                self.aplicar_auto_organizacao()
                                                
                                        self.atualizar_posicoes_mao()
                                    else:
                                        self.alerta = msg

            pygame.display.flip()

if __name__ == "__main__":
    jogo = JogoVisual()
    jogo.run = jogo.rodar()