import pygame
import random
import math

# Inicialização de fontes para as cartas (usadas dentro da classe)
pygame.font.init()
fonte_m = pygame.font.SysFont("Arial", 16, bold=True)

# Cores usadas nas cartas
COR_CARTA = (255, 255, 255)
COR_SELECIONADA = (255, 215, 0)
COR_BLOQUEIO = (220, 50, 50)
COR_VERSO_AZUL = (30, 70, 150)
COR_VERSO_VERMELHO = (180, 40, 40)
COR_VERSO_BORDA = (220, 220, 255)

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