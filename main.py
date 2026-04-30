import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def sfera(kolor):

    # Włączamy pierwszą płaszczyznę obcinania
    glEnable(GL_CLIP_PLANE0)
    glClipPlane(GL_CLIP_PLANE0, (0.0, 0.0, 1.0, 0.0))

    glColor3f(kolor[0]/255, kolor[1]/255, kolor[2]/255)

    # Tworzymy obiekt quadric (podstawa do rysowania kształtów takich jak sfery czy cylindry w OpenGL)
    sfera = gluNewQuadric()
    # Ustawiamy styl rysowania na siatkę (GLU_LINE), dzięki temu łatwiej zauważyć, że to obiekt 3D
    gluQuadricDrawStyle(sfera, GLU_FILL)

    # Generowanie wektorów normalnych (BARDZO WAŻNE DLA ŚWIATŁA!)
    # Bez tego światło nie będzie wiedziało, pod jakim kątem pada na sferę
    gluQuadricNormals(sfera, GLU_SMOOTH)
    
    # Rysujemy sferę: promień 1, 32 podziały wzdłuż, 32 w poprzek
    gluSphere(sfera, 1, 256, 256)#128, 128)

def main():
    pygame.init()
    display = (600, 600)
    
    # Inicjalizacja okna Pygame z flagami dla OpenGL i podwójnego buforowania
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Ustawienie perspektywy: kąt widzenia, proporcje okna, najbliższy i najdalszy plan
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # 1. Włączamy system oświetlenia
    glEnable(GL_LIGHTING)

    # 2. Włączamy domyślne źródło światła nr 0 (świeci z "kamery" w stronę obiektu)
    glEnable(GL_LIGHT0)

    # 3. Włączamy śledzenie kolorów materiału (dzięki temu glColor3f będzie działać ze światłem)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

# ... (reszta pętli głównej) ...
    
    # Przesunięcie "kamery" do tyłu, abyśmy widzieli sferę
    glTranslatef(0.0, 0.0, -5)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        # Czyszczenie ekranu i bufora głębi
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Wywołanie funkcji rysującej sferę
        # kolor wektor 
        
        sfera([50,150,255])
        
        # Aktualizacja ekranu
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
