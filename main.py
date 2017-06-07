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
        self.__grawitacja()
        # ruch w pionie
        self.rect.y += self.ruch_y

        lista_platform_trafionych = pygame.sprite.spritecollide(
            self, self.plansza.platformy, False)
        for p in lista_platform_trafionych:
            if self.ruch_y > 0:
                self.rect.bottom = p.rect.top
            if self.ruch_y < 0:
                self.rect.top = p.rect.bottom

            self.ruch_y = 0

            if isinstance(p, RuchomaPlatforma):
                self.rect.x += p.ruch_x

        # ruch w poziomie
        self.rect.x += self.ruch_x

        lista_platform_trafionych = pygame.sprite.spritecollide(
            self, self.plansza.platformy, False)
        for p in lista_platform_trafionych:
            if self.ruch_x > 0:
                self.rect.right = p.rect.left
            if self.ruch_x < 0:
                self.rect.left = p.rect.right

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

    def skok(self):
        self.rect.y += 2
        lista_platform_trafionych = pygame.sprite.spritecollide(
            self, self.plansza.platformy, False)
        self.rect.y -= 2

        if lista_platform_trafionych:
            self.ruch_y = -10

    def __grawitacja(self):
        if self.ruch_y == 0:
            self.ruch_y = 1
        else:
            self.ruch_y += 0.35

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
            if event.key == pygame.K_w:
                self.skok()
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


class RuchomaPlatforma(Platforma):
    def __init__(self, szerokość, wysokość, kolor, plansza):
        super().__init__(szerokość, wysokość, kolor)
        self.ruch_x = 0
        self.ruch_y = 0
        self.granica_top = 0
        self.granica_bottom = 0
        self.granica_left = 0
        self.granica_right = 0
        self.plansza = plansza

    def update(self):
        # ruch prawo/lewo
        self.rect.x += self.ruch_x
        ##        if pygame.sprite.collide_rect(self, self.plansza.gracz):
        ##            if self.ruch_x < 0:
        ##                self.plansza.gracz.rect.right = self.rect.left
        ##            else:
        ##                self.plansza.gracz.rect.left = self.rect.right

        # ruch góra/dół
        self.rect.y += self.ruch_y
        ##        if pygame.sprite.collide_rect(self, self.plansza.gracz):
        ##            if self.ruch_y < 0:
        ##                self.plansza.gracz.rect.bottom = self.rect.top
        ##            else:
        ##                self.plansza.gracz.rect.top = self.rect.bottom

        # sprawdzamy granice ruchu i decydujemy o zmianie kierunku ruchu
        if self.rect.bottom > self.granica_bottom or self.rect.top < self.granica_top:
            self.ruch_y *= -1

        pozycja = self.rect.x - self.plansza.przesunięcie
        if pozycja < self.granica_left or pozycja > self.granica_right:
            self.ruch_x *= -1


class Plansza:
    def __init__(self, gracz):
        self.przesunięcie = 0
        self.gracz = gracz
        self.platformy = pygame.sprite.Group()

    def update(self):
        self.platformy.update()
        self.gracz.update()

        # przesunięcie ekranu gdy gracz jest blisko prawej krawędzi
        if self.gracz.rect.right >= 500:
            odl = self.gracz.rect.right - 500
            self.gracz.rect.right = 500
            self.__przesuń_planszę(-odl)

        # przesunięcie ekranu gdy gracz jest blisko lewej krawędzi
        if self.gracz.rect.left <= 150:
            odl = 150 - self.gracz.rect.left
            self.gracz.rect.left = 150
            self.__przesuń_planszę(odl)

    def draw(self, surface):
        surface.fill(BIAŁY)
        self.platformy.draw(surface)
        self.gracz.draw(surface)

    def __przesuń_planszę(self, wartość):
        self.przesunięcie += wartość

        for p in self.platformy:
            p.rect.x += wartość


class Plansza_1(Plansza):
    def __init__(self, gracz):
        super().__init__(gracz)

        ws_platform = [[500, 5, 0, WYSOKOŚĆ - 5], [200, WYSOKOŚĆ - 5, -100, 0],
                       [200, 50, 300, 450], [200, 50, 600, 350],
                       [200, 50, 300, 150], [200, 50, 850, 250]]

        for p in ws_platform:
            platforma = Platforma(p[0], p[1], CIEMNOZIELONY)
            platforma.rect.x = p[2]
            platforma.rect.y = p[3]
            self.platformy.add(platforma)

        # tworzymy ruchomą platformę (w pionie)
        rp = RuchomaPlatforma(100, 50, CIEMNOCZERWONY, self)
        rp.ruch_y = 1
        rp.granica_top = 150
        rp.granica_bottom = 500
        rp.rect.x = 500
        rp.rect.y = 300
        self.platformy.add(rp)

        # tworzymy ruchomą platformę (w poziomie)
        rp1 = RuchomaPlatforma(100, 50, CIEMNOCZERWONY, self)
        rp1.ruch_x = 1
        rp1.granica_left = 1000
        rp1.granica_right = 1400
        rp1.rect.x = 1000
        rp1.rect.y = 300
        self.platformy.add(rp1)


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
        else:
            gracz.obsługa_zdarzeń(event)

    aktualna_plansza.draw(ekran)
    aktualna_plansza.update()

    pygame.display.flip()
    zegar.tick(30)

pygame.quit()