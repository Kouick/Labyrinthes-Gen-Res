from PIL import Image
import numpy as np
from copy import deepcopy
import time
from math import *
import imageio
import threading
import gc
##print("WARNING /!\ ce script détecte également les cycles, il n'est utilisable que sur des labyrinthes du type 'lab.jpg', la sortie et l'entrée peuvent cependant être changé de place, ce programme donne toute les solutions possibles")




def ckoa2(pix):     #Reconnaissance de mur/chemin.
    if pix[0]==0 and pix[1]==0 and pix[2]==0:
        return "mur"
    return "chemin"




def count(i,j):
    temp=[]
    if (ckoa2(tab[i][j])=="chemin"):
        c=0
        if i>0 and (ckoa2(tab[i-1][j])=="chemin"):
            c+=1
        if i<len(tab)-1 and (ckoa2(tab[i+1][j])=="chemin"):
            c+=1
        if j>0 and (ckoa2(tab[i][j-1])=="chemin"):
            c+=1
        if j<len(tab[0])-1 and (ckoa2(tab[i][j+1])=="chemin"):
            c+=1
        return c
    return 0



def voisins(i,j):
    temp=[]
    if (ckoa2(tab[i][j])=="chemin"):
        c=[]
        if i>0 and (ckoa2(tab[i-1][j])=="chemin"):
            c.append((i-1,j))
        if i<len(tab)-1 and (ckoa2(tab[i+1][j])=="chemin"):
            c.append((i+1,j))
        if j>0 and (ckoa2(tab[i][j-1])=="chemin"):
            c.append((i,j-1))
        if j<len(tab[0])-1 and (ckoa2(tab[i][j+1])=="chemin"):
            c.append((i,j+1))
        return c
    return []

def solv(tab):
    cur,nxt=[],[]
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            if count(i,j)<2 and not ((i,j) == (Ie, Je) or (i,j) == (Is, Js)):
                nxt.append((i,j))
    print("nxt initial créé")
    while not nxt==[]:
        cur,nxt=nxt,[]
        for cs in cur:
            i,j=cs
            temp=voisins(i,j)
            tab[i][j][0]=0
            tab[i][j][1]=0
            tab[i][j][2]=0
            for ic,jc in temp:
                if count(ic,jc)<2 and not ((ic,jc) == (Ie, Je) or (ic,jc) == (Is, Js)):
                    nxt.append((ic,jc))
    print("completion du labyrinth apres "+str(floor(time.time()-t0))+" secondes")







##def DO(g,nom,tab):
##    t0=time.time()
##    ta=deepcopy(tab)
##    print("copie finie apres "+str(floor(time.time()-t0))+" secondes")
##    solv(tab)
##    for i in range(len(tab)):
##        for j in range(len(tab[0])):
##            if not tab[0]==0:
##                ta[i][j]=[0,0,255]
##    ta[Ie][Je]=[255,0,0]
##    ta[Is][Js]=[0,255,0]
##    imageio.imwrite(nom+".png", ta)
##    print("fichier suvegardé apres " +str(floor(time.time()-t0))+" secondes")


import cv2



NAME="3.png"
NAMEFIN="3 - Soluce.png"
t0=time.time()

im = cv2.imread(NAME)
tab=np.array(im)
print("fichier chargé apres " +str(floor(time.time()-t0))+" secondes")


Ie,Je=0,0
Is,Js=len(tab)-1,len(tab[0])-1

tab[Is][Js]=[255,0,0]   #Je ne sais pas pourquoi cette ligne est necessaire mais si je ne la met pas, la sortie est un pixel bleu alors qu'il n'y a aucune raison qu'elle le soit
                        #voici un compteur du nombre d'heures passées a essayer de comprendre ce bug : 3




solv(tab)
print("labyrinthe résolu apres " +str(floor(time.time()-t0))+" secondes")

imageio.imwrite("3 - Solution seule.png", tab)

im = cv2.imread(NAME)
ta=np.array(im)

for i in range(len(tab)):
    for j in range(len(tab[0])):
        if not tab[i][j][0]==0:
            ta[i][j][0]=0
            ta[i][j][1]=0
            ta[i][j][2]=255
ta[Ie][Je]=[255,0,0]
ta[Is][Js]=[0,255,0]
print("fichier pres a la sauvegarde apres " +str(floor(time.time()-t0))+" secondes")

imageio.imwrite(NAMEFIN, ta)
print("fichier sauvegardé apres " +str(floor(time.time()-t0))+" secondes")
