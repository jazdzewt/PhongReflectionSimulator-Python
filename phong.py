import math 

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