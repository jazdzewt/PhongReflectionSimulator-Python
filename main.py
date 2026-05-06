import pygame
import math
import sys

# =========================================================
# 1. RĘCZNY MODEL PHONGA (CZYSTA MATEMATYKA)
# =========================================================
def wektor_dlugosc(v):
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

def wektor_znormalizuj(v):
    dl = wektor_dlugosc(v)
    return [v[0]/dl, v[1]/dl, v[2]/dl] if dl > 0 else [0, 0, 0]

def iloczyn_skalarny(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def oblicz_kolor(pozycja, normalna, swiatlo_poz, kamera_poz, kolor_bazy, material):
    N = wektor_znormalizuj(normalna)
    L = wektor_znormalizuj([swiatlo_poz[0] - pozycja[0], swiatlo_poz[1] - pozycja[1], swiatlo_poz[2] - pozycja[2]])
    V = wektor_znormalizuj([kamera_poz[0] - pozycja[0], kamera_poz[1] - pozycja[1], kamera_poz[2] - pozycja[2]])
    
    ambient = [c * 0.1 for c in kolor_bazy]

    dot_nl = max(iloczyn_skalarny(N, L), 0.0)
    diffuse = [c * dot_nl * material['diffuse'] for c in kolor_bazy]

    dot_nl_2 = 2.0 * iloczyn_skalarny(N, L)
    R = [dot_nl_2 * N[0] - L[0], dot_nl_2 * N[1] - L[1], dot_nl_2 * N[2] - L[2]]
    R = wektor_znormalizuj(R)
    
    spec_math = max(iloczyn_skalarny(V, R), 0.0) ** material['shininess']
    specular = [255 * material['specular'] * spec_math] * 3

    r = min(255, max(0, ambient[0] + diffuse[0] + specular[0]))
    g = min(255, max(0, ambient[1] + diffuse[1] + specular[1]))
    b = min(255, max(0, ambient[2] + diffuse[2] + specular[2]))
    
    return (int(r), int(g), int(b))


# =========================================================
# 2. DEFINICJE MATERIAŁÓW Z ZADANIA
# =========================================================
materialy = {
    pygame.K_1: {'nazwa': '1. Matowy (Kreda)',      'diffuse': 0.9, 'specular': 0.0, 'shininess': 1.0},
    pygame.K_2: {'nazwa': '2. Drewno (Pól-mat)',    'diffuse': 0.7, 'specular': 0.3, 'shininess': 16.0},
    pygame.K_3: {'nazwa': '3. Plastik (Blyszczacy)','diffuse': 0.8, 'specular': 0.8, 'shininess': 64.0},
    pygame.K_4: {'nazwa': '4. Lustro (Metal)',      'diffuse': 0.2, 'specular': 1.0, 'shininess': 256.0}
}


# =========================================================
# 3. GŁÓWNA PĘTLA
# =========================================================
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

        ekran.fill((20, 25, 30)) 

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
        
        # --- RYSOWANIE MATEMATYCZNEJ SFERY ---
        pixele = pygame.PixelArray(ekran)
        for y in range(-R, R):
            for x in range(-R, R):
                if x**2 + y**2 <= R**2:
                    z = math.sqrt(R**2 - x**2 - y**2)
                    normalna = [x, y, z]
                    pozycja = [x, y, z]
                    
                    kolor = oblicz_kolor(pozycja, normalna, poz_swiatla, poz_kamery, kolor_bazy, aktywny_material)
                    pixele[srodek_x + x, srodek_y + y] = kolor
                    
        pixele.close()

        # --- WYŚWIETLANIE TEKSTÓW ---
        # 1. Twój tekst ze współrzędną Z
        tekst_z = f"Wspolrzedna Z: {wspolrzedne:.2f}"
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