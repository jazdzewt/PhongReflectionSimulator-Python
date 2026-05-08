import pygame
import math
import sys

from phong import phong

def main():
    pygame.init()
    
    font = pygame.font.SysFont(None, 30)

    szerokosc_okna = 500
    wysokosc_okna = 600

    ekran = pygame.display.set_mode((szerokosc_okna, wysokosc_okna))
    zegar = pygame.time.Clock()

    materialy = [
    {'nazwa': 'Kreda', 'kd': 1.0, 'ks': 0.0, 'n': 1.0, 'kolor': [255, 255, 255]},
    {'nazwa': 'Drewno', 'kd': 0.8, 'ks': 0.4, 'n': 20.0, 'kolor': [173, 73, 36]},
    {'nazwa': 'Plastik', 'kd': 0.5, 'ks': 0.75, 'n': 90.0, 'kolor': [158, 66, 255]},
    {'nazwa': 'Lustro', 'kd': 0.2, 'ks': 1.0, 'n': 250.0, 'kolor': [186, 213, 227]}]

    przyciski = [
        (pygame.Rect(10, 540, 100, 30), "Kreda", 0), 
        (pygame.Rect(120, 540, 100, 30), "Drewno", 1),
        (pygame.Rect(230, 540, 100, 30), "Plastik", 2),
        (pygame.Rect(340, 540, 100, 30), "Lustro", 3)]

    promien = 150
    srodek_x = szerokosc_okna // 2
    srodek_y = wysokosc_okna // 2
    kolor_bazy = [50, 150, 255]
    wybrany_material = materialy[0]

    swiatlo_z = 200.0 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    for rect, tekst, indeks in przyciski:
                        if rect.collidepoint(event.pos):
                            wybrany_material = materialy[indeks]

        ekran.fill((0, 0, 0)) 
        x_myszka, y_myszka = pygame.mouse.get_pos()
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]: 
            if swiatlo_z < 500.0:
                swiatlo_z = swiatlo_z + 5.0 

        if keys[pygame.K_s]: 
            if swiatlo_z > -500.0:
                swiatlo_z = swiatlo_z - 5.0

        swiatlo_x = x_myszka - srodek_x
        swiatlo_y = y_myszka - srodek_y

        poz_swiatla = [swiatlo_x, swiatlo_y, swiatlo_z]

        poz_kamery = [0, 0, 1000]

        odleglosc_swiatla = math.sqrt(swiatlo_x**2 + swiatlo_y**2 + swiatlo_z**2)
        
        pixele = pygame.PixelArray(ekran)

        promien2 = promien**2

        for y in range(-promien, promien):

            y2 = y**2

            for x in range(-promien, promien):

                x2 = x**2

                if x2 + y2 <= promien2:

                    z = math.sqrt(promien2 - x2 - y2)

                    pozycja = [x, y, z]
                    
                    kolor = phong(pozycja, wybrany_material, poz_swiatla, poz_kamery)

                    pixele[srodek_x + x, srodek_y + y] = kolor
                    
        pixele.close()

        tekst_z = f"Wspolrzedna Z: {swiatlo_z:.2f}"
        tekst_ekran_z = font.render(tekst_z, True, (255, 255, 255))
        ekran.blit(tekst_ekran_z, (250, 10))


        for rect, tekst, indeks in przyciski:
            kolor_przycisku = (150, 150, 150) 
            pygame.draw.rect(ekran, kolor_przycisku, rect)
            
            tekst_kon = font.render(tekst, True, (255, 255, 255))
            tekst_x = rect.x + (rect.width - tekst_kon.get_width()) // 2
            tekst_y = rect.y + (rect.height - tekst_kon.get_height()) // 2

            ekran.blit(tekst_kon, (tekst_x, tekst_y))

        pygame.display.flip()
        
if __name__ == '__main__':
    main()