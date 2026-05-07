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

def phong(pozycja, normalna, swiatlo_poz, kamera_poz, material, kolor):
    N = wek_norm(normalna)
    L = wek_norm([swiatlo_poz[0] - pozycja[0], swiatlo_poz[1] - pozycja[1], swiatlo_poz[2] - pozycja[2]])
    V = wek_norm([kamera_poz[0] - pozycja[0], kamera_poz[1] - pozycja[1], kamera_poz[2] - pozycja[2]])
    
    ambient = [c * 0.1 for c in kolor]

    dot_nl = max(il_skal(N, L), 0.0)
    diffuse = [c * dot_nl * material['diffuse'] for c in kolor]

    dot_nl_2 = 2.0 * il_skal(N, L)
    R = [dot_nl_2 * N[0] - L[0], dot_nl_2 * N[1] - L[1], dot_nl_2 * N[2] - L[2]]
    R = wek_norm(R)
    
    spec_math = max(il_skal(V, R), 0.0) ** material['shininess']
    specular = [255 * material['specular'] * spec_math] * 3

    r = min(255, max(0, ambient[0] + diffuse[0] + specular[0]))
    g = min(255, max(0, ambient[1] + diffuse[1] + specular[1]))
    b = min(255, max(0, ambient[2] + diffuse[2] + specular[2]))
    
    return (int(r), int(g), int(b))


materialy = {
    pygame.K_1: {'nazwa': '1. Matowy (Kreda)',      'diffuse': 0.9, 'specular': 0.0, 'shininess': 1.0},
    pygame.K_2: {'nazwa': '2. Drewno (Pól-mat)',    'diffuse': 0.7, 'specular': 0.3, 'shininess': 16.0},
    pygame.K_3: {'nazwa': '3. Plastik (Blyszczacy)','diffuse': 0.8, 'specular': 0.8, 'shininess': 64.0},
    pygame.K_4: {'nazwa': '4. Lustro (Metal)',      'diffuse': 0.2, 'specular': 1.0, 'shininess': 256.0}
}


def main():
    pygame.init()
    
    # Czcionki - Twoja do Z i druga do materiałów
    font = pygame.font.SysFont(None, 30)
    czcionka_mat = pygame.font.SysFont("Arial", 16)

    szerokosc = 600
    wysokosc = 600

    ekran = pygame.display.set_mode((szerokosc, wysokosc))
    pygame.display.set_caption("Matematyczna Sfera - Model Phonga (Klawisze: W/S oraz 1-4)")
    zegar = pygame.time.Clock()

    # Ustawienie sfery na ekranie
    R = 150 # Promień
    srodek_x, srodek_y = szerokosc // 2, wysokosc // 2
    kolor_bazy = [50, 150, 255]
    aktywny_material = materialy[pygame.K_3]

    # Początkowa wartość światła
    light_z = 10.0 
    wspolrzedne = light_z - 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Przełączanie materiałów
            if event.type == pygame.KEYDOWN:
                if event.key in materialy:
                    aktywny_material = materialy[event.key]

        ekran.fill((0, 0, 0)) 

        # --- TWOJA LOGIKA STEROWANIA ---
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # Aktualizacja zmiennej pomocniczej do limitów
        wspolrzedne = light_z - 5 

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: 
            if wspolrzedne < 25.0:
                light_z = light_z + 0.5 
        if keys[pygame.K_s]: 
            if wspolrzedne > -25.0:
                light_z = light_z - 0.5

        czulosc = 100.0 
        light_x = (mouse_x - szerokosc / 2) / czulosc
        light_y = (mouse_y - wysokosc / 2) / czulosc 
        
        # SKALOWANIE DO PRZESTRZENI PIKSELI 
        # Z powrotem zmieniamy małe wartości na dziesiątki pikseli
        swiatlo_x = light_x * czulosc
        swiatlo_y = light_y * czulosc
        swiatlo_z = light_z * 20.0 

        poz_swiatla = [swiatlo_x, swiatlo_y, swiatlo_z]
        poz_kamery = [0, 0, 1000] # Kamera wisi w kosmosie przed ekranem

        odleglosc_swiatla = math.sqrt(swiatlo_x**2 + swiatlo_y**2 + swiatlo_z**2)
        
        # --- RYSOWANIE MATEMATYCZNEJ SFERY ---
        pixele = pygame.PixelArray(ekran)
        for y in range(-R, R):
            for x in range(-R, R):
                if x**2 + y**2 <= R**2:
                    z = math.sqrt(R**2 - x**2 - y**2)
                    normalna = [x, y, z]
                    pozycja = [x, y, z]
                    
                    kolor = phong(pozycja, normalna, poz_swiatla, poz_kamery, aktywny_material, [50, 150, 255])
                    pixele[srodek_x + x, srodek_y + y] = kolor
                    
        pixele.close()

        # --- WYŚWIETLANIE TEKSTÓW ---
        # 1. Twój tekst ze współrzędną Z
        tekst_z = f"Wspolrzedna Z: {odleglosc_swiatla:.2f}"
        tekst_ekran_z = font.render(tekst_z, True, (255, 255, 255))
        ekran.blit(tekst_ekran_z, (350, 10))

        # 2. Informacje o materiałach
        tekst_mat1 = czcionka_mat.render(f"Aktywny materiał: {aktywny_material['nazwa']}", True, (255, 255, 255))
        tekst_mat2 = czcionka_mat.render("Nacisnij 1, 2, 3, 4 aby zmienic material", True, (200, 200, 200))
        ekran.blit(tekst_mat1, (10, 10))
        ekran.blit(tekst_mat2, (10, 30))

        pygame.display.flip()
        
if __name__ == '__main__':
    main()