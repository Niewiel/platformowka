import pygame

# zmienne globalne
okno_otwarte = True
plik = 'minion.png'
okno_otwarte = True

# stałe
ROZMIAR = SZEROKOŚĆ, WYSOKOŚĆ = (800, 600)
BIAŁY = pygame.color.THECOLORS['white']
CZARNY = pygame.color.THECOLORS['black']
CIEMNOCZERWONY = pygame.color.THECOLORS['darkred']
CIEMNOZIELONY = pygame.color.THECOLORS['darkgreen']
JASNONIEBISKI = pygame.color.THECOLORS['lightblue']

# ustawienia okna i gry
pygame.init()

ekran = pygame.display.set_mode(ROZMIAR)
pygame.display.set_caption('Gra platformowa.')
zegar = pygame.time.Clock()


# klasy

class Gracz(pygame.sprite.Sprite):
    def __init__(self, plik_obrazu):
        super().__init__()
        self.image = pygame.image.load(plik_obrazu)
        self.rect = self.image.get_rect()


# pętla gry
while okno_otwarte:
    # pętla zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            okno_otwarte = False

        pygame.display.flip()

pygame.quit()