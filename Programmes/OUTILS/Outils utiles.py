from PIL import Image
import numpy as np
from copy import deepcopy
import time
from math import *
import imageio
from random import *

#La fusion écrase les images l'une sur l'autre en ne collant que les zones non noires.


def fus(Name1,Name2):
    im=Image.open(Name1)
    im2=Image.open(Name2)
    tab=np.array(im)
    tab2=np.array(im2)
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            if not (tab2[i][j][0]==0 and tab2[i][j][1]==0 and tab2[i][j][2]==0):
                tab[i][j]=tab2[i][j]
    print(tab)
    imageio.imwrite("done"+".png", tab)
    (Image.fromarray(tab)).show()





def agrandis(Name,multi,multj):
    im=Image.open(Name)
    tab=np.array(im)
    ta=np.full((len(tab)*multi, len(tab[0])*multj, 3), [0, 0, 0], dtype=np.uint8)
    for i in range(len(ta)):
        for j in range(len(ta[0])):
            ta[i][j]=tab[i//multi][j//multj]
    imageio.imwrite(Name+"grand"+".png", ta)
    (Image.fromarray(ta)).show()



def ckoa(pix):     
    if pix[0]==255 and pix[1]==0 and pix[2]==0:
        return "start"
    if pix[0]==0 and pix[1]==255 and pix[2]==0:
        return "end"
    if 100>pix[0]:
        return "mur"
    return "chemin"




def clean(Name):                      #Nettoie les fichiers JPG et les rend pixel perfect et couleur perfect pour enregistrement PNG : chemin = 255,255,255; mur = 0,0,0; départ = 0,255,0; arrivée = 255,0,0.
    im=Image.open(Name)
    tab=np.array(im)
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            if ckoa(tab[i][j])=="mur":
                tab[i][j][0]=0
                tab[i][j][1]=0
                tab[i][j][2]=0
            else:
                tab[i][j][0]=255
                tab[i][j][1]=255
                tab[i][j][2]=255
    tab[0][0][0]=0
    tab[0][0][1]=255
    tab[0][0][2]=0
    tab[len(tab)-2][len(tab[0])-2][0]=255
    tab[len(tab)-2][len(tab[0])-2][1]=0
    tab[len(tab)-2][len(tab[0])-2][2]=0
    imageio.imwrite(Name+"clean"+".png", tab)
    (Image.fromarray(tab)).show()




























