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
        self.ruch_x = 0
        self.ruch_y = 0
        self.plansza = None
        self.kierunek = 'RIGHT'

    def update(self):
        # ruch w pionie
        self.rect.y += self.ruch_y
        lista_trafionych = pygame.sprite.spritecollide(self, self.plansza.platformy, False)
        for p in lista_trafionych:
            if self.ruch_y > 0:
                self.rect.bottom = p.rect.top
            if self.ruch_y < 0:
                self.rect.top = p.rect.bottom

            self.ruch_y = 0

        # ruch w poziomie
        self.rect.x += self.ruch_x
        lista_trafionych = pygame.sprite.spritecollide(self, self.plansza.platformy, False)
        for p in lista_trafionych:
            if self.ruch_x>0:
                pass
            if self.ruch_x<0:
                pass

    def skok(self):
        self.rect.y+=2


    def lewo(self):
        self.ruch_x = -6
        if self.kierunek == 'RIGHT':
            self.image = pygame.transform.flip(self.image, True, False)
            self.kierunek = 'LEFT'

    def prawo(self):
        self.ruch_x = 6
        if self.kierunek == 'LEFT':
            self.image = pygame.transform.flip(self.image, True, False)
            self.kierunek = 'RIGHT'

    def stop(self):
        self.ruch_x = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def obsługa_zdarzeń(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.prawo()
            if event.key == pygame.K_a:
                self.lewo()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d and self.ruch_x > 0:
                self.stop()
            if event.key == pygame.K_a and self.ruch_x < 0:
                self.stop()


class Platforma(pygame.sprite.Sprite):
    def __init__(self, szerokość, wysokość, kolor):
        super().__init__()
        self.szerokość = szerokość
        self.wysokość = wysokość
        self.kolor = kolor
        self.image = pygame.Surface([self.szerokość, self.wysokość])
        self.rect = self.image.get_rect()
        self.image.fill(self.kolor)


class Plansza:
    def __init__(self, gracz):
        self.gracz = gracz
        self.platformy = pygame.sprite.Group()

    def update(self):
        self.platformy.update()
        self.gracz.update()

        if self.gracz.rect.right >=500:
            odl =self.gracz.rect.right-500
            self.gracz.rect.right=500

    def draw(self, surface):
        surface.fill(BIAŁY)
        self.platformy.draw(surface)
        self.gracz.draw(surface)


class Plansza_1(Plansza):
    def __init__(self, gracz):
        super().__init__(gracz)

        ws_platform = [[500, 5, 0, WYSOKOŚĆ - 5]]

        for p in ws_platform:
            platforma = Platforma(p[0], p[1], CIEMNOZIELONY)
            platforma.rect.x = p[2]
            platforma.rect.y = p[3]
            self.platformy.add(platforma)


# konkretyzacja obiektów
gracz = Gracz(plik)
gracz.rect.left = 150
gracz.rect.bottom = WYSOKOŚĆ - 5
aktualna_plansza = Plansza_1(gracz)
gracz.plansza = aktualna_plansza

# pętla gry
while okno_otwarte:
    # pętla zdarzeń
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            okno_otwarte = False

    aktualna_plansza.draw(ekran)
    aktualna_plansza.update()

    pygame.display.flip()
    zegar.tick(30)

pygame.quit()
