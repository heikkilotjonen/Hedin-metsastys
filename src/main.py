import pygame
import random

class RoboPeli:
    def __init__(self):
        pygame.init()
        self.kello = pygame.time.Clock()

        #MUSIIKKI
        pygame.mixer.init()

        self.playlist = [
            "easterpink.mp3",
            "wenotlikeyou.mp3"]
        
        self.current_track = 0

        self.MUSIC_END = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.MUSIC_END)

        pygame.mixer.music.load(self.playlist[self.current_track])
        pygame.mixer.music.play()
        #MUSIIKKI

        self.taustat = ["tausta.png", "tausta2.png"]

        self.tausta = pygame.image.load("tausta.png")
        self.tausta2 = pygame.image.load("tausta2.png")
        self.robo = pygame.image.load("robo.png")
        self.kolikko = pygame.image.load("kolikko.png")
        self.ovi = pygame.image.load("ovi.png")
        self.hirviö = pygame.image.load("hirvio.png")

        self.leveys = self.robo.get_width()
        self.korkeus = self.robo.get_height()
        self.kleveys = self.kolikko.get_width()
        self.kkorkeus = self.kolikko.get_height()
        self.oven_leveys = self.ovi.get_width()
        self.oven_korkeus = self.ovi.get_height()
        self.hirviön_leveys = self.hirviö.get_width()
        self.hirviön_korkeus = self.hirviö.get_height()

        self.hirviö_x = random.randint((0+self.hirviön_leveys), 220)
        self.hirviö_y = random.randint((0+self.hirviön_korkeus), 140)

        self.outline = pygame.font.SysFont("Georgia", 61)
        self.fontti = pygame.font.SysFont("Georgia", 60)
        self.poutline = pygame.font.SysFont("Arial", 31)
        self.pienempi_fontti = pygame.font.SysFont("Arial", 30)

        self.voitto_teksti = self.fontti.render("Nettspend sai hedit", True, (0, 0, 255))
        self.vohjeet_teksti = self.pienempi_fontti.render("F2 yrittääkseen uutta keissiä", True, (0, 0, 255))
        self.vpoistu_teksti = self.pienempi_fontti.render("ESC poistuaksesi", True, (0, 0, 255))

        self.häviö_teksti = self.fontti.render("Fakemink juggasi sinut", True, (255, 0, 0))
        self.ohjeet_teksti = self.pienempi_fontti.render("F2 yrittääkseen uutta keissiä", True, (255, 0, 0))
        self.poistu_teksti = self.pienempi_fontti.render("ESC poistuaksesi", True, (255, 0, 0))

        self.nayton_leveys = 1600
        self.nayton_korkeus = 920

        self.nayttö  = pygame.display.set_mode((self.nayton_leveys, self.nayton_korkeus))
        pygame.display.set_caption("Hedin metsästys")
        pygame.display.flip()

        #TAUSTAKUVAT
        self.taustat = ["tausta.png", "tausta2.png"]
        self.tausta_indeksi = 0
        self.taustakuvat = [pygame.image.load(t) for t in self.taustat]
        self.tausta = pygame.transform.scale(self.taustakuvat[self.tausta_indeksi], (self.nayton_leveys, self.nayton_korkeus))
        #TAUSTAKUVAT

        self.uusi_peli()

    def piirra_teksti_outline(self, fontti, teksti, vari, outline_vari, center, outline_paksuus=2):
        """Piirtää tekstin mustalla reunuksella."""
        text_surface = fontti.render(teksti, True, vari)
        outline_surface = fontti.render(teksti, True, outline_vari)
        text_rect = text_surface.get_rect(center=center)

        for dx in range(-outline_paksuus, outline_paksuus + 1):
            for dy in range(-outline_paksuus, outline_paksuus + 1):
                if dx != 0 or dy != 0:
                    outline_rect = outline_surface.get_rect(center=(center[0] + dx, center[1] + dy))
                    self.nayttö.blit(outline_surface, outline_rect)

        self.nayttö.blit(text_surface, text_rect)

    def silmukka(self):
        while True:
            self.kello.tick(60)
            self.tutki_tapahtumat()
            self.liiku()
            self.kolikko_löydetty()
            self.onko_karattu()
            self.saatiinko_kiinni()

            pygame.display.flip()
                

    def uusi_peli(self):
        self.ylös = False
        self.alas = False
        self.oikealle = False
        self.vasemmalle = False
        self.ovi_auki = False
        self.karattu = False
        self.kiinni = False

        self.x = 10
        self.y = 10

        self.kolikon_sijainti_x = random.randint(500, (self.nayton_leveys - self.kleveys))
        self.kolikon_sijainti_y = random.randint(340, (self.nayton_korkeus - self.kkorkeus))

        self.oven_sijainti_x = random.randint((0+self.oven_leveys), 220)
        self.oven_sijainti_y = random.randint((0+self.oven_korkeus), 140)

        self.lataa_robo()
        self.lataa_kolikko()
        self.silmukka()

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = True
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = True
                if tapahtuma.key == pygame.K_UP:
                    self.ylös = True
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = True
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_F3:
                    self.tausta_indeksi = (self.tausta_indeksi + 1) % len(self.taustakuvat)
                    self.tausta = pygame.transform.scale(self.taustakuvat[self.tausta_indeksi], (self.nayton_leveys, self.nayton_korkeus))
                    self.uusi_peli()
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()

            if tapahtuma.type == pygame.KEYUP:
                if tapahtuma.key == pygame.K_LEFT:
                    self.vasemmalle = False
                if tapahtuma.key == pygame.K_RIGHT:
                    self.oikealle = False
                if tapahtuma.key == pygame.K_UP:
                    self.ylös = False
                if tapahtuma.key == pygame.K_DOWN:
                    self.alas = False

            if tapahtuma.type == self.MUSIC_END:

                self.current_track = (self.current_track + 1) % len(self.playlist)
                seuraava = self.playlist[self.current_track]

                pygame.mixer.music.load(seuraava)
                pygame.mixer.music.play()


            if tapahtuma.type == pygame.QUIT:
                exit()

    def liiku(self):
        if self.karattu:
            self.nayttö.blit(self.tausta, (0, 0))
            self.nayttö.blit(self.ovi, (self.oven_sijainti_x, self.oven_sijainti_y))
            self.nayttö.blit(self.hirviö, (self.hirviö_x, self.hirviö_y))
            self.nayttö.blit(self.robo, (self.x, self.y))

            self.piirra_teksti_outline(self.fontti, "Nettspend sai hedit", (0, 0, 255), (0, 0, 0),
                                       (self.nayton_leveys/2, self.nayton_korkeus/2 - 40))
            self.piirra_teksti_outline(self.pienempi_fontti, "F2 yrittääkseen uutta keissiä", (0, 0, 255), (0, 0, 0),
                                       (self.nayton_leveys/2, self.nayton_korkeus/2 + 20))
            self.piirra_teksti_outline(self.pienempi_fontti, "ESC poistuaksesi", (0, 0, 255), (0, 0, 0),
                                       (self.nayton_leveys/2, self.nayton_korkeus/2 + 60))
            return

        if self.kiinni:
            self.nayttö.blit(self.tausta, (0, 0))
            self.nayttö.blit(self.ovi, (self.oven_sijainti_x, self.oven_sijainti_y))
            self.nayttö.blit(self.hirviö, (self.hirviö_x, self.hirviö_y))
            self.nayttö.blit(self.robo, (self.x, self.y))

            self.piirra_teksti_outline(self.fontti, "Fakemink juggasi sinut", (255, 0, 0), (0, 0, 0),
                                       (self.nayton_leveys/2, self.nayton_korkeus/2 - 40))
            self.piirra_teksti_outline(self.pienempi_fontti, "F2 yrittääkseen uutta keissiä", (255, 0, 0), (0, 0, 0),
                                       (self.nayton_leveys/2, self.nayton_korkeus/2 + 20))
            self.piirra_teksti_outline(self.pienempi_fontti, "ESC poistuaksesi", (255, 0, 0), (0, 0, 0),
                                       (self.nayton_leveys/2, self.nayton_korkeus/2 + 60))
            return
        
        pelaajan_nopeus = 4

        if self.ylös:
            if self.y > 0:
                self.y -= pelaajan_nopeus
            else:
                self.y = 0
        if self.alas:
            if self.y + self.korkeus < self.nayton_korkeus:
                self.y += pelaajan_nopeus
            else:
                self.y = self.nayton_korkeus - self.korkeus     
        if self.oikealle:
            if self.x + self.leveys < self.nayton_leveys:
                self.x += pelaajan_nopeus
            else:
                self.x = self.nayton_leveys - self.leveys
        if self.vasemmalle:
            if self.x > 0:
                self.x -= pelaajan_nopeus
            else:
                self.x = 0
        self.nayttö.blit(self.tausta, (0, 0))
        self.nayttö.blit(self.kolikko, (self.kolikon_sijainti_x, self.kolikon_sijainti_y))
        self.nayttö.blit(self.robo, (self.x, self.y))
        if self.ovi_auki == True:
            self.ovi_aukeaa()
            self.lataa_hirviö()
            self.hirviö_liikkuu()
    

    def kolikko_löydetty(self):
        if (self.kolikon_sijainti_x <= self.x <= self.kolikon_sijainti_x + self.kleveys or 
            self.kolikon_sijainti_x <= self.x + self.leveys <= self.kolikon_sijainti_x + self.kleveys) and (
            self.kolikon_sijainti_y <= self.y <= self.kolikon_sijainti_y + self.kkorkeus or 
            self.kolikon_sijainti_y <= self.y + self.korkeus <= self.kolikon_sijainti_y + self.kleveys):
            self.kolikon_sijainti_x = -100
            self.kolikon_sijainti_y = -100
            self.ovi_auki = True

    def onko_karattu(self):
        if self.ovi_auki == True:
            if (self.oven_sijainti_x <= self.x <= self.oven_sijainti_x + self.oven_leveys or 
                self.oven_sijainti_x <= self.x + self.leveys <= self.oven_sijainti_x + self.oven_leveys) and (
                self.oven_sijainti_y <= self.y <= self.oven_sijainti_y + self.oven_korkeus or 
                self.oven_sijainti_y <= self.y + self.korkeus <= self.oven_sijainti_y + self.oven_korkeus):
                self.karattu = True

    def saatiinko_kiinni(self):
        if self.ovi_auki == True:
            if (self.x <= self.hirviö_x <= self.x + self.leveys or 
                self.x<= self.hirviö_x + self.hirviön_leveys <= self.x + self.leveys) and (
                self.y <= self.hirviö_y <= self.y + self.leveys or 
                self.y <= self.hirviö_y + self.hirviön_leveys <= self.y + self.leveys):
                self.kiinni = True

    def ovi_aukeaa(self):
        self.nayttö.blit(self.ovi, (self.oven_sijainti_x, self.oven_sijainti_y))

    def lataa_robo(self):
        self.nayttö.blit(self.robo, (self.x, self.y))

    def lataa_kolikko(self):
        self.nayttö.blit(self.kolikko, (self.kolikon_sijainti_x, self.kolikon_sijainti_y))

    def lataa_hirviö(self):
        self.nayttö.blit(self.hirviö, (-1000, -1000))

    def hirviö_liikkuu(self):

        hirvion_nopeus = 3.12

        self.nayttö.blit(self.hirviö, (self.hirviö_x, self.hirviö_y))
        if self.karattu:
            return
        if self.hirviö_x > self.x:
            self.hirviö_x -= hirvion_nopeus
        if self.hirviö_x < self.x:
           self.hirviö_x += hirvion_nopeus
        if self.hirviö_y > self.y:
            self.hirviö_y -= hirvion_nopeus
        if self.hirviö_y< self.y:
            self.hirviö_y += hirvion_nopeus

if __name__ == "__main__":
    RoboPeli()