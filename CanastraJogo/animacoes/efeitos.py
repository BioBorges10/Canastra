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