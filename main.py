import pygame
import math
import sys

def wek_norm(wektor):
    dl = math.sqrt(wektor[0]**2 + wektor[1]**2 + wektor[2]**2)

    n = [0, 0, 0]

    n[0] = wektor[0] / dl
    n[1] = wektor[1] / dl
    n[2] = wektor[2] / dl
    
    return n

def il_skal(wektor1, wektor2):

    x = wektor1[0] * wektor2[0] + wektor1[1] * wektor2[1] + wektor1[2] * wektor2[2]

    return x

def phong(pozycja, material, swiatlo_poz, kamera_poz):

    kolor_r = material['kolor'][0]
    kolor_g = material['kolor'][1]
    kolor_b = material['kolor'][2]

    wektor_pow = wek_norm(pozycja)
    
    wektor_swiatlo = wek_norm([swiatlo_poz[0] - pozycja[0], swiatlo_poz[1] - pozycja[1], swiatlo_poz[2] - pozycja[2]])
                                    
    wektor_kamera = wek_norm([kamera_poz[0] - pozycja[0], kamera_poz[1] - pozycja[1], kamera_poz[2] - pozycja[2]])

    kat_padania = max(il_skal(wektor_pow, wektor_swiatlo), 0.0)
    swiatlo_rozproszone = kat_padania * material['kd']


    x = 2.0 * il_skal(wektor_pow, wektor_swiatlo)
    kierunek_odbicia = wek_norm([x * wektor_pow[0] - wektor_swiatlo[0], x * wektor_pow[1] - wektor_swiatlo[1], x * wektor_pow[2] - wektor_swiatlo[2]])
    
    odbicie = max(il_skal(wektor_kamera, kierunek_odbicia), 0.0)

    odblask = odbicie ** material['n']
    swiatlo_odblasku = odblask * material['ks']

    sila_bazy = 0.1 + swiatlo_rozproszone
    
    r = (kolor_r * sila_bazy) + (255 * swiatlo_odblasku)
    g = (kolor_g * sila_bazy) + (255 * swiatlo_odblasku)
    b = (kolor_b * sila_bazy) + (255 * swiatlo_odblasku)

    r_koncowe = min(255, max(0, int(r)))
    g_koncowe = min(255, max(0, int(g)))
    b_koncowe = min(255, max(0, int(b)))
    
    return (r_koncowe, g_koncowe, b_koncowe)


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
    wybrany_material = materialy[1]

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