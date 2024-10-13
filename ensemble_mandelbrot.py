import pygame as py
import math
import numpy as np

py.init()
# py.display.set_caption("base")



blanc=(255,255,255)
gris=(117,117,117)
noir=(0,0,0)


class Affichage:
    def __init__(self,facteur):
        self.dimensions=(int(1920*facteur),int(1080*facteur))
        self.fenetre=py.display.set_mode(self.dimensions)

        self.origine=[int(0.5*self.dimensions[0]),int(0.5*self.dimensions[1])]
        self.echelle=0.005
        self.centre=(0+0j)  # zoom

        self.nb_iterations_max=30

    def loop(self):
        horloge=py.time.Clock()

        self.fenetre.fill(blanc)
        self.afficher_pixels()
        py.display.flip()



        # boucle de jeu
        continuer=True
        while continuer:
            for event in py.event.get():
                if event.type==py.QUIT:
                    continuer=False
                if event.type==py.KEYDOWN:
                    if event.key==py.K_ESCAPE:
                        continuer=False

            horloge.tick(10)
            py.display.set_caption(str(round(horloge.get_fps(),1)))


            # self.fenetre.fill(blanc)



            # self.afficher_pixels()
            # self.zoom()



            py.display.flip()
            


        py.quit()
    
    def afficher_pixels(self):
        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                pos=self.changer_referentiel([x,y])
                # print(pos)
                nombre_iterations=self.nombre_iterations(c=pos[0]+1j*pos[1])

                nombre_iterations_modif=(nombre_iterations/self.nb_iterations_max)*255
                intensite=255-nombre_iterations_modif
                self.fenetre.set_at((x,y),(intensite,intensite,intensite))

                # if nombre_iterations==self.nb_iterations_max:
                #     self.fenetre.set_at((x,y),noir)
                # else:
                #     self.fenetre.set_at((x,y),blanc)

    def sigmoide(self,x):
        return 1/(1+np.exp(-x))

    def nombre_iterations(self,c):
        z=0
        nombre_iterations=0
        
        while abs(z)<=2 and nombre_iterations<self.nb_iterations_max:
            z=np.real(z)**2-np.imag(z)**2+2j*np.real(z)*np.imag(z)+c
            nombre_iterations+=1
        return nombre_iterations
 
    def zoom(self):
        self.echelle=max(self.echelle-self.echelle/10,0)
        self.origine[0]-=10


    def changer_referentiel(self,pos):
        return [self.echelle*(pos[0]-self.origine[0]),self.echelle*(self.dimensions[1]-pos[1]-self.origine[1])]
    
    # def changer_referentiel(self,pos):
    #     return [self.echelle*(pos[0]-self.origine[0]),self.dimensions[1]-self.echelle*(pos[1]-self.origine[1])]




facteur=0.8
affichage=Affichage(facteur)
affichage.loop()