import pygame
import trimesh
import math
import sys


def wektor_odejmij(v1, v2):
    return [v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]]

def wektor_dlugosc(v):
    return math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)

def wektor_znormalizuj(v):
    dl = wektor_dlugosc(v)
    return [v[0]/dl, v[1]/dl, v[2]/dl] if dl > 0 else [0, 0, 0]

def iloczyn_skalarny(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2]

def wektor_odbicia(L, N):
    dot = iloczyn_skalarny(L, N)
    return [2 * dot * N[0] - L[0], 2 * dot * N[1] - L[1], 2 * dot * N[2] - L[2]]

def oblicz_kolor_phong(pozycja, normalna, poz_swiatla, poz_kamery, kolor_bazy):
    ambient = [c * 0.1 for c in kolor_bazy]

    N = wektor_znormalizuj(normalna)
    L = wektor_znormalizuj(wektor_odejmij(poz_swiatla, pozycja))
    sila_diffuse = max(iloczyn_skalarny(N, L), 0.0)
    diffuse = [c * sila_diffuse for c in kolor_bazy]

    V = wektor_znormalizuj(wektor_odejmij(poz_kamery, pozycja))
    R = wektor_odbicia(L, N)
    spec_math = max(iloczyn_skalarny(V, R), 0.0) ** 16.0
    specular = [255 * 0.8 * spec_math] * 3 

    return (
        min(255, max(0, ambient[0] + diffuse[0] + specular[0])),
        min(255, max(0, ambient[1] + diffuse[1] + specular[1])),
        min(255, max(0, ambient[2] + diffuse[2] + specular[2]))
    )

def rzutuj_3d_na_2d(x, y, z, width, height, fov=600):
    if z <= 0.1:
        z = 0.1
    factor = fov / z
    x_2d = (x * factor) + (width / 2)
    y_2d = -(y * factor) + (height / 2) 
    return (x_2d, y_2d)



mesh = trimesh.creation.icosphere(subdivisions=5, radius=1.5)
wierzcholki = mesh.vertices.tolist()
trojkaty = mesh.faces.tolist()
normalne = mesh.face_normals.tolist()

def przygotuj_poligony(kolor, poz_swiatla, poz_sfery_z):
    poz_kamery = [0, 0, 0]
    poligony = []

    for idx, trojkat in enumerate(trojkaty):
        v1 = wierzcholki[trojkat[0]]
        v2 = wierzcholki[trojkat[1]]
        v3 = wierzcholki[trojkat[2]]

        v1_z = [v1[0], v1[1], v1[2] + poz_sfery_z]
        v2_z = [v2[0], v2[1], v2[2] + poz_sfery_z]
        v3_z = [v3[0], v3[1], v3[2] + poz_sfery_z]

        srodek = [
            (v1_z[0]+v2_z[0]+v3_z[0])/3, 
            (v1_z[1]+v2_z[1]+v3_z[1])/3, 
            (v1_z[2]+v2_z[2]+v3_z[2])/3
        ]

        norm = normalne[idx]
        kolor_poly = oblicz_kolor_phong(srodek, norm, poz_swiatla, poz_kamery, kolor)
        
        poligony.append({
            "z": srodek[2],
            "kolor": kolor_poly,
            "wierzcholki": [v1_z, v2_z, v3_z]
        })

    return poligony

def main():

    pygame.init()

    szerokosc = 600
    wysokosc = 600

    ekran = pygame.display.set_mode((szerokosc, wysokosc))
    zegar = pygame.time.Clock()

    light_z = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        ekran.fill((0, 0, 0)) 

        mouse_x, mouse_y = pygame.mouse.get_pos()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: 
            light_z = light_z + 0.1 
        if keys[pygame.K_s]: 
            light_z = light_z - 0.1 

        czulosc = 100.0 
        light_x = (mouse_x - szerokosc / 2) / czulosc
        light_y = -(mouse_y - wysokosc / 2) / czulosc 
        
        light_z = light_z

        poligony = przygotuj_poligony([50, 150, 255], [light_x, light_y, light_z], poz_sfery_z=5.0)

        poligony.sort(key=lambda p: p["z"], reverse=True)

        for poly in poligony:
            punkty_2d = []
            for v in poly["wierzcholki"]:
                p2d = rzutuj_3d_na_2d(v[0], v[1], v[2], szerokosc, wysokosc)
                punkty_2d.append(p2d)
            
            pygame.draw.polygon(ekran, poly["kolor"], punkty_2d)

        pygame.display.flip()
        zegar.tick(60)

if __name__ == '__main__':
    main()