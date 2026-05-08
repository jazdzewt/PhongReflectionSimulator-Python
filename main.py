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
    # Wektory pomocnicze
    N = wek_norm(pozycja) # Normalna dla sfery w środku (0,0,0) to po prostu pozycja
    L = wek_norm([swiatlo_poz[0] - pozycja[0], swiatlo_poz[1] - pozycja[1], swiatlo_poz[2] - pozycja[2]])
    V = wek_norm([kamera_poz[0] - pozycja[0], kamera_poz[1] - pozycja[1], kamera_poz[2] - pozycja[2]])
    
    # 1. Składowa otoczenia (Ambient): Ia * ka
    # Przyjmujemy Ia jako natężenie koloru bazowego
    ambient = [c * 0.1 for c in material['kolor']]

    # 2. Składowa rozproszona (Diffuse): Ip * kd * (N o L)
    dot_nl = max(il_skal(N, L), 0.0)
    diffuse = [c * dot_nl * material['kd'] for c in material['kolor']]

    # 3. Składowa kierunkowa (Specular): Ip * ks * cos^n(alpha)
    # alpha to kąt między wektorem odbicia R a wektorem do kamery V
    dot_nl_2 = 2.0 * il_skal(N, L)
    R = [dot_nl_2 * N[0] - L[0], dot_nl_2 * N[1] - L[1], dot_nl_2 * N[2] - L[2]]
    R = wek_norm(R)
    
    cos_alpha = max(il_skal(V, R), 0.0)
    spec_math = cos_alpha ** material['n']
    
    # Ip dla odblasku przyjmujemy jako 255 (białe światło punktowe)
    specular = [255 * material['ks'] * spec_math] * 3

    # Sumowanie: I = Ambient + Diffuse + Specular
    r = min(255, max(0, ambient[0] + diffuse[0] + specular[0]))
    g = min(255, max(0, ambient[1] + diffuse[1] + specular[1]))
    b = min(255, max(0, ambient[2] + diffuse[2] + specular[2]))
    
    return (int(r), int(g), int(b))

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