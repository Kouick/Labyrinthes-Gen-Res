from PIL import Image
import numpy as np
from copy import deepcopy
import time
from math import *
import imageio

print("WARNING /!\ ce script détecte également les cycles, il n'est utilisable que sur des labyrinthes du type 'lab.jpg', la sortie et l'entrée peuvent cependant être changé de place, ce programme donne toute les solutions possibles")


SAVTEMPin=(input("Doit-on sauvegarder les étapes intermédiaires ? (True ou False)"))
RETOURSin=(input("Doit-on recevoir des retours dans la console ? (True ou False)"))
SAVTEMP=SAVTEMPin=="True"
RETOURS=RETOURSin=="True"
MAXSAVEDINTERETAP=int(input("Maximum d'étapes intermédiaires sauvegardées en images : "))
NOMFINAL=str(input("Nom du fichier de sauvegarde du labyrinthe résolu : "))
NAME=str(input("Nom du fichier du labyrinthe avec l'extension jpg ou png : "))



t0=time.time()
im=Image.open(NAME)
tab=np.array(im)


#Recherche de l'entrée et de la sortie.
azert=0
for i in range(len(tab)):
    for j in range(len(tab[0])):
        if 50<tab[i][j][0]<200 and 50<tab[i][j][1]<200 and 50<tab[i][j][2]<200:
            if azert>0:
                azert=2
                Is,Js=i,j
                break
            else:
                azert=1
                Ie,Je=i,j
    if azert==2:
        break





tab[Ie][Je]=[255,0,0]     #Marquage de l'entrée et de la sortie.
tab[Is][Js]=[0,255,0]

def ckoa(pix):     #Reconnaissance de mur/chemin/entrée/sortie.
    if pix[0]==255 and pix[1]==0 and pix[2]==0:
        return "start"
    if pix[0]==0 and pix[1]==255 and pix[2]==0:
        return "end"
    if 100>pix[0]:
        return "mur"
    return "chemin"

n=len(tab)
m=len(tab[0])


def converter(tab): #Crée un graphe g sous forme de dictionnaire, où les clés sont les coordonnées des points et les valeurs sont les listes des sommets adjacents.
    g={}
    temp=[]
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            temp=[]
            if i>0 and (ckoa(tab[i-1][j])=="chemin" or ckoa(tab[i-1][j])=="end" or ckoa(tab[i-1][j])=="start"):
                temp.append([i-1,j])
            if i<len(tab)-1 and (ckoa(tab[i+1][j])=="chemin" or ckoa(tab[i+1][j])=="end" or ckoa(tab[i+1][j])=="start"):
                temp.append([i+1,j])
            if j>0 and (ckoa(tab[i][j-1])=="chemin" or ckoa(tab[i][j-1])=="end" or ckoa(tab[i][j-1])=="start"):
                temp.append([i,j-1])
            if j<len(tab[0])-1 and (ckoa(tab[i][j+1])=="chemin" or ckoa(tab[i][j+1])=="end" or ckoa(tab[i][j+1])=="start"):
                temp.append([i,j+1])
            if (ckoa(tab[i][j])=="chemin" or ckoa(tab[i][j])=="end" or ckoa(tab[i][j])=="start"):
                g[(i,j)]=temp
                temp=[]
    print("completion de la convertion en " +str(floor(time.time()-t0))+" secondes")
    return g



def solv(g):
    a=0
    at=time.time()
    z = True
    while z:                    #Tant que le labyrinthe n'est pas résolu.
        z = False
        to_delete = []
        for c in g:             #On supprime les chemins où il n'y a qu'un seul voisin adjacent ---> cul-de-sac = mur.
            if len(g[c]) < 1:
                if not (c == (Ie, Je) or c == (Is, Js)):
                    to_delete.append(c)
                    z = True
            if len(g[c]) ==1:
                if not (c == (Ie, Je) or c == (Is, Js)):
                    z = True
                    i, j = c
                    x = [i, j]
                    to_delete.append(c)
                    k=0
                    for pos in g[c]:
                        t=pos[0],pos[1]
                        if t in g:
                            while x in g[t]:
                                g[t].remove(x)
        for key in to_delete:
            del g[key]
        a+=1
        if RETOURS:
            print("completion de l'étape " +str(a)+" en " +str(floor(time.time()-t0))+" secondes")
            at=time.time()
        if SAVTEMP:
            at=time.time()
            savetap(g,a)
    print("résolu en " +str(floor(time.time()-t0))+" secondes")
    return g



def savetap(g,a):
    ta=deepcopy(tab)
    for c in g:
        i,j=c
        ta[i][j]=[0,0,255]
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            if ckoa(tab[i][j])=="mur":
                ta[i][j]=[0,0,0]
    ta[Ie][Je]=[255,0,0]
    ta[Is][Js]=[0,255,0]
    if a<MAXSAVEDINTERETAP:
        imageio.imwrite("etape_"+str(a)+".png", ta)
    else:
        imageio.imwrite("etape_"+str(MAXSAVEDINTERETAP)+".png", ta)
    print("étape "+str(a)+" rendue en " +str(floor(time.time()-t0))+" secondes")

def end(g):       #Applique la solution sur le tableau de l'image.
    ta=deepcopy(tab)
    for c in g:
        i,j=c
        ta[i][j]=[0,0,255]
    ta[Ie][Je]=[255,0,0]
    ta[Is][Js]=[0,255,0]
    print("solution rendue en " +str(floor(time.time()-t0))+" secondes")
    return ta


def finitions():
##    for i in range(len(tab)):
##        for j in range(len(tab[0])):
##            if ckoa(tab[i][j])=="mur": #Repasse les murs en noir : artefact datant des problèmes de compression JPG, n'a rien résolu.
##                ta[i][j]=[0,0,0]
    imageio.imwrite(NOMFINAL+".png", ta)
    print("solution enregistree en " +str(floor(time.time()-t0))+" secondes")
    (Image.fromarray(ta)).show()




g=converter(tab)  #Lancement de la résolution.
solv(g)
ta=end(g)
finitions()




